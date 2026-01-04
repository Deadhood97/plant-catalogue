#!/bin/bash

# Plant Catalogue Service Setup Script
# This script sets up systemd services and Nginx configuration for the Plant Catalogue.

set -e  # Exit on error

echo "🌿 Setting up Plant Catalogue Services..."

# 1. Setup Backend Service
echo " -> Installing Backend Service..."
sudo cp plant-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now plant-backend
echo "    ✅ Backend Service Installed"

# 2. Setup Monitor Service
echo " -> Installing Monitor Service..."
sudo cp plant-monitor.service /etc/systemd/system/
sudo systemctl enable --now plant-monitor
echo "    ✅ Monitor Service Installed"

# 3. Setup Nginx
echo " -> Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/plant-catalogue
# Link if not exists
if [ ! -L /etc/nginx/sites-enabled/plant-catalogue ]; then
    sudo ln -s /etc/nginx/sites-available/plant-catalogue /etc/nginx/sites-enabled/
fi
sudo systemctl restart nginx
echo "    ✅ Nginx Configured"

echo "🎉 Setup Complete! Visit http://localhost to see your Plant Catalogue."
