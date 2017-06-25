from re import finditer
from json import loads
from collections import OrderedDict
from aiohttp import ClientSession
from urllib.parse import quote, unquote
from discord.ext import commands
from Cogs.Utils.Messages import makeEmbed
from Cogs.Utils.Permissions import hasRoles 


def match(pattern, string):
    q = finditer(pattern, string)
    try:
        return list(q)[0]
    except IndexError:
        return None


class Scriptures(object):

    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        self.session = ClientSession(loop=bot.loop)
        self.regexMatches = {
            'OriginalRequest': r'(.+[a-zA-Z0-9]+\s[0-9]+:[0-9]+(-[0-9]+)?)',
            'StripAuthor': r'(.+\b)([0-9]+:)',
            'GetPassages': r'([0-9]+:[0-9]+)',
            'GetMax': r'(-[0-9]+)',
            'QuranMatch': r'([0-9]+:[0-9]+([-0-9]+)?)'
        }
        self.biblePicture = 'http://pacificbible.com/wp/wp-content/uploads/2015/03/holy-bible.png'
        self.quranPicture = 'http://www.siotw.org/modules/burnaquran/images/quran.gif'

    def __unload(self):
        self.session.close()

    @commands.command(pass_context=True)
    @hasRoles()
    async def bible(self, ctx, *, script:str):
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
        await self.bot.send_typing(ctx.message.channel)

        # Actually do some processing
        script = quote(script, safe='')
        async with self.session.get('https://getbible.net/json?scrip={}'.format(script)) as r:
            try:
                apiText = await r.text()
                apiData = loads(apiText[1:-2])
            except Exception as e:
                apiData = None
        script = unquote(script)

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

    async def getQuran(self, number, mini, maxi, english=True):
        '''
        Sends stuff off to the API to be processed, returns embed object
        '''

        o = OrderedDict()
        if english:
            base = 'http://api.alquran.cloud/ayah/{}:{}/en.sahih'
        else:
            base = 'http://api.alquran.cloud/ayah/{}:{}'

        # Get the data from the API
        async with self.session.get(base.format(number, mini)) as r:
            data = await r.json()

        author = data['data']['surah']['englishName'] if english else data['data']['surah']['name']
        o['{}:{}'.format(number, mini)] = data['data']['text']

        for verse in range(mini+1, maxi):
            async with self.session.get(base.format(number, verse)) as r:
                data = await r.json()
            o['{}:{}'.format(number, verse)] = data['data']['text']

        em = makeEmbed(fields=o, author=author, author_icon=self.quranPicture)
        return em

    @commands.command(pass_context=True)
    @hasRoles()
    async def quran(self, ctx, *, script:str):
        '''
        Gives you a Quran quote given a specific verse
        '''

        # http://api.alquran.cloud/ayah/{}/en.sahih

        # Check if it's a valid request
        matches = match(self.regexMatches['QuranMatch'], script)
        if not matches:
            self.bot.say('That string was malformed, and could not be processed. Please try again.')
            return
        else:
            script = matches.group()

        # It is - prepare to send it to an API
        await self.bot.send_typing(ctx.message.channel)

        # Acutally do some processing
        number = int(script.split(':')[0])
        minQuote = int(script.split(':')[1].split('-')[0])
        try:
            maxQuote = int(script.split(':')[1].split('-')[1]) + 1
        except IndexError as e:
            maxQuote = minQuote + 1

        # Send it off nicely to the API to be processed
        em = await self.getQuran(number, minQuote, maxQuote)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    @hasRoles()
    async def aquran(self, ctx, *, script:str):
        '''
        Gives you a Quran quote given a specific verse
        '''

        # http://api.alquran.cloud/ayah/{}/en.sahih

        # Check if it's a valid request
        matches = match(self.regexMatches['QuranMatch'], script)
        if not matches:
            self.bot.say('That string was malformed, and could not be processed. Please try again.')
            return
        else:
            script = matches.group()

        # It is - prepare to send it to an API
        await self.bot.send_typing(ctx.message.channel)

        # Acutally do some processing
        number = int(script.split(':')[0])
        minQuote = int(script.split(':')[1].split('-')[0])
        try:
            maxQuote = int(script.split(':')[1].split('-')[1]) + 1
        except IndexError as e:
            maxQuote = minQuote + 1

        # Send it off nicely to the API to be processed
        em = await self.getQuran(number, minQuote, maxQuote, False)
        await self.bot.say(embed=em)


def setup(bot):
    x = Scriptures(bot)
    bot.add_cog(x)
