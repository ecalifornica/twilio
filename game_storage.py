from pymongo import MongoClient
from twilio.rest import TwilioRestClient
from credentials import *
client = MongoClient()
import time

class Game(object):
    def __init__(self, text, participants, game_id=None):
        self.participants = self.parse_participants(participants)
        self.text = text.split(' ')
        self.prompts = filter(lambda x: x[0] == '#', self.text)
        self.game_id = game_id

    def parse_participants(self, participants):
        # This is ugly
        parsed = []
        for e in participants:
            e = e.split(':')
            #parsed.append(Partypants(e[0], e[1], False))
            parsed.append({'name': e[0], 'number': e[1], 'playing': False})
        return parsed

    def invite_players(self):
        #status_callback_url = 'http://robertqueenin.com:8765/callback/{}'.format(self.game_id)
        print self.game_id
        #print status_callback_url
        for player in self.participants:
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.create(body="Would you like to play a game? Y/N",
                    to=player['number'],
                    from_=from_number)

    def update_user_agreement(self, number, message):
        # Is there a more elegant way to filter.
        print('update user agreement method')
        user = [i for i in self.participants if i.number == number][0]
        if message.lower() in ['y', 'yes']:
            user['playing'] = True
            print('user: {}'.format(user))
            return True
        return False

class GameStore(object):
    def __init__(self):
        self.db = client.test_madlibs
        self.games = self.db.games

    def get_game(self, game_id):
        #
        game_as_dict = self.games.find_one('game_id')
        text = game_as_dict['text']
        participants = game_as_dict['participants']
        game = Game(text, participants, game_id)
        return game

    def insert_game(self, game):
        game_as_dict = game.__dict__
        insert_id = self.games.insert(game_as_dict)

    def save_game(self, game):
        insert_id = self.games.save(game)

    def list_games(self):
        all_games = []
        for game in self.games.find():
            all_games.append(game)
        return all_games

    def find_games_done_verifying(self):
        return self.games.find({'start_time': {'$lt': time.time()}, 'state': 'verification'})
