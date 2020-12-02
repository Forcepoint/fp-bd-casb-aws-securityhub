#!/usr/bin/env python3

from configs import Configs
from log_config import LogConfig
from program_constants import BATCH_LOG_FILE_NAME
from utils import process_siem_missed_files

if __name__ == "__main__":
    configs = Configs()
    LogConfig(configs.log_dir, BATCH_LOG_FILE_NAME)
    """ Process files that were missed for network down or other reasons """
    process_siem_missed_files(configs)
