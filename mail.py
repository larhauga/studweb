#!/usr/bin/env python
#-*-coding: utf-8 -*-

import smtplib
import config
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart

class mail:
    """ Sending email notifications
    """

    def __init__(self):
        self.smtpserver  = config.SMTP_SERVER
        self.smtpport    = config.SMTP_PORT
        self.smtpuser    = config.SMTP_USERNAME
        self.smtppsw     = config.SMTP_PASSWORD

    def notify(self, text, title):
        msg = self.gen_msg(title, text)
        mail = smtplib.SMTP(self.smtpserver, self.smtpport)
        mail.starttls()

        try:
            mail.login(self.smtpuser, self.smtppsw)
        except smtplib.SMTPAuthenticationError as err:
            print("Authentication error %s" % (err.message))
        except:
            print("Error while logging into %s on %s" % (self.smtpserver, self.smtpport))

        try:
            mail.sendmail(config.EMAIL_FROM, config.EMAIL_TO, msg.as_string())
        except:
            print("Could not send email. An error occured")

    def gen_msg(self, subject, data):
        msg = MIMEMultipart(data)
        msg['Subject']  = subject
        msg['To']       = config.EMAIL_TO
        msg['From']     = config.EMAIL_FROM
        msg.attach(MIMEText(data, 'plain'))
        return msg
