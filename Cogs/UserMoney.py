from discord.ext import commands 
from Cogs.Utils.FileHandling import getFileJson, saveFileJson, getCogConfigurations
from Cogs.Utils.MoneyHandling import Banker


class UserMoney(object): 

    def __init__(self, bot):
        self.bot = bot
        self.logChannels, self.logMessages, self.privateMessages = getCogConfigurations(bot)
        self.banker = Banker()

    async def on_message(self, message):
        self.banker.handle(message)

    @commands.command(pass_context=True, aliases=['wallet'])
    async def money(self, ctx):
        '''
        Shows you how much money you have in your user account
        '''

        userData = getFileJson('userMoney.json')
        userMoney = userData.get(ctx.message.author.id, 0)
        await self.bot.whisper('You have `{}` credits in your account.'.format(userMoney))

    @commands.command(pass_context=True)
    async def buyrole(self, ctx, *, roleName:str):
        '''
        Lets you buy a role
        '''

        roleData = getFileJson('buyableRoles.json')
        roleIDs = list(roleData.keys())
        serverRoles = list(ctx.message.roles)
        availableRoles = [i for i in serverRoles if i.id in roleIDs]

        # Determine what role they were trying to search for
        wantedRole = [i for i in availableRoles if roleName.lower() in i.name.lower() or roleName == i.id]

        # Determine if that role exists
        if len(wantedRole) == 0:
            await self.bot.say('There were no roles that matched the hitstring `{}`.'.format(roleName))
            return
        elif len(wantedRole) > 1:
            v = 'There were multiple roles that matched the hitstring `{}`; \n* {}'.format(roleName, '\n* '.join(wantedRole))
            await self.bot.say(v)
            return
        else:
            # There was only one role that matched that hitstring
            pass

        # Determine whether the user already has the role or not
        userRoles = list(ctx.message.author.roles)
        if wantedRole[0] in userRoles:
            await self.bot.say('You already have that role!')
            return

        # Determine whether or not they have enough money for it
        userData = getFileJson('userMoney.json')
        userMoney = userData.get(ctx.message.author.id, 0)
        roleCost = roleData.get(str(wantedRole[0].id))
        if userMoney < roleCost:
            await self.bot.say('You don\'t have enough money to purchase that role.')
            return

        # They have enough money - add the role and deduct money from their account
        self.bot.add_roles(ctx.message.author, wantedRole[0])
        userMoney -= roleCost
        userData[ctx.message.author.id] = userMoney
        saveFileJson('userMoney.json', userData)
        await self.bot.say('The role `{}` has been sucessfully added to you for `{}` credits.'.format(wantedRole[0].name, roleCost))


def setup(bot):
    x = UserMoney(bot)
    bot.add_cog(x)
