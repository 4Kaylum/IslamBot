from re import finditer
from json import loads
from collections import OrderedDict
from aiohttp import ClientSession
from urllib.parse import quote, unquote
from html import unescape
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
        self.hadithPicture = 'https://sunnah.com/images/hadith_icon2_huge.png'

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

    @commands.command(pass_context=True)
    async def hadith(self, ctx, bookAuthor:str, bookNumber:str, hadithNumber:str=None):
        '''
        Gets a particular hadith
        '''

        # Get the hadith number and book numbers into the right variables
        if not hadithNumber:
            if not ':' in bookNumber:
                await self.bot.say('That is not a valid format to get a Hadith.'
                    'Please see this command\'s help message.')
                return
            bookNumber, hadithNumber = [i.strip() for i in bookNumber.split(':')]

        await self.bot.send_typing(ctx.message.channel)

        # Special case book authors are sucky
        bookAuthor = {'qudsi':'qudsi40','nawawi':'nawawi40'}.get(bookAuthor.lower(), bookAuthor.lower())

        # Grab the links from the site
        # print(f'https://sunnah.com/{bookAuthor}/{bookNumber}/{hadithNumber}')
        siteURL = f'https://sunnah.com/{bookAuthor}/{bookNumber}/{hadithNumber}'
        async with self.session.get(siteURL) as r:
            siteText = await r.text()

        # Make sure it's a valid set of text
        if 'You have entered an incorrect URL. Please use the menu above to navigate the website.' in siteText:
            await self.bot.say('You\'ve submitted an incorrect format for the Hadith parsing.'
                'Please see this command\'s help message.')

        # Parse from the site
        siteSplit = siteText.replace('\n', '').replace('<i>', '*').replace('</i>', '*')
        regexString = r'<div class=\"englishcontainer\" id=t[0-9]+><div class=\"english_hadith_full\">' + \
                      r'<div class=hadith_narrated><p>.+</div><div class=text_details>.+</b></div>'
        matches = match(regexString, siteSplit).group()
        regexString = r'<div class=hadith_narrated><p>.+</div><'
        siteFrom = match(regexString, matches).group().split('>')[2].split('<')[0].strip()
        regexString = r'<div class=text_details>.+</b>'
        siteText = match(regexString, matches).group().split('>')[2].split('<')[0].strip()

        # Generate the embed
        bookAuthor = {
            'bukhari':'Sahih Bukhari',
            'muslim':'Sahih Muslim',
            'tirmidhi':'Jami` at-Tirmidhi',
            'abudawud':'Sunan Abi Dawud',
            'nasai':"Sunan an-Nasa'i",
            'ibnmajah':'Sunan Ibn Majah',
            'malik':'Muwatta Malik',
            'riyadussaliheen':'Riyad as-Salihin',
            'adab':"Al-Adab Al-Mufrad",
            'bulugh':'Bulugh al-Maram',
            'qudsi40':'40 Hadith Qudsi',
            'nawawi40':'40 Hadith Nawawi'
        }.get(bookAuthor, bookAuthor)
        author = f'{bookAuthor} {bookNumber}:{hadithNumber}'.title()
        em = makeEmbed(fields={siteFrom:siteText}, author=author, colour=0x78c741, author_icon=self.hadithPicture, author_url=siteURL)
        try:
            await self.bot.say(embed=em)
        except Exception:
            em = makeEmbed(fields={siteFrom:siteText[:800]+'...'}, author=author, colour=0x78c741, author_icon=self.hadithPicture, author_url=siteURL)
            await self.bot.say('That was too long to get fully. Here\'s the best I can do:', embed=em)
        # print(f'author: {author}' + str({siteFrom:siteText}))
        # await self.bot.say(len(str({siteFrom:siteText})))


def setup(bot):
    x = Scriptures(bot)
    bot.add_cog(x)
