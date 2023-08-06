import os
# GSheets Connection imports
import pickle

from discord.ext import commands
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from syncademy.config import config

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config.get('gsheets', 'spreadsheet_id')
WIDTH_OFFSET = config.getint('gsheets', 'width_offset')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class GoogleSheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.signup_translation_map = dict(
            tank='=Bot_DB!$A$1',
            healer='=Bot_DB!$B$1',
            melee='=Bot_DB!$C$1',
            ranged='=Bot_DB!$D$1',
            caster='=Bot_DB!$E$1',
            big_tank='=Bot_DB!$A$2',
            big_healer='=Bot_DB!$B$2',
            big_dps='=Bot_DB!$C$2'
        )

    @commands.command(name='connect2gs', help='Connect to GSheets', hidden='True')
    @commands.has_role('Faculty Member')
    async def connect2google(self, ctx):
        self.create_service(config.get('gsheets', 'credentials_json'),
                            config.get('gsheets', 'gsheets_api_service_name', fallback='sheets'),
                            config.get('gsheets', 'gsheets_api_version', fallback='v4'),
                            [config.get('gsheets', 'scope', fallback='https://www.googleapis.com/auth/spreadsheets')])
        await ctx.send('Connected to the Google Sheet!')

    def signup_to_values(self, signup):
        return [  # '',
            # '',
            # self.signup_translation_map['big_tank'] if signup.isTank else '',
            # self.signup_translation_map['big_healer'] if signup.isHealer else '',
            # self.signup_translation_map['big_dps'] if signup.isDps else '',
            self.signup_translation_map['tank'] if signup.isTank else '',
            self.signup_translation_map['healer'] if signup.isHealer else '',
            self.signup_translation_map['melee'] if signup.isMelee else '',
            self.signup_translation_map['ranged'] if signup.isRanged else '',
            self.signup_translation_map['caster'] if signup.isCaster else '',
            signup.student.discord_nickname]

    def export_data_to_sheets(self, course):
        sheet_name = config.get('gsheets', 'sheet_name')
        current_col = config.getint('gsheets', 'first_col_index', fallback=1)  # A=1, B=2, ...
        current_row = config.getint('gsheets', 'first_row', fallback=1)
        current_clear_col = config.getint('gsheets', 'first_col_index', fallback=1)  # A=1, B=2, ...
        current_clear_row = config.getint('gsheets', 'first_row', fallback=1)
        current_end_clear_col = config.getint('gsheets', 'first_col_index', fallback=1)
        current_end_clear_col += config.getint('gsheets', 'clear_width', fallback=5)  # A=1, B=2, ...
        current_end_clear_row = None

        clear_ranges = []

        course_array_form = []
        for timeslot in course.timeslots:
            timeslot_array_form = []
            counter = 0
            if timeslot.signups:  # if timeslot has signups
                for signup in timeslot.signups:
                    signup_array_form = self.signup_to_values(signup)
                    timeslot_array_form.append(signup_array_form)
                    counter += 1
                    if counter % 8 == 0:
                        timeslot_array_form.append([])
                        timeslot_array_form.append([])
                # Add course information with corresponding array to body
                course_array_form.append(
                    {
                        'range': self.cell_to_a1_notation(sheet_name, current_col, current_row),
                        'values': timeslot_array_form
                    }
                )
                # Add current range to clear range list
                clear_ranges.append(
                    self.range_to_a1_notation(sheet_name,
                                              current_clear_col, current_clear_row,
                                              current_end_clear_col, current_end_clear_row)
                )

                # Move ranges to the next position
                current_clear_col, current_clear_row, current_end_clear_col, current_end_clear_row = \
                    self.get_next_range(sheet_name,
                                        current_clear_col, current_clear_row,
                                        current_end_clear_col, current_end_clear_row)

                sheet_name, current_col, current_row = self.get_next_cell(sheet_name, current_col, current_row)
        print('Course in array form: ', course_array_form)

        # Clear an additional 'timeslot' to have at least one empty group
        clear_ranges.append(
            self.range_to_a1_notation(sheet_name,
                                      current_clear_col, current_clear_row,
                                      current_end_clear_col, current_end_clear_row)
        )

        # Clear range first
        self.bot.service.spreadsheets().values().batchClear(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'ranges': clear_ranges
            }
        ).execute()

        # Write new values
        body = dict(
            valueInputOption='USER_ENTERED',
            data=course_array_form)
        response_date = self.bot.service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()

        print('{0} cells updated.'.format(response_date.get('updatedCells')))
        return

    # Creates a connection to a Google service
    def create_service(self, client_secret_file, api_service_name, api_version, *scopes):
        scopes = [scope for scope in scopes[0]]

        cred = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token_write.pickle'):
            with open('token_write.pickle', 'rb') as token:
                cred = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
                cred = flow.run_local_server()
            # Save the credentials for the next run
            with open('token_write.pickle', 'wb') as token:
                pickle.dump(cred, token)

        try:
            self.bot.service = build(api_service_name, api_version, credentials=cred)
            self.bot.export = self.export_data_to_sheets
            print(api_service_name, 'service created successfully')
            # return service
        except Exception as e:
            print(e)
            # return None

    def get_next_cell(self, sheet_name, current_col, current_row):
        return [sheet_name, current_col + WIDTH_OFFSET, current_row]

    def get_next_range(self, sheet_name, current_col_start, current_row_start, current_col_end, current_row_end):
        return [current_col_start + WIDTH_OFFSET, current_row_start,
                current_col_end + WIDTH_OFFSET, current_row_end]

    def cell_to_a1_notation(self, sheet_name, col, row):
        result = []
        while col:
            col, rem = divmod(col - 1, 26)
            result[:0] = LETTERS[rem]
        return (sheet_name + '!') + ''.join(result) + str(row)

    def range_to_a1_notation(self, sheet_name, start_col, start_row, end_col, end_row):
        start_result = []
        end_result = []
        while start_col:
            start_col, rem = divmod(start_col - 1, 26)
            start_result[:0] = LETTERS[rem]
        while end_col:
            end_col, rem = divmod(end_col - 1, 26)
            end_result[:0] = LETTERS[rem]
        range_a1_notation = (sheet_name + '!') + ''.join(start_result) + (str(start_row) if start_row else '')
        range_a1_notation += ':' + ''.join(end_result) + (str(end_row) if end_row else '')
        return range_a1_notation


def setup(bot):
    bot.add_cog(GoogleSheetCog(bot))
