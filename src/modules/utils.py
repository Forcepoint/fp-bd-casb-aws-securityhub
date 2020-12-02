import logging
import ntpath
import os

from asff_utils import create_asff_finding
from aws import (
    create_securityhub_client,
    is_securityhub_connection_available,
    send_aws_securityhub_data,
)
from cef_parser import parse_cef
from common import (
    copy_file_and_delete_src,
    get_aws_fp_casb_product_arn,
    get_epoch_timestamp_in_millisec,
    get_epoch_timestamp_in_sec,
    get_epoch_timestamp_since,
    get_seconds_since_epoch,
)
from program_constants import (
    AWS_LIMIT_TIME_IN_DAYS,
    AWS_SECURITYHUB_BATCH_LIMIT,
    CEF_EXT,
)


def get_file_name(path):
    return ntpath.basename(path)


def substring_after(s, delim):
    return s.partition(delim)[2]


def get_epoch_from_filename(path):
    file_name = get_file_name(path)
    file_name_with_no_ext = os.path.splitext(file_name)[0]
    epoch_timestamp = substring_after(file_name_with_no_ext, "_")
    try:
        return int(epoch_timestamp)
    except ValueError:
        return -1


def get_content(path_and_file_name):
    if os.path.isfile(path_and_file_name):
        with open(path_and_file_name, "r") as f:
            data = f.read().strip()
            return data
    return ""


def is_valid_aws_date_range_files(cef_epoch_timestamp):
    file_timstamp = get_epoch_timestamp_in_sec(cef_epoch_timestamp)
    """ No epoch provided in the file name, process anyways """
    if file_timstamp == -1:
        return True
    elif file_timstamp < get_epoch_timestamp_since(AWS_LIMIT_TIME_IN_DAYS):
        return False
    return True


def is_valid_file(f_path, f_ext):
    return os.path.isfile(f_path) and f_path.lower().endswith(f_ext)


def get_files_list(d_path, f_ext):
    files_lst = []
    for r, _, files in os.walk(d_path):
        for f in files:
            if is_valid_file(os.path.join(r, f), f_ext):
                if is_valid_aws_date_range_files(get_epoch_from_filename(f)):
                    files_lst.append(os.path.join(r, f))
    return files_lst


def get_unprocessed_files(process_dir):
    unprocessed_files = []
    if os.path.exists(process_dir):
        unprocessed_files = get_files_list(process_dir, CEF_EXT)
    return unprocessed_files


def get_files_list_since(last_process_file, dir_path, f_ext):
    files = []
    last_process_timestamp = int(
        get_epoch_timestamp_in_millisec(get_content(last_process_file))
    )
    for f in get_files_list(dir_path, f_ext):
        if last_process_timestamp <= int(get_epoch_from_filename(f)):
            files.append(f)
    return files


def map_casb_cef_to_asff(cef_casb_dict, user_config):
    return create_asff_finding(
        cef_casb_dict,
        user_config["awsAccountId"],
        get_aws_fp_casb_product_arn(
            user_config["regionName"], user_config["awsAccountId"]
        ),
    )


def is_valid_aws_date_range(cef_epoch_timestamp):
    if get_epoch_timestamp_in_sec(cef_epoch_timestamp) < get_epoch_timestamp_since(
        AWS_LIMIT_TIME_IN_DAYS
    ):
        return False
    return True


def is_user_filter_valid(
    cef_dict,
    user_config_severity_list,
    user_config_action_list,
    user_config_product_list,
):
    if not is_valid_aws_date_range(cef_dict.get("start").strip('"')):
        return False
    if int(cef_dict.get("Severity")) not in user_config_severity_list:
        return False
    if cef_dict.get("act").lower().strip('"') not in user_config_action_list:
        return False
    if cef_dict.get("Product").lower().strip() not in user_config_product_list:
        return False
    return True


def proccess_cef_file(configs, securityhub_client, file_path):
    with open(file_path) as f:
        lines = f.readlines()
        count = 0
        aws_batch = []
        last_line_index = len(lines) - 1
        logging.info(
            "Number of Lines in: {} is: {}".format(str(file_path), str(len(lines)))
        )
        for i, line in enumerate(lines):
            cef_dict = parse_cef(line)
            if is_user_filter_valid(
                cef_dict,
                configs.user_config_severity_list,
                configs.user_config_action_list,
                configs.user_config_product_list,
            ):
                asff_record = map_casb_cef_to_asff(cef_dict, configs.user_config)
                aws_batch.append(asff_record)
                count += 1
            if count == AWS_SECURITYHUB_BATCH_LIMIT or i == last_line_index:
                send_aws_securityhub_data(securityhub_client, aws_batch)
                count = 0
                aws_batch = []
        os.remove(file_path)


def process_file(configs, securityhub_client, src_path, modify_last_process_file):
    logging.info("process_file: {}".format(str(src_path)))
    if modify_last_process_file:
        with open(configs.last_process_file, "w+") as file_to_write:
            file_to_write.write(str(get_seconds_since_epoch()))
    proccess_cef_file(configs, securityhub_client, src_path)


def pre_process_files(configs, file_lst):
    if len(file_lst) > 0:
        securityhub_client = create_securityhub_client(configs.user_config)
        if is_securityhub_connection_available(securityhub_client):
            for f_path in file_lst:
                process_file_path = copy_file_and_delete_src(
                    f_path, configs.process_dir, configs.user_config_delete_files
                )
                process_file(configs, securityhub_client, process_file_path, True)
        else:
            for f_path in file_lst:
                copy_file_and_delete_src(
                    f_path, configs.missed_dir, configs.user_config_delete_files
                )


def process_unprocessed_files(configs, process_dir):
    unprocessed_files = get_unprocessed_files(process_dir)
    if len(unprocessed_files) > 0:
        securityhub_client = create_securityhub_client(configs.user_config)
        if is_securityhub_connection_available(securityhub_client):
            for f_path in unprocessed_files:
                process_file(configs, securityhub_client, f_path, False)


def process_previous_siem_files(configs):
    """ Determine which files to process """
    logging.info("process_previous_siem_files")
    siem_files = []
    if not os.path.isfile(configs.last_process_file):
        if configs.user_config_send_historical_data:
            siem_files = get_files_list(configs.user_config_src_path, CEF_EXT)
    else:
        siem_files = get_files_list_since(
            configs.last_process_file, configs.user_config_src_path, CEF_EXT
        )
    """ Process the files """
    pre_process_files(configs, siem_files)


def process_siem_previous_files(configs):
    process_unprocessed_files(configs, configs.process_dir)
    process_previous_siem_files(configs)


def process_siem_event_file(configs, src_path):
    if is_valid_file(src_path, CEF_EXT):
        pre_process_files(configs, [src_path])


def process_siem_missed_files(configs):
    process_unprocessed_files(configs, configs.missed_dir)
