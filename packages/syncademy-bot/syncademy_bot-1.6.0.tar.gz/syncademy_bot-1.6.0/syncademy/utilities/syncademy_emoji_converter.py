from discord.ext import commands
from discord.ext.commands import BadArgument

from syncademy.utilities.syncademy_emoji import SyncademyEmoji
from syncademy.utilities.timeslot_emoji import TimeslotEmoji


class SyncademyEmojiConverter(commands.EmojiConverter):
    async def convert(self, ctx, argument):
        try:
            emoji = await super().convert(ctx, argument)
            return SyncademyEmoji(emoji.name)
        except BadArgument as bae:
            # If it matches one of unicode timeslot emojis, handle it, else throw the exception
            return TimeslotEmoji(argument)
