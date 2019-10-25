import math
from riotwatcher import RiotWatcher
from Common.Constants import *


def fetch_match(match_id:int):
    watcher = RiotWatcher(API_KEY)
    return watcher.match.by_id(REGION, match_id)


def format_game_duration(game_duration:int):
    minutes = int(math.floor(game_duration / 60))
    seconds = game_duration % 60
    return '%(minutes)s.%(seconds)s' % {'minutes': minutes, "seconds": seconds}
