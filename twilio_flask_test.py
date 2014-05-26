#from flask import Flask, request
import logging
import re
import flask
import twilio
from twilio.rest import TwilioRestClient
import twilio.twiml as twiml
import credentials
import pymongo
app = flask.Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('madlib.log')
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.debug('\nProgram start')

dbclient = pymongo.MongoClient()
db = dbclient.twilio_hello_world
players = db.players

account_sid = credentials.account_sid
auth_token = credentials.auth_token
client = TwilioRestClient(account_sid, auth_token)
from_number = credentials.from_number
msg = ''
to = ''
# message = client.messages.create(body=msg, to=to, from_=from_number)


@app.route('/twilio/', methods=['GET', 'POST'])
def twilio():
    participants = []
    if flask.request.method == 'POST':
        logger.debug(flask.request.form)
        posted_data = flask.request.form
        if 'From' in posted_data.keys():
            number = posted_data['From']
            message = posted_data['Body'].lower()
            logger.debug('message: {}'.format(message))
            '''
            else:
                submitted_string = flask.request.form['to_number_text']
            '''
            number = re.sub("[^0-9]", "", number)
            if len(number) < 10:
                print 'less than ten digits'
                return 'number not recognized'
            elif len(number) == 11 and number[0] == '1':
                number = '+' + number
            elif len(number) == 10:
                number = '+1' + number
            else:
                print 'some sort of error'
                return 'number not recognized'
            number = {'number': number}
            if players.find_one(number) is None:
                logger.debug('player not found in db')
                logger.debug(players.insert(number))
                player = players.find_one(number)
            else:
                logger.debug('already in db')
                player = players.find_one(number)
                logger.debug('player found: {}'.format(player))
                if message in ('y', 'yes', 'yeah'):
                    logger.debug('player agreed to game')
                    player['playing'] = True
                    logger.debug(player)
                    logger.debug('update: {}'.format(players.save(player)))
            '''
            for player in players.find():
                logger.debug('player: {}'.format(player))
                if player['playing']:
                    participants.append(player['number'])
            logger.debug(participants)
            '''
    else:
        pass
    return flask.render_template('twilio.html', participants=participants)

@app.route('/callxml/', methods=['GET', 'POST'])
def barf():
    resp = twiml.Response()
    resp.say("Please rechord a NOUN.")
    resp.record(maxLength="5", action="/handle-recording/")
    return str(resp)

@app.route('/handle-recording/', methods=['GET', 'POST'])
def handle_recording():
    print('made it this far')
    recording_url = flask.request.values.get("RecordingUrl", None)
    resp = twiml.Response()
    resp.say("Thank you for recording a noun.")
    resp.play(recording_url)
    resp.say("Have a good night friend, I hope you sleep well.")
    return str(resp)



@app.route('/call/', methods=['GET', 'POST'])
def call():
    call = client.calls.create(url="http://blametommy.com:5050/callxml/",
            to="+14158598214",
            from_=credentials.from_number)
    logger.debug(call.sid)
    return 'barf'


if __name__ == '__main__':
	app.run(debug=True, host="blametommy.com", port=5050)
