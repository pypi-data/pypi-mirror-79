import json
import os
import subprocess
import atexit
import sys


class Server:
    def __init__(self, jar_path: str, min_RAM: str = '1G', max_RAM: str = '3G'):
        self.max_RAM = max_RAM
        self.min_RAM = min_RAM
        self.jar = jar_path

        self.process = None

        self.abs_cwd, self.jar = os.path.split(self.jar)
        if not os.path.isabs(self.abs_cwd):
            self.abs_cwd = os.path.join(os.getcwd(), self.abs_cwd)

        file = open(os.path.join(self.abs_cwd, 'temp-log.txt'), 'a+')
        atexit.register(os.remove, os.path.join(self.abs_cwd, 'temp-log.txt'))

        self.stdout = file
        self.sterr = file
        self.stdin = sys.stdin

    def online(self):
        return True if self.process.returncode is None else False

    def run(self):
        if (not os.path.isfile(os.path.join(self.abs_cwd, self.jar))) or (not self.jar.endswith('.jar')):
            raise OSError('{} is not a jar file.'.format(self.jar))

        # noinspection PyTypeChecker
        self.process = subprocess.Popen(
            ' '.join(['java', f'-Xms{self.min_RAM}', f'-Xmx{self.max_RAM}', '-jar', self.jar, 'nogui']),
            cwd=self.abs_cwd,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.sterr,
            shell=True
        )

        atexit.register(self.process.terminate)

    def _exec_cmd(self, cmd, *params):
        if not self.online:
            raise OSError('Server isn\'t started yet.')
        stdout, stderr = self.process.communicate(' '.join([cmd, *params]))
        return stdout, stderr

    def hardstop(self):
        self.process.terminate()

    # Commands
    def run_cmd(self, *args):
        return self._exec_cmd(*args)

    def op(self):
        pass

    def deop(self):
        pass

    # Server Folder Analysis
    @property
    def properties(self):
        with open(os.path.join(self.abs_cwd, 'server.properties'), 'r') as file:
            lines = file.readlines()
        properties = {}
        for line in lines:
            if not line.startswith('#'):
                k, v = line.split('=')
                properties[k] = v
        return properties

    @properties.setter
    def properties(self, properties: dict):
        with open(os.path.join(self.abs_cwd, 'server.properties'), 'w') as file:
            properties = ['='.join(item) for item in properties.items()]
            file.writelines(properties)

    @property
    def banned_ips(self):
        with open(os.path.join(self.abs_cwd, 'banned-ips.json'), 'r') as file:
            banned_ips = json.load(file)
        return banned_ips

    @property
    def banned_players(self):
        with open(os.path.join(self.abs_cwd, 'banned-players.json'), 'r') as file:
            banned_players = json.load(file)
        return banned_players

    @property
    def ops(self):
        with open(os.path.join(self.abs_cwd, 'ops.json'), 'r') as file:
            ops = json.load(file)
        return ops



