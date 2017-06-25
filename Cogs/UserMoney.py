from discord.ext import commands 
from Cogs.Utils.DatabaseHandling import getFileJson, saveFileJson
from Cogs.Utils.FileHandling import getCogConfigurations

class UserMoney(object): 

    def __init__(self, bot):
        self.bot = bot
        self.logChannels, self.logMessages, self.privateMessages = getCogConfigurations(bot)

    @commands.command(pass_context=True, aliases=['wallet'])
    async def money(self, ctx):
        '''
        Shows you how much money you have in your user account
        '''

        userData = getFileJson('money.json')
        userMoney = userData.get(ctx.message.author.id, 0)
        await self.bot.whisper('You have `{}` credits in your account.'.format(userMoney))

    @commands.command(pass_context=True)
