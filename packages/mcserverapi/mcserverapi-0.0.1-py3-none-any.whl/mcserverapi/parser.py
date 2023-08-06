import datetime
import threading
import atexit
import time
from typing import Union, Optional, List
from mcserverapi.player import Player
from mcserverapi.si import Server

class Event:
    def __init__(self, raw_event: str):
        self.raw = raw_event
        if self.raw.startswith('['):
            info = self.raw.replace('\n', '').split(': ')[0]
            message = self.raw.replace('\n', '').split(': ')[1:]
            self.message = ': '.join(message).replace('[', ' ').replace(']', '')
            time, self.process = info.replace('[', '').replace(']', '').split(' ')[0], ' '.join(
                info.replace('[', '').replace(']', '').split(' ')[1:])
            now = datetime.datetime.now()
            self.time = datetime.datetime(now.year, now.month, now.day, *[int(num) for num in time.split(':')])
        else:
            raise ValueError('Not a recognized event,', self.raw)

        self.type = self._event_type()

    def _event_type(self) -> Union[str, None]:
        msg_comps = self.message.split(' ')
        try:
            Player(msg_comps[0])  # Check if valid player from Mojang.
            if msg_comps[1] == 'left':
                return 'player_leave'
            elif msg_comps[1] == 'joined':
                return 'player_join'
            elif ' '.join(msg_comps[1:3]) == 'lost connection':
                return 'player_disconnect'
            elif msg_comps[1].startswith('/'):
                return 'player_connect'
        except ValueError:
            if ' '.join(msg_comps[0:3]) == 'Preparing spawn area':
                return 'spawn_prep'
            if msg_comps[0] == 'Done':
                return 'ready'
            if ' '.join(msg_comps[0:3]) == 'Can\'t keep up!':
                return 'ticks_behind'
            if ' '.join(msg_comps[0:6]) == 'Considering it to be crashed,':
                return 'crash'
            if msg_comps[0].startswith('<') and msg_comps[0].endswith('>'):
                try:
                    Player(msg_comps[0].replace('<', '').replace('>', ''))
                    return 'player_msg'
                except ValueError:
                    return str(None)


class Parser:
    def __init__(self, server: Server, cycle_length: int = 1):
        self._si = server
        self._cycle_length = cycle_length
        self._event_cache = {}

    def watch_for_events(self):
        while self._si.online:
            self.process_events(*self._si.process.stdout.readlines())
            print(self._event_cache)
            time.sleep(self._cycle_length)

    def process_events(self, *events):
        for raw_event in events:
            try:
                if raw_event not in self._event_cache:
                    print(raw_event)
                    self._event_cache[raw_event] = Event(raw_event)
                    for attr in self.__dict__:
                        if attr == 'on_' + self._event_cache[raw_event].type:
                            threading.Thread(target=self.__dict__[attr], args=[]).start()
            except Exception as err:
                self.on_parsing_error(err, raw_event)

    def on_ready(self, time, startup_time):
        print('ready')

    def on_spawn_prep(self, completion_percent: float):
        print('prep')

    def on_player_join(self, time, player):
        print('join')

    def on_player_connect(self, time, player):
        print('connect')

    def on_player_leave(self, time, player):
        print('leave')

    def on_player_disconnect(self, time, player):
        print('disconnect')

    def on_ticks_behind(self, time, ticks):
        print('behind')

    def on_command(self, time, command):
        print('command')

    def on_player_message(self, time, player, message):
        print('message')

    def on_crash(self):
        print('crashed')

    def on_parsing_error(self, err, raw_event):
        print(err.__class__.__name__, err, raw_event)
