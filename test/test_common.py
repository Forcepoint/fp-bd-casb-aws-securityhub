from src.modules import common as c


def test_epoch_to_iso8601_format() -> None:
    assert c.epoch_to_iso8601_format(1575971969) == "2019-12-10T09:59:29"


def test_casb_cef_to_iso8601_format() -> None:
    assert c.casb_cef_to_iso8601_format(1575971969000) == "2019-12-10T09:59:29Z"


def test_get_epoch_timestamp_in_sec() -> None:
    assert c.get_epoch_timestamp_in_sec(1575971969000) == 1575971969
    assert c.get_epoch_timestamp_in_sec(1575971969123) == 1575971969
    assert c.get_epoch_timestamp_in_sec("1575971969000") == 1575971969
    assert c.get_epoch_timestamp_in_sec("xyz") == -1


def test_get_epoch_timestamp_in_millisec() -> None:
    assert c.get_epoch_timestamp_in_millisec(1575971969) == 1575971969000
    assert c.get_epoch_timestamp_in_millisec(15759719695) == 15759719695000
    assert c.get_epoch_timestamp_in_millisec("1575971969") == 1575971969000
    assert c.get_epoch_timestamp_in_millisec("xyz") == -1


def test_normalize_severity_casb() -> None:
    assert c.normalize_severity_casb("Info") == [0, 1, 2, 3, 4, 5, 6]
    assert c.normalize_severity_casb("Low") == 7
    assert c.normalize_severity_casb("Medium") == 8
    assert c.normalize_severity_casb("HIGH ") == 9
    assert c.normalize_severity_casb("critical") == 10
    assert c.normalize_severity_casb("random") == -1


def test_pupulate_cef_severity_list() -> None:
    assert c.pupulate_cef_severity_list(["Info"]) == [0, 1, 2, 3, 4, 5, 6]
    assert c.pupulate_cef_severity_list(["Low"]) == [7]
    assert c.pupulate_cef_severity_list(["Medium"]) == [8]
    assert c.pupulate_cef_severity_list(["High"]) == [9]
    assert c.pupulate_cef_severity_list(["Critical"]) == [10]
    assert c.pupulate_cef_severity_list(["Info", "Low"]) == [0, 1, 2, 3, 4, 5, 6, 7]
    assert c.pupulate_cef_severity_list(["random"]) == [-1]
    assert c.pupulate_cef_severity_list(["Medium", "random"]) == [8, -1]
    assert c.pupulate_cef_severity_list(["High", "Critical"]) == [9, 10]


def test_pupulate_cef_filter_list() -> None:
    assert c.pupulate_cef_filter_list(["Block", "Monitor"]) == ["block", "monitor"]
    assert c.pupulate_cef_filter_list(["Block ", "MONITOR"]) == ["block", "monitor"]
    assert c.pupulate_cef_filter_list(
        [
            "SaaS Security Gateway ",
            "CASB INCIDENTS",
            " CASB Admin audit log ",
            "Cloud Service Monitoring",
        ]
    ) == [
        "saas security gateway",
        "casb incidents",
        "casb admin audit log",
        "cloud service monitoring",
    ]


def test_get_aws_fp_casb_product_arn() -> None:
    assert (
        c.get_aws_fp_casb_product_arn("eu-central-1", False)
        == "arn:aws:securityhub:eu-central-1:365761988620:product/forcepoint/forcepoint-casb"
    )
    assert (
        c.get_aws_fp_casb_product_arn("eu-west-1", True)
        == "arn:aws-us-gov:securityhub:eu-west-1:365761988620:product/forcepoint/forcepoint-casb"
    )
