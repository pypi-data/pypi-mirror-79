#  discordstatus/discordstatus.py

import requests

project_name = 'DiscordStatus'
user_agent = f'{project_name}/1.0'


class DiscordStatus():
    def __init__(self):
        self.base_target = 'https://srhpyqt94yxb.statuspage.io/api/v2'

    @property
    def summary(self):
        return self.get('summary')

    @property
    def status(self):
        return self.get('status')

    @property
    def components(self):
        return self.get('components')

    @property
    def unresolved_incidents(self):
        return self.get('incidents/unresolved')

    @property
    def all_incidents(self):
        return self.get('incidents')

    @property
    def upcoming_maintenances(self):
        return self.get('scheduled-maintenances/upcoming')

    @property
    def active_maintenances(self):
        return self.get('scheduled-maintenances/active')

    @property
    def all_maintenances(self):
        return self.get('scheduled-maintenances')

    def get(self, target: str = None, force: bool = False):
        if not target:
            raise ValueError('No target given')
        resp = requests.get(f'{self.base_target}/{target}.json', headers={'User-Agent': user_agent})
        return resp.json()
