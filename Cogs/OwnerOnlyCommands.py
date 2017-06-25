from os import execl
from sys import exit, executable, argv, exc_info
from discord.ext import commands


class OwnerOnly(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    @permissionChecker(check='is_owner')
    async def ev(self, ctx, *, content: str):
        '''
        Evaluates a given Python expression
        '''

        # Eval and print the answer
        try:
            output = eval(content)
        except Exception:
            type_, value_, traceback_ = exc_info()
            ex = format_exception(type_, value_, traceback_)
            output = ''.join(ex)
        await self.bot.say('```python\n{}```'.format(output))

    @commands.command(pass_context=True, hidden=True)
    @permissionChecker(check='is_owner')
    async def kill(self, ctx):
        '''
        Kills the bot. Makes it deaded
        '''

        # If it is, tell the user the bot it dying
        await self.sparcli.say('*Finally*.')
        await self.sparcli.change_presence(status=Status.invisible, game=None)
        exit()

    @commands.command(pass_context=True, hidden=True, aliases=['rs'])
    @permissionChecker(check='is_owner')
    async def restart(self, ctx):
        '''
        Restarts the bot. Literally everything
        '''

        # If it is, tell the user the bot it dying
        await self.sparcli.say('Now restarting.')
        await self.sparcli.change_presence(status=Status.dnd, game=None)
        execl(executable, *([executable] + argv))  


def setup(bot):
    x = OwnerOnly(bot)
    bot.add_cog(x)
