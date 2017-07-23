from discord import Member
from discord.ext import commands 
from Cogs.Utils.FileHandling import getCogConfigurations, getFileJson, saveFileJson
from Cogs.Utils.Permissions import permissionChecker


class UserWarnings(object):

    def __init__(self, bot):
        self.bot = bot
        self.logChannels, self.logMessages, self.privateMessages = getCogConfigurations(bot)

    @commands.command(pass_context=True)
    @permissionChecker(check='kick_members')
    async def warn(self, ctx, user:Member, *, reason:str=None):
        '''
        Gives a warning to the user.
        '''

        # Require a reason
        if reason == None:
            await self.bot.say('You need to provide a reason for your warning.')
            return 

        # Set up local variable
        moderator = ctx.message.author

        # Get the current warnings for the user
        warningData = getFileJson('userWarns.json')
        warnAmounts = warningData.get(user.id, 0)

        # Increment their warns by one
        warnAmounts += 1

        # Check if they're over three warnings
        warnType = None
        if warnAmounts >= 3:

            # This is the point at which we kick the user
            warnType = 'Warn Kick'
            f = self.privateMessages['Warn Kick'].format(server=ctx.message.server, reason=reason)    
            try:
                await self.bot.send_message(user, f)
            except Exception:
                pass
            await self.bot.kick(user)
            await self.bot.say('👌 This user has been kicked for having 3 warnings.')

        else:

            # Just a warning
            warnType = 'Warn'

        # Save the new warning data 
        if warnAmounts >= 3:
            del warningData[user.id]
        else:
            warningData[user.id] = warnAmounts
        saveFileJson('userWarns.json', warningData)

        # Send a message back to the user
        await self.bot.say('👌 This user has had a warning applied for reason `{}`.'.format(reason))

        # Send a message to the logs channel
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels[warnType]
        f = self.logMessages[warnType].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)

    @commands.command(pass_context=True, aliases=['warnset', 'setwarn'])
    @permissionChecker(check='kick_members')
    async def setwarns(self, ctx, user:Member, amount:int=0):
        '''
        Sets the amount of warnings that a user has
        '''

        if amount >= 3:
            await self.bot.say('You can only *set* a maximum of 2 warnings on a user.')
            return
        elif amount < 0:
            await self.bot.say('You can\'t... you can\'t give someone *negative* warnings. That\'s dumb. Stop that. Don\'t be dumb.')
            return

        # Get the current warnings for the user
        warningData = getFileJson('userWarns.json')

        # Save the new warning data 
        if amount == 0:
            try:
                del warningData[user.id]
            except Exception:
                pass
        else:
            warningData[user.id] = warnAmounts
        saveFileJson('userWarns.json', warningData)

        # Send a message back to the user
        await self.bot.say('👌 This user has had their warnings set to `{}`.'.format(amount))


def setup(bot):
    x = UserWarnings(bot)
    bot.add_cog(x)
