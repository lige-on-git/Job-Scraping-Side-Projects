#!/bin/bash
# change the database storage to an attached disk
# https://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory

# stop mysql service
sudo service $(cd /etc/init.d; grep -l mysql *) stop
sudo service $(cd /etc/init.d; grep -l mysql *) status

# copy (recursively and preserve current setting) the existing data directory (default located in /var/lib/mysql) to a new directory
sudo cp -R -p /var/lib/mysql /media/lige/Samsung2TB/MySQL-DB-Storage

# REMOVE COMMENT & then replace old data directory to new data directory in the MySQL configuration
# old: /var/lib/mysql
# new: /media/lige/Samsung2TB/MySQL-DB-Storage/mysql
sudo gedit /etc/mysql/mysql.conf.d/mysqld.cnf

# change MySQL alias in the apparmor access control
sudo gedit /etc/apparmor.d/tunables/alias  # add a new line: "alias /var/lib/mysql/ -> /media/lige/Samsung2TB/MySQL-DB-Storage/mysql,"

# restart apparmor access control and mysql service
sudo service apparmor restart
sudo service $(cd /etc/init.d; grep -l mysql *) restart
sudo service $(cd /etc/init.d; grep -l mysql *) status

### unfortunately this script doesn't work. failed to point to the new directory
### in the meantime "AppArmor parser error for /etc/apparmor.d/usr.sbin.mysqld" has appeared.
### but can still restart mysql server after revert to the old directory
### try to solve this after exams (don't waste time right now); if can't resolve, then recover to 8-03 system backup...
