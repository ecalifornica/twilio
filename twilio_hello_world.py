from twilio.rest import TwilioRestClient
import twilio.twiml
account_sid = ""
auth_token = ""
client = TwilioRestClient(account_sid, auth_token)
msg = 'hi'
to = '+14155551212'
from_number = '+14155551212'
message = client.messages.create(body=msg, to=to, from_=from_number)
