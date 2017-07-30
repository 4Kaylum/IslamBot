from datetime import datetime, timedelta
from re import search, IGNORECASE
from discord import PermissionOverwrite, Channel
from discord.ext import commands
from Cogs.Utils.Permissions import permissionChecker


class CalebAnnoyanceMachine(object):

    def __init__(self, bot):
        self.bot = bot 
        self.calebConstant = r'(bot|sultan).+(((is not|isn\'t)+.+(working))|((is) (broken|down|dead)))'
        self.languageConst = r'what(\'s)* ((programming )*language|is).*(bot|sultan|code)'
        self.lastSaid = datetime(1971, 1, 1, 1, 1, 1, 1)

    def timeCheck(self, message):
        return message.timestamp > self.lastSaid + timedelta(minutes=5)

    async def on_message(self, message):

        if search(self.languageConst, message.content, IGNORECASE):
            await self.bot.send_message(message.channel, 'I\'m written in Python3.6, using the Discord.py library c:')

        # if self.timeCheck or message.author.id == '141231597155385344':
        #     pass
        # else:
        #     return

        # if search(self.calebConstant, message.content, IGNORECASE):
        #     await self.bot.send_message(
        #         message.channel, 
        #         'Yo, <@141231597155385344>, this guy thinks I\'m broken. Fix me.'
        #     )
        #     self.lastSaid = datetime.now()

    @commands.command(pass_context=True)
    @permissionChecker(check='is_owner')
    async def sendimages(self, ctx, channel:str=None):
        if not channel:
            channel = ctx.message.channel
        else:
            channel = [i for i in ctx.message.server.channels if channel.lower() in i.name.lower()][0]
        role = [i for i in ctx.message.server.roles if i.id == '257634720572112896'][0]
        q = PermissionOverwrite(attach_files=True, read_messages=True, send_messages=True)
        await self.bot.edit_channel_permissions(channel, role, q)
        await self.bot.say('Done!')   


def setup(bot):
    x = CalebAnnoyanceMachine(bot)
    bot.add_cog(x)
