#Use:
#add crontab list 

MAILTO=""
*/1 * * * * * /usr/bin/python mysql_check.py
