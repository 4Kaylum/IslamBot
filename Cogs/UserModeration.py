from discord import Member
from discord.ext import commands
from Cogs.Utils.FileHandling import getCogConfigurations, getFileJson
from Cogs.Utils.Permissions import permissionChecker 


class UserModeration(object):

    def __init__(self, bot):
        self.bot = bot 
        self.jailRoleID = getFileJson('Configs.json')['Jail Role']
        self.jailRole = None
        self.logChannels, self.logMessages, self.privateMessages, self.serverSettings = getCogConfigurations(bot)

    @commands.command(pass_context=True)
    @permissionChecker(check='ban_members', compare=True)
    async def ban(self, ctx, user:Member, *, reason:str=None):
        '''
        Bans a user from the server.
        '''

        # Require a reason
        if reason == None:
            await self.bot.say('You need to provide a reason for your ban.')
            return 

        # Set up local variable
        moderator = ctx.message.author
        if user == moderator:
            await self.bot.say('You\'re an idiot.')
            return

        # Try to send a message to the banned user
        try:
            f = self.privateMessages['Bans'].format(user=member, moderator=moderator, reason=reason)            
            await self.bot.send_message(user, f)
        except Exception:
            pass 

        # Ban the user
        try:
            await self.bot.ban(user, delete_message_days=0)
        except Exception:
            await self.bot.say('I was unable to ban that user.')
            return

        # Send a message back to the user
        await self.bot.say('👌 This user has been banned for reason `{}`.'.format(reason))

        # Send a message to the modlogs
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Bans']
        f = self.logMessages['Bans'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)

    @commands.command(pass_context=True)
    @permissionChecker(check='ban_members', compare=True)
    async def dban(self, ctx, user:Member, *, reason:str=None):
        '''
        Bans a user from the server.
        '''

        # Require a reason
        if reason == None:
            await self.bot.say('You need to provide a reason for your ban.')
            return 

        # Set up local variable
        moderator = ctx.message.author
        if user == moderator:
            await self.bot.say('You\'re an idiot.')
            return

        # Try to send a message to the banned user
        try:
            f = self.privateMessages['Bans'].format(user=member, moderator=moderator, reason=reason)            
            await self.bot.send_message(user, f)
        except Exception:
            pass 

        # Ban the user
        try:
            await self.bot.ban(user, delete_message_days=1)
        except Exception:
            await self.bot.say('I was unable to ban that user.')
            return

        # Send a message back to the user
        await self.bot.say('👌 This user has been banned for reason `{}`.'.format(reason))

        # Send a message to the modlogs
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Bans']
        f = self.logMessages['Bans'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)

    @commands.command(pass_context=True)
    @permissionChecker(check='kick_members', compare=True)
    async def kick(self, ctx, user:Member, *, reason:str=None):
        '''
        Bans a user from the server.
        '''

        # Require a reason
        if reason == None:
            await self.bot.say('You need to provide a reason for your kick.')
            return 

        # Set up local variable
        moderator = ctx.message.author
        if user == moderator:
            await self.bot.say('You\'re an idiot.')
            return

        # Try to send a message to the banned user
        try:
            f = self.privateMessages['Kicks'].format(user=member, moderator=moderator, reason=reason)            
            await self.bot.send_message(user, f)
        except Exception:
            pass 

        # Ban the user
        try:
            await self.bot.kick(user)
        except Exception:
            await self.bot.say('I was unable to kick that user.')
            return

        # Send a message back to the user
        await self.bot.say('👌 This user has been kicked for reason `{}`.'.format(reason))

        # Send a message to the modlogs
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Kicks']
        f = self.logMessages['Kicks'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)

    @commands.command(pass_context=True)
    @permissionChecker(check='kick_members', compare=True)
    async def jail(self, ctx, user:Member, *, reason:str='None'):
        '''
        Jails a user on the server
        '''

        # Set up local variable
        moderator = ctx.message.author
        if user == moderator:
            await self.bot.say('You\'re an idiot.')
            return

        # See if the jail role has been set up
        if self.jailRole:
            pass
        else:
            self.jailRole = [i for i in ctx.message.server.roles if i.id == self.jailRoleID][0]

        await self.bot.add_roles(user, self.jailRole)

        # Send a message back to the user
        await self.bot.say('👌 This user has been jailed for reason `{}`.'.format(reason))

        # Send a message to the modlogs
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Jailed']
        f = self.logMessages['Jailed'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)

    @commands.command(pass_context=True)
    @permissionChecker(check='kick_members')
    async def unjail(self, ctx, user:Member, *, reason:str='None'):
        '''
        Jails a user on the server
        '''

        # Set up local variable
        moderator = ctx.message.author
        if user == moderator:
            await self.bot.say('You\'re an idiot.')
            return

        # See if the jail role has been set up
        if self.jailRole:
            pass
        else:
            self.jailRole = [i for i in ctx.message.server.roles if i.id == self.jailRoleID][0]

        await self.bot.remove_roles(user, self.jailRole)

        # Send a message back to the user
        await self.bot.say('👌 This user has been unjailed for reason `{}`.'.format(reason))

        # Send a message to the modlogs
        if ctx.message.server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Unjailed']
        f = self.logMessages['Unjailed'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)


def setup(bot):
    x = UserModeration(bot)
    bot.add_cog(x)
