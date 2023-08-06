from enum import Enum, unique


@unique
class SyncademyEmoji(Enum):
    TANK = 'tank'
    TANK_ROLE = 'tank_role'
    HEALER = 'healer'
    HEALER_ROLE = 'healer_role'
    DPS = 'dps'
    MELEE_ROLE = 'melee_role'
    CASTER_ROLE = 'caster_role'
    RANGED_ROLE = 'ranged_role'
    BACKUP = 'online'
    BLU = 'blue_mage'
    EUREKA = 'eureka'