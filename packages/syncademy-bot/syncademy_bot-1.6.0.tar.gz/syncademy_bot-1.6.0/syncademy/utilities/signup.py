class Signup:
    def __init__(self, student=None, is_tank=False, is_healer=False, is_dps=False, is_melee=False,
                 is_ranged=False, is_caster=False, is_backup=False, has_participated=False):
        self.student = student  # Student
        self.isTank = is_tank  # boolean
        self.isHealer = is_healer  # boolean
        self.isMelee = is_melee  # boolean
        self.isRanged = is_ranged  # boolean
        self.isCaster = is_caster  # boolean
        self.isDps = is_dps or self.isMelee or self.isRanged or self.isCaster
        self.isBackup = is_backup  # boolean
        self.hasParticipated = has_participated  # boolean

    def to_array(self):
        return [self.student.get_discord_name(), self.isTank, self.isHealer, self.isDps, self.isMelee,
                self.isRanged, self.isCaster, self.isBackup]
