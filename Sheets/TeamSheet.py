from Sheets.SheetsAPI import SheetBase
from Common.Constants import *
import Riot


class TeamSheet(SheetBase):
    def fill_empty_matches(self, riot_API):
        filled_match_count = 0
        row_index: int = GAME_STAT_STARTING_ROW
        match_id: int
        print('Looking for unfilled games..')
        while True:
            row_string = str(row_index)
            general_info_row = self.get_row_values('A' + row_string + ':' + COL_GAME_STAT_MATCH_ID + row_string)
            game_result = self.get_row_cell_value(general_info_row, COL_GAME_STAT_RESULT)
            side = self.get_row_cell_value(general_info_row, COL_GAME_STAT_SIDE)

            # Match has 'side' cell filled
            if side:
                # Match is already filled
                if side and game_result:
                    row_index += 1
                    continue
                # Match is set and needs to be filled
                if side and not game_result:
                    match_id = self.get_row_cell_value(general_info_row, COL_GAME_STAT_MATCH_ID)
                    self.fill_all_stats(riot_API, match_id, general_info_row, row_string, side)
                    filled_match_count += 1
                    row_index += 1
                    continue
            else:
                print('All matches have been iterated')
                print('Matches filled - ' + str(filled_match_count))
                break

    def fill_all_stats(self, riot_API, match_id: int, general_info_row: list, row_index, side: str):
        # Fetch stats from Riot
        print('Fetching match #' + str(match_id) + ' stats')
        match = riot_API.fetch_match(match_id)
        team_stats = Riot.get_team_stats(match, side)

        # Start filling spreadsheet
        print('Filling spreadsheet')
        self.fill_match_stats(match, team_stats, general_info_row)
        self.fill_player_stats(riot_API, side, match, team_stats, row_index)

        # Reset active spreadsheet to 'Game stats'
        self.worksheet = self.sheet.worksheet(WORKSHEET_GAME_STATS)

    # Fill game's general info
    def fill_match_stats(self, match, team_stats, general_info_row):
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_GAME_TIME_FORMATTED, Riot.format_game_duration(match['gameDuration']))
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_GAME_TIME, match['gameDuration'])
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_RESULT, RESULT_WIN if team_stats['win'] == 'Win' else RESULT_LOSE)
        self.set_row_values(general_info_row)

    # Fill all player stats
    def fill_player_stats(self, riot_API, side, match, team_stats, row_index):
        for i in range(0, 5):  # 0: top, 1: jungle.. etc.
            self.worksheet = self.sheet.worksheet(ROLE_WORKSHEETS[i])
            player = Riot.get_participant_by_index(match, side, i)
            champion = riot_API.fetch_champion(match, player['championId'])
