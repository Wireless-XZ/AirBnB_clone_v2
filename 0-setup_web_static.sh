#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment

# Check if Nginx is already installed
if ! command -v nginx &>/dev/null; then
    # Install Nginx
    sudo apt-get update
    sudo apt-get install nginx -y
fi

# Create necessary directories if they don't already exist
if [ ! -d "/data" ]; then
    sudo mkdir /data
fi

if [ ! -d "/data/web_static" ]; then
    sudo mkdir /data/web_static
fi

if [ ! -d "/data/web_static/releases" ]; then
    sudo mkdir /data/web_static/releases
fi

if [ ! -d "/data/web_static/shared" ]; then
    sudo mkdir /data/web_static/shared
fi

if [ ! -d "/data/web_static/releases/test" ]; then
    sudo mkdir /data/web_static/releases/test
fi

# Create a fake index.html file
echo "test content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or update symbolic link
if [ -L "/data/web_static/current" ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
EOF
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;
        root /data/web_static/current;
        index index.html;

        location /hbnb_static/ {
                alias /data/web_static/current/;
        }
}
EOF

# Restart Nginx
sudo service nginx restart

EOF
