#!/usr/bin/env python

from mailer import Mailer
from mailer import Message

message = Message(From="adam@adamfeuer.com",
                  To="adamfeuer@gmail.com")
message.Subject = "HTML email test - dev"
message.Html = """<form method="post" action="http://localhost:8080/profile-landing/adamf">
<p>
<label for="id_text">Type in your gratitude for today (start with "I am grateful for..."):</label>
<input id="id_text" type="text" maxlength="5000" name="text">
</p>
</form>"""

sender = Mailer('mailout.easydns.com', usr='adamfeuer.com', pwd='b8PnU7HXD1f25D0m9V7478029n4hL6')
sender.send(message)
