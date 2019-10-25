from Sheets.TeamSheet import TeamSheet
from Common.Constants import *
from Riot import RiotAPI
from datetime import datetime


def main():
    # Init
    startTime = datetime.now()
    riot_API = RiotAPI()

    team_sheet = TeamSheet(TEAM_SHEET_ID, WORKSHEET_GAME_STATS)
    team_sheet.fill_empty_matches(riot_API)

    # Execution time
    print('-----------------------------')
    print('Execution time - ' + str(datetime.now() - startTime))


if __name__ == "__main__":
    main()