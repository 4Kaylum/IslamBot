from re import search
from discord import Member
from discord.ext import commands
from Cogs.Utils.Permissions import permissionChecker 
from Cogs.Utils.FileHandling import getFileJson, saveFileJson
from Cogs.Utils.Exceptions import MemberMissingPermissions


class MoneyModeration(object):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.additionRegex = r'^<@\d+> *\+\+ -*\d+$'

    async def on_message(self, message):
        
        # Determine if using the `.user++ amount` syntax
        if not search(self.additionRegex, message.content):
            return

        # They are - check permissions
        if message.author.server_permissions.manage_channels or message.author.id in getFileJson('Configs.json')['Owner IDs'] or message.author.server_permissions.administrator:
            pass
        else:
            await self.bot.send_message(message.channel, 'You are missing the permissions required to run that command.')
            return

        # Wew that was a long line; change the user
        user = message.channel.server.get_member(''.join(i for i in message.content.split(' ')[0] if i.isdigit()))
        amount = int(message.content.split(' ')[-1])

        # Copy paste from the other command 
        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        userMoney += amount
        userData[user.id] = userMoney
        saveFileJson('userMoney.json', userData)
        await self.bot.send_message(
            message.channel, 
            'This user\'s account has now been modified by a factor of `{}`.'.format(amount)
        )


    @commands.command(pass_context=True)
    @permissionChecker(check='manage_channels')
    async def moneyof(self, ctx, user:Member):
        '''
        Shows you the amount of money a particular user has
        '''

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        try:
            await self.bot.whisper('The user `{}` has `{}` credits in their account.'.format(user, userMoney))
        except Exception as e:
            await self.bot.say('I can\'t send you PMs. Please enable these to allow me to send you messages.')

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_channels')
    async def addmoney(self, ctx, amount, user):
        '''
        Adds money to a user's account
        '''

        try:
            amount = int(amount)
            userMention = user
        except ValueError:
            userMention, amount = amount, int(user)

        user = ctx.message.server.get_member(''.join(i for i in userMention if i.isdigit()))

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(user.id, 0)
        userMoney += amount
        userData[user.id] = userMoney
        saveFileJson('userMoney.json', userData)
        await self.bot.say('This user\'s account has now been modified by a factor of `{}`.'.format(amount))

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_channels')
    async def removemoney(self, ctx, amount, user):
        '''
        Removes money from a user's account
        '''

        try:
            int(amount)
        except ValueError:
            user, amount = amount, user

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
