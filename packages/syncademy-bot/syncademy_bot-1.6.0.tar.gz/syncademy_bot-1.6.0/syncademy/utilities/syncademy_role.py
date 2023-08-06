from enum import Enum
from syncademy.utilities.syncademy_emoji import SyncademyEmoji


class SyncademyRole:
    def __init__(self, role_name, emoji=None, separator_role=None):
        self.role_name = role_name
        self.separator_role = separator_role
        self.emoji = emoji
        self.children = []
        if separator_role:
            separator_role.add_child(self)

    def add_child(self, child):
        self.children.append(child)


# Initialize Roles in a way that allows them to reference each other, before adding them to the map
stu_assoc_role = SyncademyRole('⁣      Students\' Associations        ⁣')
blu_role = SyncademyRole('Blue Mage', SyncademyEmoji.BLU, stu_assoc_role)
eureka_role = SyncademyRole('Eureka', SyncademyEmoji.EUREKA, stu_assoc_role)


class SyncademyRoleMap(Enum):
    STUDENTS_ASSOC = stu_assoc_role,
    BLU = blu_role,
    EUREKA = eureka_role


SYNCADEMY_EMOJI_DICT = {
    SyncademyEmoji.BLU: blu_role,
    SyncademyEmoji.EUREKA: eureka_role
}