import math
import time
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
        print('Riot API - RUNNING')

    def fetch_match(self, match_id: int):
        return self.watcher.match.by_id(REGION, match_id)

    def fetch_champion(self, match, champ_key: str):
        dd_champ_version = self.watcher.data_dragon.versions_for_region('euw')['n']['champion']
        champion_json = self.watcher.data_dragon.champions(dd_champ_version)
        champion = None

        for k, v in champion_json['data'].items():
            if v['key'] == str(champ_key):
                champion = v
                break

        return champion
