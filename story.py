from flask import Flask, request
from twilio.rest import TwilioRestClient
from credentials import *
app = Flask(__name__)
app.debug = True


#games_list = {}
class GameRepository(object):
    def __init__(self):


class Partypants(object):
    def __init__(self, name, number, playing):
        self.name = name
        self.number = number
        self.playing = playing

class Game(object):
    def __init__(self, text, participants, game_id):
        self.participants = self.parse_participants(participants)
        self.text = text.split(' ')
        self.prompts = filter(lambda x: x[0] == '#', self.text)
        self.game_id = game_id

    def parse_participants(self, participants):
        # This is ugly
        parsed = []
        for e in participants:
            e = e.split(':')
            parsed.append(Partypants(e[0], e[1], False))
        return parsed

    def invite_players(self):
        #status_callback_url = 'http://robertqueenin.com:8765/callback/{}'.format(self.game_id)
        print self.game_id
        #print status_callback_url
        for player in self.participants:
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(body="Would you like to play a game? Y/N",
                    to=player.number,
                    from_=from_number)

    def update_user_agreement(self, number, message):
        # Is there a more elegant way to filter.
        user = [i for i in self.participants if i.number == number][0]
        if message.lower() in ['y', 'yes']:
            user.playing = True
            return True
        return False


@app.route('/')
def root():
    return '/story POST [text, participants]'

@app.route('/games', methods=['POST', 'GET'])
def create_game():
    print request.form
    print request.method
    if request.method == 'GET':
        return 'please POST\n'
    if request.method == 'POST':
        text = request.form['storytext']
        participants = request.values.getlist('participants')
        game_id = len(games_list) + 1
        game = Game(text, participants, game_id)
        games_list[game_id] = game
        game.invite_players()
        game.timer_start = #timestamp
        return 'text: {}\nparticipants: {}'.format(game.text, game.participants)

@app.route('/callback', methods=['POST', 'GET'])
def callback_endpoint():
    print 'from: {}, body:{}'.format(request.form['From'], request.form['Body'])
    number = request.form['From']
    message = request.form['Body']
    for game_id in games_list:
        game = games_list[game_id]
        for player in game.participants:
            if player.number == number:
                game.update_user_agreement(number, message)
    return 'barf'

def test_game_creation():
    game = Game('I like #flavor ice cream in #city', ['name1:1234', 'name2:9876'])
    assert game.participants == [('name1', '1234', False), ('name2', '9876', False)]
    assert game.text == ['I', 'like', '#flavor', 'ice', 'cream', 'in', '#city']
    assert game.prompts == ['#flavor', '#city']

@app.route('/twilio_test')
#nm, pretend to be the twilio callback
def twilio_test():
    return twilio_test()

def twilio_test():
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Hi, this is a test of the emergency barf system",
            to="+14158598214",
            from_=from_number)
    return message.sid


if __name__ == '__main__':
    app.run(host='robertqueenin.com', port=8765)
