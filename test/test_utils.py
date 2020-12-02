from src.modules import common as c
from src.modules import program_constants as const
from src.modules import utils as utl

from .t_utils import create_file, delete_file_content, delete_files
from .test_data import (
    TEST_RECORD_1,
    USER_CONFIG_ACTION_LIST,
    USER_CONFIG_PRODUCT_LIST,
    USER_CONFIG_SEVERITY_LIST,
)


def test_get_file_name() -> None:
    assert utl.get_file_name("/home/test.cef") == "test.cef"


def test_substring_after() -> None:
    assert utl.substring_after("ALert_99999999", "_") == "99999999"


def test_get_epoch_from_filename() -> None:
    assert utl.get_epoch_from_filename("/home/test_99999999.cef") == 99999999


def test_get_content() -> None:
    assert utl.get_content("/home/test_99999999.cef") == ""


def test_is_valid_aws_date_range_files() -> None:
    assert utl.is_valid_aws_date_range_files("test.cef") is True
    assert (
        utl.is_valid_aws_date_range_files(c.get_current_epoch_timestamp_in_ms()) is True
    )
    assert utl.is_valid_aws_date_range_files("1513971969000") is False


def test_is_valid_file() -> None:
    create_file("test.cef", "test")
    assert utl.is_valid_file("test.cef", const.CEF_EXT) is True
    delete_file_content("test.cef")
    # sometimes the os is reporting 0 size when the file has content!
    assert utl.is_valid_file("test.cef", const.CEF_EXT) is True
    create_file("test.text", "test")
    assert utl.is_valid_file("test.text", const.CEF_EXT) is False
    assert utl.is_valid_file("test", const.CEF_EXT) is False
    delete_files(["test.cef", "test.text"])


def test_is_valid_aws_date_range() -> None:
    assert utl.is_valid_aws_date_range("test.cef") is False
    assert utl.is_valid_aws_date_range(c.get_current_epoch_timestamp_in_ms()) is True
    assert utl.is_valid_aws_date_range("1513971969000") is False


def test_is_user_filter_valid() -> None:
    assert (
        utl.is_user_filter_valid(
            TEST_RECORD_1,
            USER_CONFIG_SEVERITY_LIST,
            USER_CONFIG_ACTION_LIST,
            USER_CONFIG_PRODUCT_LIST,
        )
        is False
    )
