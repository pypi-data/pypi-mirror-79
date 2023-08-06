import configparser
import os


class TechnicalSyncademyException(Exception):
    pass


class BotConfig(configparser.ConfigParser):
    def __init__(self, config_file):
        super(BotConfig, self).__init__(allow_no_value=True)
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        if not os.path.isfile(config_path):
            raise TechnicalSyncademyException('Config file not found in %s!' % config_path)
        self.read(config_path)
        self.validate_config()

    def validate_config(self):
        section = None
        keys = None

        required_values = {
            'discord': {
                'token': None
            },
            'gsheets': {
                'credentials_json': None,
                'spreadsheet_id': None,
                'sheet_name': None
            }
        }

        for section, keys in required_values.items():
            if section not in self:
                raise TechnicalSyncademyException(
                    'Missing section %s in the config file' % section
                )

        for key, values in keys.items():
            if key not in self[section] or self[section][key] == '':
                raise TechnicalSyncademyException(
                    'Missing value for %s under section %s in the config file' % (key, section)
                )

            if values:
                if self[section][key] not in values:
                    raise TechnicalSyncademyException(
                        'Invalid value for %s under section %s in the config file' % (key, section)
                    )


config = {}

try:
    config = BotConfig('resources/syncademy_bot.ini')
except TechnicalSyncademyException as e:
    print(e)
    exit(1)
