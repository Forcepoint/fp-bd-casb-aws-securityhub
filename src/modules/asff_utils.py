from common import casb_cef_to_iso8601_format, get_current_epoch_timestamp_in_ms
from program_constants import (
    ASFF_TYPE,
    BLANK,
    CRITICAL,
    HIGH,
    INFORMATIONAL,
    LOW,
    MEDIUM,
    NOT_APPLICABLE,
    OTHER,
    RESOURCES_OTHER_FIELDS_LST,
    SAAS_SECURITY_GATEWAY,
    SCHEMA_VERSION,
)


def is_valid_entry(entries_dict, entry_key):
    if entries_dict.get(entry_key):
        if entries_dict.get(entry_key).strip('"'):
            return True
    return False


def normalize_severity_aws(severity):
    switcher = {6: INFORMATIONAL, 7: LOW, 8: MEDIUM, 9: HIGH, 10: CRITICAL}
    return switcher.get(severity, INFORMATIONAL)


def get_asff_field_value(record, feild, default_func):
    if is_valid_entry(record, feild):
        return record.get(feild).strip('"')
    return default_func()


def get_asff_created_time(record):
    asff_time = get_asff_field_value(
        record, "start", get_current_epoch_timestamp_in_ms()
    )
    return casb_cef_to_iso8601_format(int(asff_time))


def get_asff_current_time():
    return casb_cef_to_iso8601_format(get_current_epoch_timestamp_in_ms())


def create_id(record):
    return "{}-{}".format(record.get("SignatureID").strip('"'), record.get("Severity"))


def create_severity_object(record):
    return {
        "Label": normalize_severity_aws(int(record.get("Severity", 6))),
        "Product": int(record.get("Severity")),
    }


def create_network_object(record):
    network = {}
    network["DestinationDomain"] = get_asff_field_value(
        record, "destinationServiceName", lambda: NOT_APPLICABLE
    )[:128]
    network["DestinationIpV4"] = get_asff_field_value(
        record, "dst", lambda: NOT_APPLICABLE
    )
    network["SourceIpV4"] = get_asff_field_value(record, "src", lambda: NOT_APPLICABLE)
    return network


def create_remediation_object(record):
    remediation = {}
    recommendation = {}
    recommendation["Text"] = get_asff_field_value(
        record, "output", lambda: NOT_APPLICABLE
    )
    remediation["Recommendation"] = recommendation
    return remediation


def create_dict_of_key_values_object(
    user_defined_result_dct, fields_lst, data_source_dct
):
    if fields_lst:
        field = fields_lst[0]
        if is_valid_entry(data_source_dct, field):
            user_defined_result_dct[field] = data_source_dct.get(field).strip('"')[
                :1024
            ]
        modified_fields_lst = fields_lst.copy()
        modified_fields_lst.remove(field)
        create_dict_of_key_values_object(
            user_defined_result_dct, modified_fields_lst, data_source_dct
        )
    return user_defined_result_dct


def create_resources_object(record):
    resources = []
    resource = {}
    details = {}
    resource["Type"] = OTHER
    resource["Id"] = get_asff_field_value(record, "Product", lambda: NOT_APPLICABLE)
    details[OTHER] = create_dict_of_key_values_object(
        {}, RESOURCES_OTHER_FIELDS_LST, record
    )
    resource["Details"] = details
    resources.append(resource)
    return resources


def create_asff_finding(record, aws_account_id, product_arn):
    result = {}
    result["AwsAccountId"] = aws_account_id
    result["CreatedAt"] = get_asff_created_time(record)
    result["Description"] = get_asff_field_value(record, "cs1", lambda: BLANK)
    result["GeneratorId"] = get_asff_field_value(
        record, "Product", lambda: SAAS_SECURITY_GATEWAY
    )
    result["Id"] = create_id(record)
    result["Network"] = create_network_object(record)
    result["ProductArn"] = product_arn
    result["Remediation"] = create_remediation_object(record)
    result["Resources"] = create_resources_object(record)
    result["SchemaVersion"] = SCHEMA_VERSION
    result["Severity"] = create_severity_object(record)
    result["Title"] = get_asff_field_value(record, "cat", lambda: BLANK)
    result["Types"] = [ASFF_TYPE]
    result["UpdatedAt"] = get_asff_created_time(record)
    return result
