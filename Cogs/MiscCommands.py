from discord import Member
from discord.ext import commands 
from Cogs.Utils.Permissions import permissionChecker 


class Misc(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def clean(self, ctx, amount:int=50): 
        '''
        Removes the last x messages of the bot from a given channel
        '''

        d = await self.bot.purge_from(ctx.message.channel, limit=amount, check=lambda x: x.author.id == self.bot.user.id)
        await self.bot.say('Removed `{}` messages.'.format(len(d)))

    @commands.command(pass_context=True)
    async def annoycaleb(self, ctx):
        '''
        Fuck off.
        '''

        await self.bot.say('<@141231597155385344>')

    @commands.command(pass_context=True)
    @permissionChecker(check='manage_messages', compare=True)
    async def purge(self, ctx, amount:int=50, user:Member=None):
        '''
        Removes the last x messages [from y user] from the channel
        '''

        if user:
            check = lambda x: x.author.id == user.id 
        else:
            check = lambda x: True 

        d = await self.bot.purge_from(ctx.message.channel, limit=amount, check=check)
        await self.bot.say('Removed `{}` messages.'.format(len(d)))


def setup(bot):
    x = Misc(bot)
    bot.add_cog(x)
