class PrintableMessage(object):
    MAX_TIMESTAMP_LENGTH = 26
    MAX_PRIVATE_BOOL = 6
    MAX_GUILD_NAME = 15
    MAX_GUILD_ID = 18
    MAX_CHANNEL_NAME = 12
    MAX_CHANNEL_ID = 18
    MAX_AUTHOR_NAME = 15
    MAX_AUTHOR_ID = 18
    MAX_MESSAGE_CONTENT = 50
    MAX_MESSAGE_ID = 18

    def __init__(self, message):
        self.message = message 
        self.guild = message.server 
        self.channel = message.channel if self.guild else 'None'
        self.author = message.author
        self.content = message.clean_content.replace('\n', '\\n')
        self.private = False if self.guild else True
        self.full = ' :: '.join(self.getOutput())

    def getOutput(self):
        workingOutput = []

        # Add on the timestamp
        timestamp = str(self.message.timestamp)[:PrintableMessage.MAX_TIMESTAMP_LENGTH]
        if len(timestamp) < PrintableMessage.MAX_TIMESTAMP_LENGTH:
            timestamp = ' ' * (PrintableMessage.MAX_TIMESTAMP_LENGTH - len(timestamp)) + timestamp 
        workingOutput.append(timestamp)

        # Add on the boolean for server or PMs
        private = {False:'Server',True:'PMs'}[self.private]
        if len(private) < PrintableMessage.MAX_PRIVATE_BOOL:
            private = ' ' * (PrintableMessage.MAX_PRIVATE_BOOL - len(private)) + private 
        workingOutput.append(private)

        # Plonk on the guild name
        guildName = self.guild.name[:PrintableMessage.MAX_GUILD_NAME] if self.guild else 'None'
        if len(guildName) < PrintableMessage.MAX_GUILD_NAME:
            guildName = ' ' * (PrintableMessage.MAX_GUILD_NAME - len(guildName)) + guildName 
        workingOutput.append(guildName)

        # Plonk on the guild ID
        guildID = self.guild.id[:PrintableMessage.MAX_GUILD_ID] if self.guild else 'None'
        if len(guildID) < PrintableMessage.MAX_GUILD_ID:
            guildID = ' ' * (PrintableMessage.MAX_GUILD_ID - len(guildID)) + guildID 
        workingOutput.append(guildID)

        # Plonk on the guild name
        channelName = self.channel.name[:PrintableMessage.MAX_CHANNEL_NAME] if self.guild else 'None'
        if len(channelName) < PrintableMessage.MAX_CHANNEL_NAME:
            channelName = ' ' * (PrintableMessage.MAX_CHANNEL_NAME - len(channelName)) + channelName 
        workingOutput.append(channelName)

        # Plonk on the guild ID
        channelID = self.channel.id[:PrintableMessage.MAX_CHANNEL_ID] if self.guild else 'None'
        if len(channelID) < PrintableMessage.MAX_CHANNEL_ID:
            channelID = ' ' * (PrintableMessage.MAX_CHANNEL_ID - len(channelID)) + channelID 
        workingOutput.append(channelID)

        # Plonk on the author name
        authorName = self.author.name[:PrintableMessage.MAX_AUTHOR_NAME]
        if len(authorName) < PrintableMessage.MAX_AUTHOR_NAME:
            authorName = ' ' * (PrintableMessage.MAX_AUTHOR_NAME - len(authorName)) + authorName 
        workingOutput.append(authorName)

        # Plonk on the author ID
        authorID = self.author.id[:PrintableMessage.MAX_AUTHOR_ID]
        if len(authorID) < PrintableMessage.MAX_AUTHOR_ID:
            authorID = ' ' * (PrintableMessage.MAX_AUTHOR_ID - len(authorID)) + authorID 
        workingOutput.append(authorID)

        # Plonk on the message content
        messageContent = self.content[:PrintableMessage.MAX_MESSAGE_CONTENT]
        if len(messageContent) < PrintableMessage.MAX_MESSAGE_CONTENT:
            messageContent = ' ' * (PrintableMessage.MAX_MESSAGE_CONTENT - len(messageContent)) + messageContent 
        workingOutput.append(messageContent)

        # Plonk on the message content
        messageID = self.message.id[:PrintableMessage.MAX_MESSAGE_ID]
        if len(messageID) < PrintableMessage.MAX_MESSAGE_ID:
            messageID = ' ' * (PrintableMessage.MAX_MESSAGE_ID - len(messageID)) + messageID 
        workingOutput.append(messageID)

        return workingOutput

    def __repr__(self):
        return self.full
