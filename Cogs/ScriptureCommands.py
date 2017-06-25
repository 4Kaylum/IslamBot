from re import match
from json import loads
from collections import OrderedDict
from aiohttp import ClientSession
from discord.ext import commands
from Cogs.Utils.Messages import makeEmbed


class Scriptures(object):

    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        self.session = ClientSession(loop=bot.loop)
        self.regexMatches = {
            'OriginalRequest': r'(.+[a-zA-Z0-9]+\s[0-9]+:[0-9]+(-[0-9]+)?)',
            'StripAuthor': r'(.+\b)([0-9]+:)',
            'GetPassages': r'([0-9]+:[0-9]+)',
            'GetMax': r'(-[0-9]+)',
            'QuranMatch': r''
        }
        self.biblePicture = 'http://pacificbible.com/wp/wp-content/uploads/2015/03/holy-bible.png'
        self.quranPicture = 'http://www.siotw.org/modules/burnaquran/images/quran.gif'

    def __unload(self):
        self.session.close()

    @commands.command(pass_context=True)
    async def bible(self, *, script:str):
        '''
        Gives you the Christian Bible quote from a specific script
        '''

        # Check if it's a valid request
        matches = match(self.regexMatches['OriginalRequest'], script)
        if not matches:
            self.bot.say('That string was malformed, and could not be processed. Please try again.')
            return
        else:
            script = matches.group()

        # It is - send it to the API
        async with self.session.get('https://getbible.net/json?scrip={}'.format(script)) as r:
            try:
                apiData = await r.json()
            except:
                apiData == None

        # Just check if it's something that we can process
        if not apiData:
            await self.bot.say('I was unable to get that paricular Bible passage. Please try again.')

        # Now we do some processin'
        # Get the max and the min verse numbers
        chapterMin = int(match(self.regexMatches['GetPassages'], script).group().split(':')[1])
        chapterMax = match(self.regexMatches['GetMax'], script)
        if chapterMax:
            chapterMax = int(chapterMax.group()) + 1
        else:
            chapterMax = chapterMin + 1

        # Process them into an ordered dict
        o = OrderedDict()
        passages = apiData['book'][0]['chapter']
        for verse in range(chapterMin, chapterMax):
            o[verse] = passages[str(verse)]['verse']

        # Make it into an embed
        author = match(self.regexMatches['StripAuthor'], script).group().title()
        em = makeEmbed(fields=o, author=author, author_icon=self.biblePicture)

        # And done c:
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def quran(self, ctx, *, script:str):
        '''
        Gives you a Quran quote given a specific verse
        '''

        pass


def setup(bot):
    x = Scriptures(bot)
    bot.add_cog(x)
