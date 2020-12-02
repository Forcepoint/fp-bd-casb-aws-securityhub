#!/usr/bin/env python3

from aws import (
    create_cloudformation_stack,
    create_securityhub_insights,
    enable_securityhub_product,
)
from configs import Configs
from log_config import LogConfig
from program_constants import CLOUDFORMATION_STACK_NAME, STREAM_LOG_FILE_NAME
from utils import process_siem_previous_files
from watcher import create_siem_watcher_and_run

if __name__ == "__main__":
    configs = Configs()
    LogConfig(configs.log_dir, STREAM_LOG_FILE_NAME)

    """ Enable Security Hub """
    create_cloudformation_stack(
        configs.user_config,
        CLOUDFORMATION_STACK_NAME,
        configs.cloudFormation_stack_file,
    )

    """ Enable Import Findings For Product """
    enable_securityhub_product(configs.user_config)

    """ Create Insights """
    create_securityhub_insights(
        configs.user_config, configs.default_insights_file, configs.insights_arns_file
    )

    """ Process SIEM historical files or/and any SIEM files that are left to process since last run and process unprocessed files """
    process_siem_previous_files(configs)

    """ Run SIEM Watcher """
    create_siem_watcher_and_run(configs)
