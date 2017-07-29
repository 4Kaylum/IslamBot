from datetime import datetime, timedelta
from re import search, IGNORECASE
from discord.ext import commands


class CalebAnnoyanceMachine(object):

    def __init__(self, bot):
        self.bot = bot 
        self.calebConstant = r'(bot|sultan).+(((is not|isn\'t)+.+(working))|((is) (broken|down|dead)))'
        self.lastSaid = datetime(1971, 1, 1, 1, 1, 1, 1)

    def timeCheck(self, message):
        return message.timestamp > self.lastSaid + timedelta(minutes=5)

    async def on_message(self, message):
        if self.timeCheck or message.author.id == '141231597155385344':
            pass
        else:
            return

        if search(self.calebConstant, message.content, IGNORECASE):
            await self.bot.send_message(
                message.channel, 
                'Yo, <@141231597155385344>, this guy thinks I\'m broken. Fix me.'
            )
            self.lastSaid = datetime.now()


def setup(bot):
    x = CalebAnnoyanceMachine(bot)
    bot.add_cog(x)
