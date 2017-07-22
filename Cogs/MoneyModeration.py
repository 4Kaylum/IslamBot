from discord import Member
from discord.ext import commands
from Cogs.Utils.Permissions import permissionChecker 
from Cogs.Utils.FileHandling import getFileJson, saveFileJson


class MoneyModeration(object):

    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def moneyof(self, ctx, user:Member):
        '''
        Shows you the amount of money a particular user has
        '''

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        await self.bot.whisper('The user `{}` has `{}` credits in their account.'.format(user, userMoney))

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def addmoney(self, ctx, amount:int, user:Member):
        '''
        Adds money to a user's account
        '''

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        userMoney += amount
        userData[user.id] = userMoney
        saveFileJson('userMoney.json', userData)
        await self.bot.say('This user\'s account has now been modified by a factor of `{}`.'.format(amount))

    @commands.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def removemoney(self, ctx, amount:int, user:Member):
        '''
        Removes money from a user's account
        '''

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        amount = -amount
        userMoney += amount
        userData[user.id] = userMoney
        saveFileJson('userMoney.json', userData)
        await self.bot.say('This user\'s account has now been modified by a factor of `{}`.'.format(amount))


def setup(bot):
    x = MoneyModeration(bot)
    bot.add_cog(x)
