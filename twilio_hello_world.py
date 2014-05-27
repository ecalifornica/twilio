from twilio.rest import TwilioRestClient
import twilio.twiml
import credentials
account_sid = credentials.account_sid
auth_token = credentials.auth_token
client = TwilioRestClient(account_sid, auth_token)
msg = 'hi'
to = '+14158598214'
from_number = credentials.from_number
message = client.messages.create(body=msg, to=to, from_=from_number)
