from discord.ext import commands
from Cogs.Utils.Exceptions import *
from Cogs.Utils.FileHandling import getConfigs
from Cogs.Utils.Messages import messageToEmbed
from Cogs.Utils.PrintableMessage import PrintableMessage


class EventHandler(object):

	def __init__(self, bot):
		self.bot = bot
		self.logChannels, self.logMessages, self.privateMessages = getCogConfigurations(bot)

	async def on_message(self, message):
		'''
		Message handler for the bot. Prints debug messages.
		'''

		if server.id != self.serverSettings['Server ID']: return
		# print(PrintableMessage(message))
		# await self.bot.process_commands(message)

	async def on_message_delete(self, message):
		'''
		Logs deleted messages from users.
		'''

		if server.id != self.serverSettings['Server ID']: return
		em = messageToEmbed(message)
		await self.bot.send_message('This message was just deleted from {.memtion}.'.format(message.channel), embed=em)

	async def on_member_join(self, member):
		'''
		Triggered when a member joins the server.
		'''

		if server.id != self.serverSettings['Server ID']: return
		try:
			f = self.privateMessages['Joins'].format(user=member, server=member.server)
			await self.bot.send_message(member, f)
		except Exception:
			pass

		c = self.logChannels['Joins']
		f = self.logMessages['Joins'].format(user=member, server=member.server)
		await self.bot.send_message(c, f)

	async def on_member_remove(self, member):
		'''
		Triggered when a member is removed from (leaves, is kicked) the server.
		'''

		if server.id != self.serverSettings['Server ID']: return
		c = self.logChannels['Leaves']
		f = self.logMessages['Leaves'].format(user=member, server=member.server)
		await self.bot.send_message(c, f)

	async def on_member_ban(self, member):
		'''
		Triggered when a member is banned.
		'''

		if server.id != self.serverSettings['Server ID']: return
		c = self.logChannels['Bans']
		f = self.logMessages['Nonbot Bans'].format(user=member)
		await self.bot.send_message(c, f)

	async def on_member_unban(self, server, user):
		'''
		Triggered when a user is unbanned from a server.
		'''

		if server.id != self.serverSettings['Server ID']: return
		c = self.logChannels['Unbans']
		f = self.logMessages['Unbans'].format(user=member)
		await self.bot.send_message(c, f)

    async def on_command_error(self, error, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        toSay = None

        if isinstance(error, BotPermissionsTooLow):
            # This should run if the bot doesn't have permissions to do a thing to a user
            toSay = 'That user is too high ranked for me to perform that action on them.'
            
        elif isinstance(error, MemberPermissionsTooLow):
            # This should run if the member calling a command doens't have permission to call it
            toSay = 'That user is too high ranked for you to run that command on them.'
            
        elif isinstance(error, MemberMissingPermissions):
            # This should be run should the member calling the command not be able to run it
            toSay = 'You are missing the permissions required to run that command.'

        elif isinstance(error, BotMissingPermissions):
            # This should be run if the bot can't run what it needs to
            toSay = 'I\'m missing the permissions required to run this command.'

        elif isinstance(error, DoesntWorkInPrivate):
            # This is to be run if the command is sent in PM
            toSay = 'This command does not work in PMs.'
            
        elif isinstance(error, commands.errors.CheckFailure):
            # This should never really occur
            # This is if the command check fails
            toSay = 'Command check failed. Unknown error; please mention `Caleb#2831`.'
            
        else:
            # Who knows what happened? Not me. Raise the error again, and print to console
            print('Error on message :: Server{0.server.id} Author{0.author.id} Message{0.id} Content'.format(ctx.message), end='')
            try: print(ctx.message.content + '\n')
            except: print('Could not print.' + '\n')
            raise(error)

        if toSay:
            await self.bot.send_message(channel, toSay)


def setup(bot):
	x = EventHandler(bot)
	bot.add_cog(x)
