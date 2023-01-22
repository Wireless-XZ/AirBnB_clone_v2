#!/usr/bin/env bash
#
# Update Package
#
sudo apt update
sudo apt -y install nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir /data/web_static/shared/

sudo echo "WIRELEXZ..." | sudo tee /data/web_static/releases/test/index.html

rm -f "/data/web_static/current";
ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu "/data/"

CONFIG="server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"

FILE="/etc/nginx/sites-available/default"

sudo sed -i "s|server_name _;|$CONFIG|" $FILE

sudo system nginx restart
