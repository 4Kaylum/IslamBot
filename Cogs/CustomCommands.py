from discord.ext import commands 
from Cogs.Utils.FileHandling import getFileJson, saveFileJson
from Cogs.Utils.Permissions import permissionChecker 


class CustomCommands(object):

    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        commands = getFileJson('customCommands.json')
        self.cc = commands

    async def on_message(self, message):
        '''
        Triggers the command to be used
        '''
        
        commandResponse = self.cc.get(message.content)
        if commandsResponse:
            await self.bot.send_message(message.channel, commandResponse)
        else:
            pass

    @commands.group(pass_context=True)
    @permissionChecker(check='administrator')
    async def tag(self, ctx):
        '''
        The custom commands handler for the bot
        '''

        pass

    @tag.command(pass_context=True)
    @permissionChecker(check='administrator')
    async def add(self, ctx):
        '''
        Add a custom command to the bot
        '''

        # Get the name of the command
        await self.bot.say('What will the name of the command be?')
        mes = await self.bot.wait_for_message(author=ctx.message.author)
        commandName = mes.content

        # Validate it
        while commandName[0] == '!':
            commandName = commandName[1:]
        if not commandName:
            await self.bot.say('You can\'t just set the name of the command as a string of `!`s -.-')
            return
        commandName = f'!{commandName}'.lower()

        # Get the content of the command
        await self.bot.say(f'What will the content of the command `{commandName}` be?')
        mes = await self.bot.wait_for_message(author=ctx.message.author)
        commandContent = mes.content

        # Validate it
        if not commandContent:
            await self.bot.say('You need to have content in the message - you can\'t send images or embeds.')
            return

        # Save it
        commands = self.cc
        commands[commandName] = commandContent
        saveFileJson('customCommands.json', commands)
        self.cc = commands

        # Return to user
        await self.bot.say('The command `{}` has been added.'.format(commandName))

    @tag.command(pass_context=True, aliases=['rem', 'del', 'delete'])
    @permissionChecker(check='administrator')
    async def remove(self, ctx, *, tagName:str=None):
        '''
        Remove a custom command from the bot
        '''

        # Get the tag name
        if not tagName:
            await self.bot.say('What is the name of the command that you want to delete?')
            mes = await self.bot.wait_for_message(author=ctx.message.author)
            tagName = mes.content
            if not tagName:
                await self.bot.say('You can\'t send an image or an embed as a tag name.')
                return

        tagName = tagName.lower()

        # Get the current commands
        if not self.cc.get(tagName):
            await self.bot.say('That currently isn\'t a custom command that\'s in my system.')
            return

        commands = self.cc 
        del self.cc[tagName]
        self.cc = commands
        saveFileJson('customCommands.json', commands)



def setup(bot):
    x = CustomCommands(bot)
    bot.add_cog(x)
