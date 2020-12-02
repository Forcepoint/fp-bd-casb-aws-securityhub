#!/usr/bin/env bash

sudo systemctl stop casb-siem-aws-securityhub-batch.service casb-siem-aws-securityhub-batch.timer casb-siem-aws-securityhub.service casb-siem-batch.service casb-siem-batch-timer.service
sudo systemctl disable casb-siem-aws-securityhub-batch.service casb-siem-aws-securityhub-batch.timer casb-siem-aws-securityhub.service casb-siem-batch.service casb-siem-batch-timer.service
sudo rm /etc/systemd/system/casb-siem-aws-securityhub-batch.service
sudo rm /etc/systemd/system/casb-siem-aws-securityhub-batch.timer
sudo rm /etc/systemd/system/casb-siem-aws-securityhub.service
sudo rm /etc/systemd/system/casb-siem-batch.service
sudo rm /etc/systemd/system/casb-siem-batch-timer.service
    
sudo systemctl daemon-reload
sudo systemctl reset-failed

ps aux | grep casb-siem
jobs -l
systemctl list-unit-files | grep casb-siem
