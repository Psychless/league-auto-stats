from Sheets.SheetsAPI import SheetBase
from Common.Constants import *
import Riot


class TeamSheet(SheetBase):
    def fill_empty_matches(self, riot_API):
        row_index: int = GAME_STAT_STARTING_ROW
        match_id: int
        print('Looking for unfilled games..')
        while True:
            row_string = str(row_index)
            row_values = self.get_row_values('A' + row_string + ':' + GAME_STAT_MATCH_ID_COL + row_string)
            game_result = self.get_row_cell_value(row_values, GAME_STAT_RESULT_COL)
            side = self.get_row_cell_value(row_values, GAME_STAT_SIDE_COL)

            # Match has 'side' cell filled
            if side:
                # Match is already filled
                if side and game_result:
                    row_index += 1
                    continue
                # Match is set and needs to be filled
                if side and not game_result:
                    match_id = self.get_row_cell_value(row_values, GAME_STAT_MATCH_ID_COL)
                    self.fill_match_stats(riot_API, match_id, row_values, row_string, side)
                    row_index += 1
                    continue
            else:
                print('All matches have been iterated')
                print('Total matches found - ' + str(row_index - int(GAME_STAT_STARTING_ROW)))
                break

    def fill_match_stats(self, riot_API, match_id: int, row_values: list, row_index, side: str):
        print('Filling match - %s' % match_id)
        match = riot_API.fetch_match(match_id)
        team_stats = Riot.get_team_stats(match, side)

        # Fill game's general info
        self.set_row_cell_value(row_values, GAME_STAT_GAME_TIME_FORMATTED_COL, Riot.format_game_duration(match['gameDuration']))
        self.set_row_cell_value(row_values, GAME_STAT_GAME_TIME_COL, match['gameDuration'])
        self.set_row_cell_value(row_values, GAME_STAT_RESULT_COL, RESULT_WIN if team_stats['win'] == 'Win' else RESULT_LOSE)
        self.set_row_values(row_values)
