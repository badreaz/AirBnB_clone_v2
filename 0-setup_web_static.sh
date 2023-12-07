#!/usr/bin/env bash
# sets up the web servers for the deployment of web-static
apt-get update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "test server" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
printf %s "server {
\tlisten 80 default_server;
\tlisten [::]:80 default_server;
\tadd_header X-Served-By $HOSTNAME;
\troot /var/www/html;
\tindex index.html index.htm;
\tlocation /hbnb_static {
\t\talias /data/web_static/current;
\t\tindex index.html index.htm;\n\t}
\tlocation /redirect_me {
\t\treturn 301 http://www.google.com;\n\t}
\terror_page 404 /404.html;
\tlocation /404 {
\t\troot /var/ww/html;
\t\tinternal;\n\t}\n}" > /etc/nginx/sites-available/default
service nginx restart
