#!/bin/bash
# https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/#apt-repo-fresh-install

# Install mysql server
sudo apt update && sudo apt upgrade
sudo apt install mysql-server
mysql --version

# To get into root of the server: sudo mysql -u root # type 'exit' to quit root mode

# Starting and Stopping the MySQL Server
# dir '/etc/init.d' stores services that can be started and stopped manually - find the correct process name (might be mysql or mysqld)
service $(cd /etc/init.d; grep -l mysql *) status  # the server is active by default after installation
service $(cd /etc/init.d; grep -l mysql *) stop
service $(cd /etc/init.d; grep -l mysql *) start   # can be one of start/stop/status/restart

# Adding the MySQL APT Repository
wget "https://dev.mysql.com/get/mysql-apt-config_0.8.23-1_all.deb" -O ~/Downloads/mysql-apt-config_0.8.23-1_all.deb
sudo dpkg -i ~/Downloads/mysql-apt-config_0.8.23-1_all.deb
sudo apt-get update

# Installing Additional MySQL Products and Components - e.g. workbench
sudo apt-get install mysql-workbench-community

# Launch MySQL Workbench
mysql-workbench
