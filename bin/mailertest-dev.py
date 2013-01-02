#!/usr/bin/env python

from mailer import Mailer
from mailer import Message

toAddress='adamfeuer@gmail.com'

smtpServer='mailout.easydns.com'
user='adamfeuer.com'
password='b8PnU7HXD1f25D0m9V7478029n4hL6'
fromAddress='adam@adamfeuer.com'

message = Message(From=fromAddress,
                  To=toAddress)
message.Subject = "HTML email test - dev"
message.Html = """<form method="post" action="http://artofgratitude.com/app/profile-landing/adamf">
<p>
<label for="id_text">Type in your gratitude for today (start with "I am grateful for..."):</label>
<input id="id_text" type="text" maxlength="5000" name="text">
</p>
</form>"""

sender = Mailer(smtpServer, usr=user, pwd=password, use_tls=True)
sender.send(message)
