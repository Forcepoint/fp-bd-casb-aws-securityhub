import json
import os

from common import create_dir, pupulate_cef_filter_list, pupulate_cef_severity_list
from program_constants import (
    CLOUDFORMATION_STACK_TEMPLATE_FILE,
    DEFAULT_INSIGHTS_FILE,
    INSIGHTS_ARNS_FILE,
)


class Configs:
    def __init__(self):
        self._modules_dir = None
        self._source_dir = None
        self._home_dir = None
        self._config_file = None
        self.user_config = None
        self.process_dir = None
        self.last_process_file = None
        self.missed_dir = None
        self.log_dir = None
        self.aws_resources_dir = None
        self.default_insights_file = None
        self.insights_arns_file = None
        self.cloudFormation_stack_file = None
        self.user_config_delete_files = None
        self.user_config_send_historical_data = None
        self.user_config_src_path = None
        self.user_config_severity_list = None
        self.user_config_action_list = None
        self.user_config_product_list = None
        self._init()

    def _init(self):
        """ Configs for the configuration file """
        self._modules_dir = os.path.dirname(os.path.realpath(__file__))
        self._source_dir = os.path.abspath(os.path.join(self._modules_dir, os.pardir))
        self._home_dir = os.path.abspath(os.path.join(self._source_dir, os.pardir))
        self._config_file = "{}/{}".format(self._home_dir, "cfg.json")
        self._init_config_file(self._config_file)
        """ Configs for the processing directory """
        self.process_dir = "{}/{}".format(self._home_dir, "process-files")
        self.last_process_file = "{}/{}".format(self.process_dir, "last-process-file")
        create_dir(self.process_dir)
        """ Configs for the processing missed directory """
        self.missed_dir = "{}/{}".format(self._home_dir, "missed-files")
        create_dir(self.missed_dir)
        """ Configs for the logging """
        self.log_dir = "{}/{}".format(self._home_dir, "logs")
        create_dir(self.log_dir)
        """ Configs for AWS resources """
        self.aws_resources_dir = "{}/{}".format(self._home_dir, "aws-resources")
        self.default_insights_file = "{}/{}".format(
            self.aws_resources_dir, DEFAULT_INSIGHTS_FILE
        )
        self.insights_arns_file = "{}/{}".format(
            self.aws_resources_dir, INSIGHTS_ARNS_FILE
        )
        self.cloudFormation_stack_file = "{}/{}".format(
            self.aws_resources_dir, CLOUDFORMATION_STACK_TEMPLATE_FILE
        )
        """ Configs for the user input """
        self.user_config_delete_files = self.user_config["deleteSiemFiles"]
        self.user_config_send_historical_data = self.user_config[
            "firstRunSendHistoricalData"
        ]
        self.user_config_src_path = self.user_config["siemPath"]
        self.user_config_severity_list = pupulate_cef_severity_list(
            self.user_config["severityFilterInclude"]
        )
        self.user_config_action_list = pupulate_cef_filter_list(
            self.user_config["actionFilterInclude"]
        )
        self.user_config_product_list = pupulate_cef_filter_list(
            self.user_config["productFilterInclude"]
        )

    def _init_config_file(self, config_file):
        with open(config_file) as conf_file:
            self.user_config = json.load(conf_file)
