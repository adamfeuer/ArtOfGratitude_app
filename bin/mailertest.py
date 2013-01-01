#!/usr/bin/env python

from mailer import Mailer
from mailer import Message

message = Message(From="adam@adamfeuer.com",
                  To="adamfeuer@gmail.com")
message.Subject = "HTML email test"
message.Html = """<form method="post" action="http://localhost:8080/profile-landing/adamf">
<div style="display:none">
<input type="hidden" value="HWPLvPOA67CRib6bfQyinrlUwH1Kmeqy" name="csrfmiddlewaretoken">
</div>
<p>
<label for="id_text">Type in your gratitude for today:</label>
<input id="id_text" type="text" maxlength="5000" name="text" value="I am grateful for...">
</p>
</form>"""

sender = Mailer('mailout.easydns.com', usr='adamfeuer.com', pwd='b8PnU7HXD1f25D0m9V7478029n4hL6')
sender.send(message)
