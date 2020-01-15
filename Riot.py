import time
import urllib.request
import json
from riotwatcher import RiotWatcher
from Common.Constants import *


def get_team_stats(match: dict, side: str):
    return match['teams'][0 if side == 'B' else 1]


def get_opponent_team_stats(match: dict, side: str):
    opponent_side = 'R' if side == 'B' else 'B'
    return get_team_stats(match, opponent_side)


def get_participant_by_index(match: dict, side: str, index: int):
    index += 0 if side == 'B' else 5  # Red team's player indexes are offset by 5
    return match['participants'][index]


def format_game_duration(game_duration: int):
    return time.strftime('%M.%S', time.gmtime(game_duration))


class RiotAPI:
    def __init__(self):
        print('Starting up Riot API')
        self.watcher = RiotWatcher(API_KEY)
        self.dd_champ_version = self.watcher.data_dragon.versions_for_region(REGION_DATA_DRAGON)['n']['champion']
        self.champion_json = self.watcher.data_dragon.champions(self.dd_champ_version)
        self.queue_json = json.loads(urllib.request.urlopen("http://static.developer.riotgames.com/docs/lol/queues.json").read())
        print('Riot API - RUNNING')

    def fetch_match(self, match_id: int):
        return self.watcher.match.by_id(REGION, match_id)

    def fetch_champion(self, match, champ_key: str):
        champion = None

        for k, v in self.champion_json['data'].items():
            if v['key'] == str(champ_key):
                champion = v
                break

        return champion

    def find_queue_by_id(self, queue_id):
        for q in self.queue_json:
            if q['queueId'] == queue_id:
                return q

        return None

    def is_queue_flex(self, match):
        queue_id = match['queueId']
        queue = self.find_queue_by_id(queue_id)
        queue_name = queue['description'] if queue['description'] is not None else ''

        return '5v5' in queue_name and 'Flex' in queue_name
