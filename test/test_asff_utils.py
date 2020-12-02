from src.modules import asff_utils as asff
from src.modules import program_constants as const

from .test_data import FIELDS_LST, TEST_RECORD_1


def test_is_valid_entry() -> None:
    assert asff.is_valid_entry(TEST_RECORD_1, "cs1") is False
    assert asff.is_valid_entry(TEST_RECORD_1, "deviceProcessName") is False
    assert asff.is_valid_entry(TEST_RECORD_1, "app") is True
    assert asff.is_valid_entry(TEST_RECORD_1, "destinationServiceName") is True


def test_normalize_severity_aws() -> None:
    assert asff.normalize_severity_aws(0) == const.INFORMATIONAL
    assert asff.normalize_severity_aws(6) == const.INFORMATIONAL
    assert asff.normalize_severity_aws(7) == const.LOW
    assert asff.normalize_severity_aws(8) == const.MEDIUM
    assert asff.normalize_severity_aws(9) == const.HIGH
    assert asff.normalize_severity_aws(10) == const.CRITICAL


def test_get_asff_field_value() -> None:
    assert (
        asff.get_asff_field_value(TEST_RECORD_1, "cs1", lambda: const.BLANK)
        == const.BLANK
    )
    assert (
        asff.get_asff_field_value(
            TEST_RECORD_1, "deviceProcessName", lambda: const.BLANK
        )
        == const.BLANK
    )
    assert (
        asff.get_asff_field_value(TEST_RECORD_1, "app", lambda: const.BLANK)
        == "Office Apps"
    )
    assert (
        asff.get_asff_field_value(
            TEST_RECORD_1, "destinationServiceName", lambda: const.BLANK
        )
        == "Office365"
    )


def test_get_asff_created_time() -> None:
    assert asff.get_asff_created_time(TEST_RECORD_1) == "2019-09-22T17:06:10Z"


def test_create_id() -> None:
    assert asff.create_id(TEST_RECORD_1) == "250677275138-9"


def test_create_severity_object() -> None:
    assert asff.create_severity_object(TEST_RECORD_1) == {
        "Label": const.HIGH,
        "Product": 9,
    }


def test_create_network_object() -> None:
    assert asff.create_network_object(TEST_RECORD_1) == {
        "DestinationDomain": "Office365",
        "DestinationIpV4": "40.90.23.111",
        "SourceIpV4": "192.168.122.178",
    }


def test_create_remediation_object() -> None:
    assert asff.create_remediation_object(TEST_RECORD_1) == {
        "Recommendation": {"Text": "N/A"}
    }


def test_create_resources_object() -> None:
    assert asff.create_resources_object(TEST_RECORD_1) == [
        {
            "Type": "Other",
            "Id": "SaaS Security Gateway",
            "Details": {
                "Other": {
                    "Name": "login",
                    "suid": "02vt",
                    "suser": "02v",
                    "act": "Block",
                    "cat": "Block Access to personal Office365/Block Access to personal Office365",
                    "app": "Office Apps",
                    "deviceFacility": "true",
                    "dpriv": "User",
                    "end": "1569171970000",
                    "externalId": "787",
                    "fsize": "0",
                    "msg": "//France/United States/",
                    "proto": "Office Apps",
                    "reason": "login",
                    "request": "https://login.live.com/rst2.srf",
                    "requestClientApplication": 'Desktop/Windows 10/"mozilla/4.0 (compatible; msie 6.0; windows nt 10.0; win64; .net4.0c; .net4.0e; idcrl 14.10.0.15063.0.0; idcrl-cfg 16.0.26889.0; app svchost.exe, 10.0.15063.0, {df60e2df-88ad})',
                    "rt": "1569171970000",
                    "sourceServiceName": "Managed",
                    "cs5": "false",
                    "AD.IPOrigin": "External",
                    "AD.samAccountName": "02vta",
                    "dproc": "Unknown",
                    "cn1": "null",
                    "dvc": "10.1.4.11",
                    "dvchost": "my.skyfence.com",
                }
            },
        }
    ]


def test_create_dict_of_key_values_object() -> None:
    assert asff.create_dict_of_key_values_object({}, FIELDS_LST, TEST_RECORD_1) == {
        "Name": "login",
        "suid": "02vt",
        "suser": "02v",
    }


def test_create_asff_finding() -> None:
    assert asff.create_asff_finding(
        TEST_RECORD_1, "123", "arn:aws:securityhub:eu-west-2:123:product/123/default"
    ) == {
        "AwsAccountId": "123",
        "CreatedAt": "2019-09-22T17:06:10Z",
        "Description": "blank",
        "GeneratorId": "SaaS Security Gateway",
        "Id": "250677275138-9",
        "Network": {
            "DestinationDomain": "Office365",
            "DestinationIpV4": "40.90.23.111",
            "SourceIpV4": "192.168.122.178",
        },
        "ProductArn": "arn:aws:securityhub:eu-west-2:123:product/123/default",
        "Remediation": {"Recommendation": {"Text": "N/A"}},
        "Resources": [
            {
                "Type": "Other",
                "Id": "SaaS Security Gateway",
                "Details": {
                    "Other": {
                        "Name": "login",
                        "suid": "02vt",
                        "suser": "02v",
                        "act": "Block",
                        "cat": "Block Access to personal Office365/Block Access to personal Office365",
                        "app": "Office Apps",
                        "deviceFacility": "true",
                        "dpriv": "User",
                        "end": "1569171970000",
                        "externalId": "787",
                        "fsize": "0",
                        "msg": "//France/United States/",
                        "proto": "Office Apps",
                        "reason": "login",
                        "request": "https://login.live.com/rst2.srf",
                        "requestClientApplication": 'Desktop/Windows 10/"mozilla/4.0 (compatible; msie 6.0; windows nt 10.0; win64; .net4.0c; .net4.0e; idcrl 14.10.0.15063.0.0; idcrl-cfg 16.0.26889.0; app svchost.exe, 10.0.15063.0, {df60e2df-88ad})',
                        "rt": "1569171970000",
                        "sourceServiceName": "Managed",
                        "cs5": "false",
                        "AD.IPOrigin": "External",
                        "AD.samAccountName": "02vta",
                        "dproc": "Unknown",
                        "cn1": "null",
                        "dvc": "10.1.4.11",
                        "dvchost": "my.skyfence.com",
                    }
                },
            }
        ],
        "SchemaVersion": "2018-10-08",
        "Severity": {"Label": const.HIGH, "Product": 9},
        "Title": "Block Access to personal Office365/Block Access to personal Office365",
        "Types": ["Unusual Behaviors/Application/ForcepointCASB"],
        "UpdatedAt": "2019-09-22T17:06:10Z",
    }
