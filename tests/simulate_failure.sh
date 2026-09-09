#!/bin/bash
# Simule une panne : crée un service qui échoue volontairement

echo "🔧 Création d'un service de test qui va échouer..."

sudo tee /etc/systemd/system/test-fail.service > /dev/null << 'SERVICE'
[Unit]
Description=Service de test pour TermCopilot

[Service]
ExecStart=/bin/false
Restart=no

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl start test-fail.service

echo "✅ Le service 'test-fail' a été démarré et va échouer."
echo "Lance maintenant : python3 -m termcopilot.cli diagnose"
