#!/usr/bin/env bash
# Update Package
sudo apt update
sudo apt -y install nginx

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo chown -R ubuntu:ubuntu /data/

sudo echo "WIRELEXZ..." > /data/web_static/releases/test/index.html

ln -s /data/web_static/releases/test/ /data/web_static/current

CONFIG="server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"

FILE="/etc/nginx/sites-available/default"

sudo sed -i "s|server_name _;|$CONFIG|" $FILE

sudo system nginx restart
