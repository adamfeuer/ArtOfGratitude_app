#!/usr/bin/env python

from mailer import Mailer
from mailer import Message

toAddress='adamfeuer@gmail.com'

smtpServer='email-smtp.us-east-1.amazonaws.com'
user='AKIAIBJGVZ52BWW3V7XQ'
password='AgyFiq9cDPEKj87cYcUUVr4aEkINzoXjGavnyIoA5w2l'
fromAddress='team@artofgratitude.com'

message = Message(From=fromAddress,
                  To=toAddress)
message.Subject = "HTML email test - prod"
message.Html = """<form method="post" action="http://artofgratitude.com/app/profile-landing/adamf">
<p>
<label for="id_text">Type in your gratitude for today (start with "I am grateful for..."):</label>
<input id="id_text" type="text" maxlength="5000" name="text">
</p>
</form>"""

sender = Mailer(smtpServer, usr=user, pwd=password, use_tls=True)
sender.send(message)
