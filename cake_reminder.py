#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from datetime import datetime as dt
import sqlite3
import time
import os

text = """Liebe/r {name},

wir wünschen Dir alles Gute zu deinem Geburtstag und freuen uns schon darauf, den Geburtstag demnächst mit einem Kuchen zu feiern. :)

Liebe Grüße,
Deine Astroteilchenphysiker


Dear {name},

we congratulate you to your birthday and look forward to celebrating this with a cake in the near future. :)

Kind regards,
Your astro particle physicists"""


def compose_mail(name, to_addr):
    msg = MIMEMultipart()
    msg['To'] = to_addr
    msg['From'] = formataddr(('Cake Reminder',
                             'atp-bbq-owner@listserv.uni-tuebingen.de'))
    msg['Subject'] = Header('Geburtstagsgrüße', 'utf-8')

    msg.attach(MIMEText(text.format(name=name), _charset='utf-8'))

    s = smtplib.SMTP('smtpserv.uni-tuebingen.de')
    s.sendmail('Cake Reminder', [to_addr], msg.as_string())


def check_bdays():
    now = dt.now()
    conn = sqlite3.connect('birthdays.db')
    c = conn.cursor()

    now_md = '____-{:02d}-{:02d}'.format(now.month, now.day)
    now_ymd = '{:04d}-{:02d}-{:02d}'.format(now.year, now.month, now.day)
    c.execute("select rowid, name, email, last_cake from birthdays where birthday like '{date}'".format(date=now_md))
    for tup in c.fetchall():
        rowid, name, email, last_cake = tup
        if last_cake != now_ymd:
            compose_mail(name, email)
            compose_mail(name, 'atp-bbq-owner@listserv.uni-tuebingen.de')
            print('sent mail to {} with email address {}'.format(name, email))
            c.execute("update birthdays set last_cake='{date}' where rowid={rid}".format(date=now_ymd, rid=rowid))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    check_bdays()
