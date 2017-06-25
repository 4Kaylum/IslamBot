from discord import Member
from discord.ext import commands
from Cogs.Utils.FileHandling import getCogConfigurations
from Cogs.Utils.Permissions import permissionChecker 


class UserModeration(object):

    def __init__(self, bot):
        self.bot = bot 
        self.logChannels, self.logMessages, self.privateMessages = getCogConfigurations(bot)

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
        if server.id != self.serverSettings['Server ID']: return
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
        if server.id != self.serverSettings['Server ID']: return
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
        if server.id != self.serverSettings['Server ID']: return
        c = self.logChannels['Kicks']
        f = self.logMessages['Kicks'].format(user=member, moderator=moderator, reason=reason)
        await self.bot.send_message(c, f)


def setup(bot):
    x = UserModeration(bot)
    bot.add_cog(x)
