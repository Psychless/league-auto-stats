import math
import time
from riotwatcher import RiotWatcher
from Common.Constants import *


def get_team_stats(match: dict, side: str):
    return match['teams'][0 if side == 'B' else 1]


def get_opponent_team_stats(match: dict, side: str):
    opponent_side = 'R' if side == 'B' else 'B'
    return get_team_stats(match, opponent_side)


def format_game_duration(game_duration: int):
    return time.strftime('%M.%S', time.gmtime(game_duration))


class RiotAPI:
    def __init__(self):
        print('Starting up Riot API')
        self.watcher = RiotWatcher(API_KEY)
        print('Riot API - RUNNING')

    def fetch_match(self, match_id: int):
        return self.watcher.match.by_id(REGION, match_id)
