from collections import defaultdict

import discord
from discord.ext import commands

from syncademy.cogs.events import Events
from syncademy.utilities.course import Course, StandardCourseEmojis
from syncademy.utilities.signup import Signup
from syncademy.utilities.student import Student
from syncademy.utilities.syncademy_emoji import SyncademyEmoji
from syncademy.utilities.syncademy_emoji_converter import SyncademyEmojiConverter
from syncademy.utilities.timeslot import Timeslot
from syncademy.utilities.timeslot_emoji import TimeslotEmoji


class SyncademyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', help='Syncademy says hello')
    @commands.has_role('Faculty Member')
    async def hello(self, ctx):
        response = 'Hello World!'
        await ctx.send(response)

    @commands.command(name='parse_reactions',
                      help='Receives a message ID (same channel) or message URL (different channel) and sends a message with the users and their reactions')
    @commands.has_role('Faculty Member')
    async def parse_reactions(self, ctx, msg: discord.Message):
        # print(f'Message: {msg.content}')
        # print(f'Reactions: {msg.reactions} for {msg.jump_url}')

        # Store the emojis on a dictionary {user: list(emojis)}
        user_roles = defaultdict(list)
        user_timeslots = defaultdict(list)

        for reaction in msg.reactions:
            async for user in reaction.users():
                if not isinstance(reaction.emoji, discord.Emoji):
                    # Unicode Emojis
                    user_timeslots[user].append(TimeslotEmoji(reaction.emoji))
                else:
                    # Custom Discord Emojis
                    user_roles[user].append(SyncademyEmoji(reaction.emoji.name))

        signups = defaultdict()
        timeslot_users = defaultdict(list)
        timeslot_list = [create_timeslot(None, [])]

        # Creating signups
        for user, role_emojis in user_roles.items():
            signups[user] = create_signup_from_user(user, role_emojis)
            # Add to dummy timeslot, if user has not selected one
            if user_timeslots[user] is None:
                timeslot_list[0].add_signup(create_signup_from_user(user, role_emojis))

        # Map signups to timeslots by iterating over user timeslot selections
        for user, timeslot_emojis in user_timeslots.items():
            for timeslot_emoji in timeslot_emojis:
                # User has selected roles => Add signup with roles
                if user in signups:
                    timeslot_users[timeslot_emoji].append(signups[user])
                # User has not selected roles => Add signup without roles
                else:
                    timeslot_users[timeslot_emoji].append(create_signup_from_user(user, []))

        # Create timeslots and add them to list
        for timeslot_emoji, timeslot_signups in timeslot_users.items():
            timeslot_list.append(create_timeslot(timeslot_emoji, timeslot_signups))

        course = create_course(message_id=msg.id, channel_id=msg.channel.id, date='parse date from message',
                               timeslots=timeslot_list)

        try:
            self.bot.export(course)
            response = 'SUCCESS: Signups got parsed and exported!'
            print(f'{response}')
        except AttributeError as ae:
            response = 'ERROR: Tried to export but could not find service!'
            print(f'{response} - {ae}')

        await ctx.send(response)

    @commands.command(name='add_reactions',
                      help='Receives a message ID (same channel) or message URL (different channel), '
                           'a mode (\'single\',\'double\', or \'custom\') '
                           'and a list of emojis (empty if single or double, non-empty when custom), '
                           'and sends a message with the users and their reactions')
    @commands.has_role('Faculty Member')
    # This command only accepts syncademy or timeslot emojis - any other and it will crash
    # TODO - figure out why sometimes this code bugs with 'Unknown emoji', and sometimes it works fine
    async def add_reactions(self, ctx, msg: discord.Message, mode, *emojis: SyncademyEmojiConverter):
        try:
            if mode == 'single':
                emojis = StandardCourseEmojis.SINGLE_SLOT.value
            elif mode == 'double':
                emojis = StandardCourseEmojis.DOUBLE_SLOT.value

            for emoji in emojis:
                if isinstance(emoji, SyncademyEmoji):
                    converted_emoji = discord.utils.get(self.bot.emojis, name=emoji.value)
                else:
                    converted_emoji = emoji.value
                await msg.add_reaction(converted_emoji)
        except Exception as e:
            await ctx.send(str(e))
            raise e

    @commands.command(name='listen_roles',
                      help='Receives a message ID (same channel) or message URL (different channel) '
                           'and makes the bot listen to role reactions added to it')
    @commands.has_role('Faculty Member')
    async def listen_roles(self, ctx, msg: discord.Message):
        # Go to Event cog, and set the message?
        # or add a new 'instance' of the event cog to listen to a specific message?
        cog = self.bot.get_cog('Events')
        cog.listen_to(msg.channel.id, msg.id)
        print(self.bot.cogs)
        pass


# ----------------------------------
# ------   Public methods   -------
# ----------------------------------

def create_course(message_id, channel_id, date, timeslots):
    return Course(
        message_id=message_id,
        channel_id=channel_id,
        date=date,
        timeslots=timeslots)


def create_timeslot(emoji, signups):
    return Timeslot(
        emoji=emoji,
        signups=signups)


def create_signup(student, role_emojis):
    return Signup(
        student=student,
        is_tank=SyncademyEmoji.TANK in role_emojis
                or SyncademyEmoji.TANK_ROLE in role_emojis,
        is_healer=SyncademyEmoji.HEALER in role_emojis
                  or SyncademyEmoji.HEALER_ROLE in role_emojis,
        is_dps=SyncademyEmoji.DPS in role_emojis,
        is_melee=SyncademyEmoji.MELEE_ROLE in role_emojis,
        is_ranged=SyncademyEmoji.RANGED_ROLE in role_emojis,
        is_caster=SyncademyEmoji.CASTER_ROLE in role_emojis,
        is_backup=SyncademyEmoji.BACKUP in role_emojis)


def create_signup_from_user(user, role_emojis):
    student = create_student(user)
    signup = create_signup(student, role_emojis)
    return signup


def create_student(discord_user):
    return Student(
        discord_id=discord_user.id,
        discord_name=discord_user.name + '#' + discord_user.discriminator,
        discord_nickname=discord_user.display_name)


def parse_emoji(emoji):
    # probably needs some better way to handle the weird strings like :one: or non-defined emojis
    try:
        # Custom Emoji
        if isinstance(emoji, discord.Emoji) or isinstance(emoji, discord.PartialEmoji):
            return SyncademyEmoji(emoji.name)
        # Unicode Emoji
        else:
            return TimeslotEmoji(emoji)
    except ValueError:
        return None


def setup(bot):
    bot.add_cog(SyncademyCog(bot))
