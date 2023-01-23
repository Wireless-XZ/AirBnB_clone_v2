
#!/usr/bin/env bash
# A bash script that sets up your
# web servers for deployment

# set Nginx location block
server="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\
\t}"

# set nginx config file
file="/etc/nginx/sites-available/default"

# Update system
sudo apt-get update -y

# Install Nginx
sudo apt-get install nginx -y

# Create relevant directories
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir "/data/web_static/shared/"

# create dummy html page
echo "Wireless" | sudo tee "/data/web_static/releases/test/index.html"

# remove and create new symlink
sudo rm -f "/data/web_static/current"
sudo ln -s "/data/web_static/releases/test/" "/data/web_static/current"

# Give user ownership of /data/ dir
sudo chown -R ubuntu:ubuntu "/data/"

# add location block to nginx config file
sudo sed -i "29i\ $server" "$file"

# restart nginx service
sudo service nginx restart
