#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created 2012-01-12 by Zhangmh - mail.charlesf@gmail.com
Env Python 2.4.3
Use 139 E-mail SMS alarm monitoring the DB the Subordinate synchronization
'''
import os
import sys
import string
import smtplib
import MySQLdb.cursors
mymail="Monitor@2345.com"
myphone="158XXXXXXXX@139.com" ##你的手机号码
sql={}
def notice_email(FROM,TO,SUBJECT,TEXT):
                        text=TEXT
                        SUBJECT = SUBJECT
                        TO = TO
                        FROM = FROM
                        BODY = string.join((
                        "From: %s" % FROM,
                        "To: %s" % TO,
                        "Subject: %s" % SUBJECT ,
                        "",
                        text
                        ), "\r\n")
                        server = smtplib.SMTP('mx1.mail.139.com')
                        server.sendmail(FROM, [TO], BODY)
#mx1.mail.139.com by use 
#dig @8.8.8.8 139.com mx
def check_mysql_subordinate ():
                global sql
                host=["10.0.0.23","10.0.0.24","10.0.0.25"]
                ####23,24,25 是我的Subordinate DB IP
                for hosts in host:
                        try:
                                conn=MySQLdb.connect(host=hosts,user="root",passwd="password",db="test",connect_timeout=3)
                                cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
                                cursor.execute("""
                                show subordinate status;
                                """)
                                sql=cursor.fetchall()
                                cursor.close ()
                                print hosts+" Mysql conn Suncess!"
                        except:
                                notice_email(mymail,myphone,hosts,hosts+" Mysql Conn Faild!")
                                print hosts+" Mysql conn Faild!"
                        for i in sql:
              
                                if i['Subordinate_IO_Running'] == "Yes" and i['Subordinate_SQL_Running'] == "Yes":

                                        print hosts+" DB subordinate Running OK"

                                else:
                                        notice_email(mymail,myphone,hosts,hosts+" Mysql Subordinate Stop....!")

if __name__ == "__main__":
        check_mysql_subordinate()
