from dataclasses import dataclass
import math

@dataclass
class Match:
    """Match DTO object that contains all match data including summoner match stats"""
    gameid: int
    game_duration: int
    game_duration_formatted: str

    def __init__(self, match_id: int):
        self.gameid = match_id

    def format_game_duration(self):
        minutes = int(math.floor(self.game_duration / 60))
        seconds = self.game_duration % 60
        self.game_duration_formatted = '%(minutes)s.%(seconds)s' % {'minutes': minutes, "seconds": seconds}
