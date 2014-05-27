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
        if 'make_call' in posted_data.keys():
            call = client.calls.create(url="http://blametommy.com:5050/callxml/",
                    to="+14158598214",
                    from_=credentials.from_number)
            logger.debug(call.sid)
            return flask.redirect('/twilio/')

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
    resp.say('please rechord words for these prompts:')
    '''
    for word in game.word_list:
        resp.say(word)
        resp.record(maxLength="2", action="/handle-recording/")
    '''
    resp.say('noun')
    resp.record(maxLength="2", action="/handle-recording/")
    resp.say('verb')
    resp.record(maxLength="2", action="/handle-recording/")
        
    #resp.say("Please rechord a NOUN.")
    #resp.say("Hi Sarah, this is a test of the computer swearing system. Fuck. Shit. Barf. Cocksucker. Motherfucker. Record your own swearword after the beep")
    #resp.record(maxLength="2", action="/handle-recording/")
    resp.say('thank you. I will text you the finished game U R L')
    return str(resp)

@app.route('/handle-recording/', methods=['GET', 'POST'])
def handle_recording():
    logger.debug(flask.request.form)
    recording_url = flask.request.values.get("RecordingUrl", None)
    #game.recording_urls.save({'dunno': recording_url})
    resp = twiml.Response()
    #resp.say("You sounded like:")
    resp.play(recording_url)
    logger.debug(recording_url)
    resp.redirect(url="/callxml/")
    #resp.say("Tee-hee, you're so naughty.")
    print str(resp)
    return str(resp)

class madLibGame(object):
    def __init__(self):
        import time
        self.game_id = int(time.time())
        print self.game_id
        self.game_url = None
        #self.word_list = [{'noun': None}, {'verb': None}, {'adjective', None}, {'noun': None}]
        self.word_list = ['noun', 'verb', 'adjective', 'ice cream flavor', 'animal']
        self.datastore = dbclient['{}'.format(self.game_id)]
        self.recording_urls = self.datastore['recording_urls']
        #self.recording_urls.remove({'test': 'value'})
        #for x in self.datastore.find():
        #    print x
        print self.datastore.collection_names()
        self.player_numbers = db.phone_numbers
        print db.collection_names()
        print 'object initialized'

    def start_new_game(self):
        pass


game = madLibGame()

@app.route('/object_test/', methods=['GET', 'POST'])
def testing():
    #print game.player_numbers
    for player in game.player_numbers.find():
        print('{}: {}'.format(player['name'], player['number']))
    return 'hello test'
    

@app.route('/call/', methods=['GET', 'POST'])
def call():
    call = client.calls.create(url="http://blametommy.com:5050/callxml/",
            to="+14158598214",
            from_=credentials.from_number)
    logger.debug(call.sid)
    return 'barf'


if __name__ == '__main__':
	app.run(debug=True, host="blametommy.com", port=5050)
