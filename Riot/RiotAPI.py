from riotwatcher import RiotWatcher
from Riot.RiotConsts import *
from DTO.Match import Match

def fetch_match_stats(match: Match):
    watcher = RiotWatcher(API_KEY)
    match_JSON = watcher.match.by_id(REGION, match.gameid)

    # Game's duration
    match.game_duration = match_JSON['gameDuration']
    match.format_game_duration()