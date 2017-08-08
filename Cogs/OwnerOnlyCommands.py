from aiohttp import ClientSession
from os import execl
from sys import exit, executable, argv, exc_info
from discord import Status, Colour
from discord.ext import commands
from Cogs.Utils.Permissions import permissionChecker


class OwnerOnly(object):

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    @commands.command(pass_context=True)
    @permissionChecker(check='is_owner')
    async def editrolecolour(self, ctx, colour, *, name):
        '''
        Lets you change the profile.
        '''

        r = [i for i in ctx.message.server.roles if name.lower() in i.name.lower()]
        if len(r) > 1:
            await self.bot.say('Too many roles etc')
            return
        elif len(r) < 1:
            await self.bot.say('nop no roles like that')
            return

        if len(colour) == 6:
            colour = Colour(int(colour, 16))
        else:
            await self.bot.say('Idk what colours are, man')
            return

        await self.bot.edit_role(ctx.message.server, r[0], colour=colour)
        await self.bot.say('Done.')

    @commands.group()
    @permissionChecker(check='is_owner')
    async def profile(self):
        '''
        Lets you change the profile.
        '''

        pass

    @profile.command()
    @permissionChecker(check='is_owner')
    async def name(self, *, name:str=None):
        '''
        Changes the name of the profile.
        '''

        if name == None:
            await self.bot.say('`!profile name [NAME]`')
            return

        await self.bot.edit_profile(username=name)
        w = await self.bot.say('👌')
        await sleep(2)
        await self.bot.delete_message(w)

    @profile.command()
    @permissionChecker(check='is_owner')
    async def avatar(self, *, avatar:str=None):
        '''
        Changes the profile picture of the bot.
        '''

        if avatar == None:
            await self.bot.say('`!profile avatar [URL]`')
            return

        async with self.session.get(avatar) as r:
            content = r.read()

        await self.bot.edit_profile(avatar=content)
        w = await self.bot.say('👌')
        await sleep(2)
        await self.bot.delete_message(w)

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
    async def cls(self, ctx):
        '''
        Clears the console
        '''

        print('\n' * 50)
        await self.bot.say('Done.')

    @commands.command(pass_context=True, hidden=True)
    @permissionChecker(check='is_owner')
    async def kill(self, ctx):
        '''
        Kills the bot. Makes it deaded
        '''

        # If it is, tell the user the bot it dying
        await self.bot.say('*Finally*.')
        await self.bot.change_presence(status=Status.invisible, game=None)
        exit()

    @commands.command(pass_context=True, hidden=True, aliases=['rs'])
    @permissionChecker(check='is_owner')
    async def restart(self, ctx):
        '''
        Restarts the bot. Literally everything
        '''

        # If it is, tell the user the bot it dying
        await self.bot.say('Now restarting.')
        await self.bot.change_presence(status=Status.dnd, game=None)
        execl(executable, *([executable] + argv))  

    @commands.command(pass_context=True, hidden=True)
    @permissionChecker(check='is_owner')
    async def rld(self, ctx, *, extention:str):
        '''
        Reloads a cog from the bot
        '''

        extention = f'Cogs.{extention}'

        # Unload the extention
        await self.bot.say("Reloading extension **{}**...".format(extention))
        try:
            self.bot.unload_extension(extention)
        except:
            pass

        # Load the new one
        try:
            self.bot.load_extension(extention)
        except Exception:
            type_, value_, traceback_ = exc_info()
            ex = format_exception(type_, value_, traceback_)
            output = ''.join(ex)
            await self.bot.say('```python\n{}```'.format(output))
            return

        # Boop the user
        await self.bot.say("Done!")


def setup(bot):
    x = OwnerOnly(bot)
    bot.add_cog(x)
