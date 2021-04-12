import asyncio
import logging
import os
import time
from signal import SIGTERM

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from common import (
    get_aws_fp_casb_product_arn,
    get_current_epoch_timestamp_in_ms,
    get_json_content,
    write_json_to_a_file,
    write_to_a_file,
)
from program_constants import CEF_EXT, MAX_RETRIES

""" securityhub """


def create_securityhub_client(user_config):
    return boto3.client(
        "securityhub",
        aws_access_key_id=user_config["awsAccessKeyId"],
        aws_secret_access_key=user_config["awsSecretAccessKey"],
        region_name=user_config["regionName"],
    )


def is_securityhub_connection_available(securityhub_client):
    try:
        response = securityhub_client.describe_hub()
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
    except (ClientError, EndpointConnectionError) as exception:
        logging.error("is_securityhub_connection_available: {}".format(exception))
    return False


async def aws_security_hub_batch_upload(
    securityhub_client, asff_findings, original_findings_lst, missed_dir
):
    try:
        logging.info(securityhub_client.batch_import_findings(Findings=asff_findings))
    except (ClientError, EndpointConnectionError) as error:
        # the documentation mentioned ThrottlingException status code 400! hence adding extra checks
        if error.response["ResponseMetadata"][
            "HTTPStatusCode"
        ] == 429 or error.response["Error"]["Code"] in (
            "LimitExceededException",
            "ThrottlingException",
        ):
            # write to missed_dir to proceess latter
            __file_name = get_current_epoch_timestamp_in_ms()
            write_to_a_file(
                "{}/throttling_{}{}".format(missed_dir, __file_name, CEF_EXT),
                original_findings_lst,
            )
            logging.warn(
                "aws_security_hub_batch_upload - API call limit exceeded; backing off and adding the content into a missed directory"
            )
        else:
            logging.error(error)


def send_aws_securityhub_data(
    securityhub_client, asff_list, original_findings_lst, missed_dir
):
    logging.info("send_aws_securityhub_data: {}".format(str(len(asff_list))))
    if len(asff_list) > 0:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(
            aws_security_hub_batch_upload(
                securityhub_client, asff_list, original_findings_lst, missed_dir
            )
        )
        loop.run_until_complete(task)


def retrieve_securityhub_insights_arns(securityhub_client):
    insights = securityhub_client.get_insights()["Insights"]
    securityhub_insight_arns = map(lambda insight: insight["InsightArn"], insights)
    return list(securityhub_insight_arns)


def create_securityhub_insights(user_config, default_insights_file, insights_arns_file):
    if (
        not os.path.exists(insights_arns_file)
        or os.stat(insights_arns_file).st_size == 0
    ):
        response_list = []
        insights = get_json_content(default_insights_file)
        securityhub_client = create_securityhub_client(user_config)
        if is_securityhub_connection_available(securityhub_client):
            try:
                for insight in insights:
                    response = securityhub_client.create_insight(
                        Name=insight["Name"],
                        Filters=insight["Filters"],
                        GroupByAttribute=insight["GroupByAttribute"],
                    )
                    response_list.append(response["InsightArn"])
                logging.info("Insights are created: {}".format(response_list))
                write_json_to_a_file(insights_arns_file, response_list)
            except securityhub_client.exceptions.LimitExceededException:
                logging.info("create_securityhub_insights - LimitExceededException")
        else:
            logging.error("Insights didn't created, Error in AWS connection")


def enable_securityhub_product(user_config):
    securityhub_client = create_securityhub_client(user_config)
    if is_securityhub_connection_available(securityhub_client):
        try:
            casb_product_arn = get_aws_fp_casb_product_arn(
                user_config["regionName"],
                user_config["govFlag"],
            )
            response = securityhub_client.enable_import_findings_for_product(
                ProductArn=casb_product_arn
            )
            logging.info("enable_securityhub_product: {}".format(response))
        except securityhub_client.exceptions.ResourceConflictException:
            logging.info(
                "enable_securityhub_product - ResourceConflictException - {} - this product is already have been enabled".format(
                    casb_product_arn
                )
            )
    else:
        logging.error(
            "enable_securityhub_product- Error in AWS connection - Can't enable securityhub product."
        )
        print("Error in AWS connection")
        os.kill(os.getpid(), SIGTERM)


""" cloudformation """


def create_cloudformation_client(user_config):
    return boto3.client(
        "cloudformation",
        aws_access_key_id=user_config["awsAccessKeyId"],
        aws_secret_access_key=user_config["awsSecretAccessKey"],
        region_name=user_config["regionName"],
    )


def is_cloudformation_connection_available(cloudformation_client):
    try:
        response = cloudformation_client.list_stacks()
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
    except (ClientError, EndpointConnectionError) as exception:
        logging.error("is_cloudformation_connection_available: {}".format(exception))
    return False


def is_cloudformation_stack_exist(cloudformation_client, stack_name):
    try:
        logging.info(cloudformation_client.get_stack_policy(StackName=stack_name))
        return True
    except ClientError as exception:
        logging.info("{}, Creating the {}".format(exception, stack_name))
        return False


def describe_stack(cloudformation_client, stack_name):
    try:
        return cloudformation_client.describe_stacks(StackName=stack_name)
    except ClientError as exception:
        logging.error("is_describe_stack {} - {}".format(exception, stack_name))


def is_securityhub_enabled_stack_created(cloudformation_client, stack_name):
    try:
        response = describe_stack(cloudformation_client, stack_name)
        if response["Stacks"][0]["StackStatus"] == "CREATE_COMPLETE":
            return True
        elif response["Stacks"][0]["StackStatus"] == "ROLLBACK_COMPLETE":
            # exception here where ROLLBACK_COMPLETE could happen in case security hub was already enabled
            return True
    except ClientError as exception:
        logging.error("is_stack_created {} - {}".format(exception, stack_name))
        raise
    return False


def aws_cloudformation_create_stack(
    cloudformation_client, stack_name, stack_template_file
):
    if not is_cloudformation_stack_exist(cloudformation_client, stack_name):
        try:
            logging.info(
                cloudformation_client.create_stack(
                    StackName=stack_name,
                    TemplateBody=str(get_json_content(stack_template_file)),
                )
            )
            # we need to make sure that securityhub is enabled before we create insights.
            stack_created = False
            attempts = 1
            while not stack_created:
                logging.info("Waiting for Security Hub to be enabled...")
                time.sleep(5)
                stack_created = is_securityhub_enabled_stack_created(
                    cloudformation_client, stack_name
                )
                attempts += 1
                if attempts >= MAX_RETRIES:
                    logging.error(
                        "Max attempts reached. Error in Security Hub enabling!"
                    )
                    print("Error in Security Hub enabling")
                    os.kill(os.getpid(), SIGTERM)

        except ClientError as exception:
            logging.error(exception)


def create_cloudformation_stack(user_config, stack_name, stack_template_file):
    cloudformation_client = create_cloudformation_client(user_config)
    if is_cloudformation_connection_available(cloudformation_client):
        aws_cloudformation_create_stack(
            cloudformation_client, stack_name, stack_template_file
        )
