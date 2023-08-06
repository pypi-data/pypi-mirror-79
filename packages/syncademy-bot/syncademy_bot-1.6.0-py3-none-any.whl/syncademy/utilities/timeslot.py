class Timeslot:
    def __init__(self, emoji=None, signups=None):
        if signups is None:
            signups = []
        self.emoji = emoji
        self.signups = signups

    def add_signup(self, signup):
        if self.signups is None:
            self.signups = []
        self.signups.append(signup)

    def to_array(self):
        return [self.signups.to_array()]
