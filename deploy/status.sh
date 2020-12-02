#!/usr/bin/env bash

systemctl status casb-siem-aws-securityhub-batch.service casb-siem-aws-securityhub-batch.timer casb-siem-aws-securityhub.service
systemctl status casb-siem-batch.service casb-siem-batch-timer.service
