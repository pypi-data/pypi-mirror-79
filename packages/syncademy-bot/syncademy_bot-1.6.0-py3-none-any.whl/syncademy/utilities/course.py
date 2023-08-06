from enum import Enum

from syncademy.utilities.syncademy_emoji import SyncademyEmoji
from syncademy.utilities.timeslot_emoji import TimeslotEmoji


class Course:
    def __init__(self, message_id=None, channel_id=None, date=None, timeslots=None):
        self.messageId = message_id
        self.channelId = channel_id
        self.date = date
        self.timeslots = timeslots

    def add_timeslot(self, emoji, timeslot):
        self.timeslots.append(emoji, timeslot)


class StandardCourseEmojis(Enum):
    SINGLE_SLOT = (TimeslotEmoji.ACCEPTED,
                   SyncademyEmoji.TANK_ROLE,
                   SyncademyEmoji.HEALER_ROLE,
                   SyncademyEmoji.MELEE_ROLE,
                   SyncademyEmoji.RANGED_ROLE,
                   SyncademyEmoji.CASTER_ROLE,
                   SyncademyEmoji.BACKUP)
    DOUBLE_SLOT = (TimeslotEmoji.CLOCK_FIVE,
                   TimeslotEmoji.CLOCK_SEVEN,
                   SyncademyEmoji.TANK_ROLE,
                   SyncademyEmoji.HEALER_ROLE,
                   SyncademyEmoji.MELEE_ROLE,
                   SyncademyEmoji.RANGED_ROLE,
                   SyncademyEmoji.CASTER_ROLE,
                   SyncademyEmoji.BACKUP)
