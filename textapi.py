# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACe6503bfc0d90a64215a333f39811c674'
auth_token = '30c9ce5a4b8d6aa4ec5188e45113b1b4'
client = Client(account_sid, auth_token)

def sendMessage(msg_text):
    message = client.messages \
                    .create(
                        body=msg_text,
                        from_='+19895147904',
                        to='+17347305966'
                    )

    print(message.sid)