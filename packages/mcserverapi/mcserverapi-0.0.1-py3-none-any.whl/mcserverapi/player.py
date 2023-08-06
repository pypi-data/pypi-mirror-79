import requests
import json


class Player:
    cache = {}

    def __init__(self, player=None, uuid=None):
        if player and uuid:
            pass
        elif uuid:
            player = self.get_player(uuid)
        elif player:
            uuid = self.get_uuid(player)
        else:
            raise ValueError('class Player needs either a player username or uuid to initialize.')
        self.player = player
        self.uuid = uuid

    def get_player(self, uuid):
        if uuid in self.cache.values():
            return {v:k for k,v in self.cache.items()}[uuid]
        api = 'https://api.mojang.com/user/profiles/%s/names' % uuid
        try:
            response = requests.get(api).json()
            if 'error' in response and 'errorMessage' in response:
                ResponseError = type(response['error'], tuple([Exception]), {})
                raise ResponseError(response['errorMessage'])
            self.cache[response[-1]['name']] = uuid
            return response[-1]['name']
        except json.decoder.JSONDecodeError:
            raise ValueError('No players exist with uuid, {}, according to Mojang.'.format(uuid))

    def get_uuid(self, player):
        if player in self.cache:
            return self.cache[player]

        api = 'https://api.mojang.com/users/profiles/minecraft/%s' % player
        try:
            response = requests.get(api).json()
            if 'error' in response and 'errorMessage' in response:
                ResponseError = type(response['error'], tuple([Exception]), {})
                raise ResponseError(response['errorMessage'])
            self.cache[player] = response['id']
            return response['id']
        except json.decoder.JSONDecodeError:
            raise ValueError('Player {} Doesn\'t exist, according to Mojang.'.format(player))

    def __repr__(self):
        return '<Player {}:{}>'.format(self.player, self.uuid)