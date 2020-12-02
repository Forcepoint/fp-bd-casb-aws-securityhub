import calendar
import datetime as dt
import json
import logging
import os
import shutil
import time

from program_constants import ONE_DAY_IN_SEC


def get_seconds_since_epoch():
    return calendar.timegm(time.gmtime())


def get_current_epoch_timestamp_in_ms():
    return int(get_seconds_since_epoch() * 1000)


def get_epoch_timestamp_since(days):
    return get_seconds_since_epoch() - (days * ONE_DAY_IN_SEC)


def epoch_to_iso8601_format(seconds_since_epoch):
    return dt.datetime.utcfromtimestamp(seconds_since_epoch).isoformat()


def casb_cef_to_iso8601_format(seconds_since_epoch):
    return "{}Z".format(epoch_to_iso8601_format(int(seconds_since_epoch / 1000)))


def get_asff_current_time():
    return casb_cef_to_iso8601_format(get_current_epoch_timestamp_in_ms())


def get_epoch_timestamp_in_sec(millisec):
    if millisec == -1:
        return millisec
    try:
        return int(int(millisec) / 1000)
    except ValueError:
        return -1


def get_epoch_timestamp_in_millisec(sec):
    try:
        return int(int(sec) * 1000)
    except ValueError:
        return -1


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def normalize_severity_casb(severity):
    switcher = {
        "info": list(range(0, 7)),
        "low": 7,
        "medium": 8,
        "high": 9,
        "critical": 10,
    }
    return switcher.get(severity.lower().strip(), -1)


def pupulate_cef_severity_list(user_severity_list):
    severity_list = []
    for s in user_severity_list:
        normalize_s = normalize_severity_casb(s)
        severity_list.extend(
            [normalize_s] if isinstance(normalize_s, int) else normalize_s
        )
    return severity_list


def pupulate_cef_filter_list(user_filter_list):
    filter_list = []
    for s in user_filter_list:
        filter_list.append(s.lower().strip())
    return filter_list


def delete_file(f_path):
    logging.info("delete_file: {}".format(f_path))
    if os.path.exists(f_path) and os.path.isfile(f_path):
        os.remove(f_path)
    else:
        logging.error("Error deleting this file: {}".format(f_path))


def copy_file_and_delete_src(src_path, dst_dir, user_config_delete_files):
    dst = None
    os.makedirs(os.path.dirname(dst_dir), exist_ok=True)
    if os.path.exists(src_path) and os.path.isfile(src_path):
        dst = shutil.copy(src_path, dst_dir)
    else:
        logging.error("Error copying this file: {}".format(src_path))
    """ User feature toggle - delete original SIEM processed file """
    if user_config_delete_files:
        delete_file(src_path)
    return dst


def get_json_content(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def write_to_a_file(file_path, content):
    with open(file_path, "w+") as f:
        f.write(json.dumps(content))


def get_aws_fp_casb_product_arn(region_name, aws_account_id):
    return "arn:aws:securityhub:{}:{}:product/forcepoint/forcepoint-casb".format(
        region_name, aws_account_id
    )
