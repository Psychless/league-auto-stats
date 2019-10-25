from Sheets.TeamSheet import TeamSheet


def main():
    team_sheet = TeamSheet()
    foo = team_sheet.get_game_stat_cell_val('G9')
    team_sheet.fill_empty_matches()

if __name__ == "__main__":
    main()