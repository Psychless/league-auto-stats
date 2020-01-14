from Sheets.SheetsAPI import SheetBase
from Common.Constants import *
import Riot
import time

class TeamSheet(SheetBase):
    ROLE_INDEX = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4
    }

    def fill_empty_matches(self, riot_API):
        filled_match_count = 0
        row_index: int = GAME_STAT_STARTING_ROW
        match_id: int
        print('Looking for unfilled games..')
        while True:
            row_string = str(row_index)
            general_info_row = self.get_row_values('A' + row_string + ':' + COL_GAME_STAT_LAST_COL + row_string)
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
                    if filled_match_count > 0:
                        print('Waiting 100 seconds for API quota')
                        time.sleep(100)

                    # Fetch match ID and role indexes
                    match_id = self.get_row_cell_value(general_info_row, COL_GAME_STAT_MATCH_ID)
                    self.ROLE_INDEX[0] = int(self.get_row_cell_value(general_info_row, COL_GAME_STAT_TOP_INDEX))
                    self.ROLE_INDEX[1] = int(self.get_row_cell_value(general_info_row, COL_GAME_STAT_JGL_INDEX))
                    self.ROLE_INDEX[2] = int(self.get_row_cell_value(general_info_row, COL_GAME_STAT_MID_INDEX))
                    self.ROLE_INDEX[3] = int(self.get_row_cell_value(general_info_row, COL_GAME_STAT_ADC_INDEX))
                    self.ROLE_INDEX[4] = int(self.get_row_cell_value(general_info_row, COL_GAME_STAT_SUP_INDEX))

                    # Start stat fill
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
        print('Filling general match stats')
        self.fill_match_stats(match, team_stats, general_info_row)
        print('General match stats - DONE')

        print('Filling player stats')
        self.fill_player_stats(riot_API, side, match, team_stats, row_index)
        print('Player stats - DONE')

        # Reset active spreadsheet to 'Game stats'
        self.worksheet = self.sheet.worksheet(WORKSHEET_GAME_STATS)

        print('Match #' + str(match_id) + ' - DONE')

    # Fill game's general info
    def fill_match_stats(self, match, team_stats, general_info_row):
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_GAME_TIME_FORMATTED, Riot.format_game_duration(match['gameDuration']))
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_GAME_TIME, match['gameDuration'])
        self.set_row_cell_value(general_info_row, COL_GAME_STAT_RESULT, RESULT_WIN if team_stats['win'] == 'Win' else RESULT_LOSE)
        self.set_row_values(general_info_row)

    # Fill all player stats
    def fill_player_stats(self, riot_API, side, match, team_stats, row_index):
        row = str(row_index)  # Used for cell range
        for i in range(0, 5):  # 0: top, 1: jungle.. etc.
            print('- player #' + str(i + 1))
            self.worksheet = self.sheet.worksheet(ROLE_WORKSHEETS[i])
            participant_index = self.ROLE_INDEX[i] - 1  # Subtract 1 since end-users don't start counting from 0 like us nerds do
            player = Riot.get_participant_by_index(match, side, participant_index)
            player_stats = player['stats']
            champion = riot_API.fetch_champion(match, player['championId'])

            self.set_cell_value(COL_PLAYER_STAT_CHAMPION_NAME + row, champion['name'])
            self.set_cell_value(COL_PLAYER_STAT_KILLS + row, player_stats['kills'])
            self.set_cell_value(COL_PLAYER_STAT_DEATHS + row, player_stats['deaths'])
            self.set_cell_value(COL_PLAYER_STAT_ASSISTS + row, player_stats['assists'])
            self.set_cell_value(COL_PLAYER_STAT_DMG_TO_CHAMPS + row, player_stats['totalDamageDealtToChampions'])
            self.set_cell_value(COL_PLAYER_STAT_DMG_TAKEN + row, player_stats['totalDamageTaken'])
            self.set_cell_value(COL_PLAYER_STAT_WARDS_PLACED + row, player_stats['wardsPlaced'])
            self.set_cell_value(COL_PLAYER_STAT_WARDS_DESTROYED + row, player_stats['wardsKilled'])
            self.set_cell_value(COL_PLAYER_STAT_WARDS_BOUGHT + row, player_stats['visionWardsBoughtInGame'])
            self.set_cell_value(COL_PLAYER_STAT_VISION_SCORE + row, player_stats['visionScore'])
            self.set_cell_value(COL_PLAYER_STAT_CREEP_SCORE + row, player_stats['totalMinionsKilled'] + player_stats['neutralMinionsKilled'])
            self.set_cell_value(COL_PLAYER_STAT_GOLD_EARNED + row, player_stats['goldEarned'])
