import time
from flask import Flask, request, render_template
from twilio.rest import TwilioRestClient
from credentials import *
app = Flask(__name__)
app.debug = True
import game_storage
games_list = game_storage.GameStore()

@app.route('/')
def root():
    return '/story POST [text, participants]'

@app.route('/games/new')
def create_game_form():
    return render_template('game-new.html')

@app.route('/games', methods=['POST', 'GET'])
def create_game():
    #print request.form
    #print request.method
    if request.method == 'GET':
        return 'please POST\n'
    if request.method == 'POST':
        text = request.form['storyText']
        participants = request.values.getlist('participants')
        #
        #game_id = len(games_list) + 1
        #game = Game(text, participants, game_id)
        game = game_storage.Game(text, participants)
        #
        #games_list[game_id] = game
        game.start_time = time.time()
        game.state = 'verification'
        games_list.insert_game(game)
        game.invite_players()
        #game.timer_start = #timestamp
        return 'text: {}\nparticipants: {}'.format(game.text, game.participants)

@app.route('/phonecall', methods=['POST'])
def phonecall():
    resp = twiml.Response()
    resp.say('Woooooooo this worked. I want cookies! COOOOOKIES! COOOOKEEEESS!')



@app.route('/callback', methods=['POST', 'GET'])
def callback_endpoint():
    print 'from: {}, body:{}'.format(request.form['From'], request.form['Body'])
    number = request.form['From']
    message = request.form['Body']
    for game in games_list.list_games():
        for player in game['participants']:
            if player['number'] in number and message.lower() in ['y', 'yes']:
                player['playing'] = True
                games_list.save_game(game)

    #print games_list.list_games()
    for game in games_list.list_games():
        print game

    #for game_id in games_list:
        #game = games_list[game_id]

        '''        
        for player in game.participants:
            if player.number == number:
                game.update_user_agreement(number, message)
        '''
    return 'barf'

@app.route('/list_games')
def list_games():
    #print('all games: {}'.format(games_list.list_games()))
    for game in games_list.list_games():
        print game
    print('done verifying: ')
    for game in games_list.find_games_done_verifying():
        print game

    barf = ''
    '''
    for game in games_list.list_games():
        for i in game:
            barf += i
    '''
    return barf

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
