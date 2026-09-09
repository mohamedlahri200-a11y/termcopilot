#!/bin/bash
sudo systemctl stop test-fail.service
sudo systemctl disable test-fail.service
sudo rm -f /etc/systemd/system/test-fail.service
sudo systemctl daemon-reload
echo "🧹 Nettoyage terminé."
