import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetBase:
    def __init__(self, sheet_id, worksheet_name):
        print('Starting up Google sheets API')
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(sheet_id)
        self.worksheet = self.sheet.worksheet(worksheet_name)
        print('Google sheets API - RUNNING')

    def get_row_values(self, row_range: str):
        return self.worksheet.range(row_range)

    def set_row_values(self, cell_list):
        self.worksheet.update_cells(cell_list)

    def get_row_cell_value(self, cell_list: list, cell: str):
        return cell_list[self.get_col_index(cell)].value

    def set_row_cell_value(self, cell_list: list, cell: str, value):
        cell_list[self.get_col_index(cell)].value = value

    def get_cell_value(self, cell: str):
        return self.worksheet.acell(cell).value

    def set_cell_value(self, cell: str, value):
        self.worksheet.update_cell(cell, value)

    # Converts col referrencing letter to index
    # A -> 1, D -> 4 etc.
    def get_col_index(self, col: str):
        # -96 : ASCII
        # -1 : Starting from 0
        return ord(col.lower()) - 96 - 1
