class Student:
    def __init__(self, db_id=None, discord_id=None, discord_name=None, discord_nickname=None, lodestone_id=None,
                 character_name=None, participations=None):
        self.db_id = db_id
        self.discord_id = discord_id
        self.discord_name = discord_name
        self.discord_nickname = discord_nickname
        self.lodestone_id = lodestone_id
        self.character_name = character_name
        self.participations = participations  # integer should this be here at all?

    def add_participations(self, participations):
        self.participations += participations

    def get_discord_id(self):
        return self.discord_id

    def get_discord_name(self):
        return self.discord_name

    def get_discord_nickname(self):
        return self.discord_nickname
