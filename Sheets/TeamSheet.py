from Sheets.SheetsAPI import SheetBase
from Common.Constants import *


class TeamSheet(SheetBase):
    def fill_empty_matches(self):
        row: int = GAME_STAT_STARTING_ROW
        match_id: int
        while True:
            cell_row = str(row)
            game_result = self.get_game_stat_cell_val(GAME_STAT_RESULT_COL + cell_row)
            side = self.get_game_stat_cell_val(GAME_STAT_SIDE_COL + cell_row)

            # Match has 'side' cell filled
            if side:
                # Match is already filled
                if side and game_result:
                    row += 1
                    continue
                # Match is set and needs to be filled
                if side and not game_result:
                    match_id = int(self.get_game_stat_cell_val(GAME_STAT_MATCH_ID_COL + cell_row))
                    self.fill_match_stats(match_id, row)
                    row += 1
                    continue
            else:
                print('All matches have been iterated')
                print('Total matches found - ' + str(row - int(GAME_STAT_STARTING_ROW)))
                break

    def fill_match_stats(self, match_id, row):
        # TODO: Start match filling here
        print('Found unfilled match - %s' % match_id)

    def get_game_stat_cell_val(self, cell: str) -> str:
        return self.get_cell_value(TEAM_SHEET_ID, SHEET_GAME_STATS, cell)
