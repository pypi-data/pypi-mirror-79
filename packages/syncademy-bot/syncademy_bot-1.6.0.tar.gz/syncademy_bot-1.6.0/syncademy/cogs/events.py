import discord
from discord.ext import commands

from syncademy.cogs import syncademy
from syncademy.config import config
from syncademy.utilities.syncademy_role import SYNCADEMY_EMOJI_DICT

ROLE_ASSIGNMENT_MSG_ID = config.getint('gsheets', 'role_assignment_msg_id')
ROLE_ASSIGNMENT_CHANNEL_ID = config.getint('gsheets', 'role_assignment_channel_id')


class Events(commands.Cog):
    def __init__(self, bot, message_id=ROLE_ASSIGNMENT_MSG_ID, channel_id=ROLE_ASSIGNMENT_CHANNEL_ID):
        self.bot = bot
        self.listeners = [(channel_id, message_id)]
        print(f'Added Events Cog with message_id={message_id} and channel_id={channel_id}')

    def listen_to(self, channel_id, message_id):
        self.listeners.append((channel_id, message_id))
        print(f'Now also listening to message_id={message_id} and channel_id={channel_id}')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # message_id, user_id, channel_id, emoji, member, event_type
        if payload.event_type == 'REACTION_ADD':
            await self.handle_add_reaction(payload)
        # else: handle_remove_reaction(payload)

    async def handle_add_reaction(self, payload):
        # if any channel+message pair matches the payload channel+message:
        # [expr for elem in iterable if conditional] - see list comprehension
        # (iterate over iterable, if conditional is true do expression and create list with all the results)
        if any([chan_msg_pair[1] == payload.message_id
                for chan_msg_pair in self.listeners if chan_msg_pair[0] == payload.channel_id]):
            print(f'{payload.user_id} added a reaction {syncademy.parse_emoji(payload.emoji)}')
            await self.handle_role_reaction(payload, syncademy.parse_emoji(payload.emoji))

    async def handle_role_reaction(self, payload, parsed_emoji):
        if parsed_emoji in SYNCADEMY_EMOJI_DICT:
            syncademy_role = SYNCADEMY_EMOJI_DICT[parsed_emoji]
            separator_role = syncademy_role.separator_role
            member = payload.member
            member_roles = member.roles
            role = discord.utils.get(member.guild.roles, name=syncademy_role.role_name)

            if role in member_roles:
                member_roles.remove(role)
                await member.remove_roles(role)
                # if user loses all reactions roles for a given separator, remove separator role
                if separator_role:
                    # for each child role of this role's separator role (aka, go to parent then get all children)
                    # if that role exists in member_roles, return true
                    # if none of the child roles exists in member_roles, return false
                    if not any(x in map(lambda mrole: mrole.name, member_roles)
                               for x in map(lambda x: x.role_name, separator_role.children)):
                        await member.remove_roles(discord.utils.get(member.guild.roles, name=separator_role.role_name))
            else:
                await member.add_roles(role)
                if separator_role and separator_role not in member_roles:
                    await member.add_roles(discord.utils.get(member.guild.roles, name=separator_role.role_name))

            await self.remove_reaction(member, parsed_emoji, payload)

    async def remove_reaction(self, member, parsed_emoji, payload):
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        print(f'Removing reaction {parsed_emoji} by {member}')
        await msg.remove_reaction(payload.emoji, member)


def setup(bot):
    bot.add_cog(Events(bot))
