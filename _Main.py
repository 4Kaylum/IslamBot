from sys import argv
import discord
from discord.ext import commands


description = '''Bot indended for use on the r/Islam Discord server.
Created by Caleb#2831'''


def getCommandPrefix(bot, message):
	return ['\'', '{.mention} '.format(bot.user)]


bot = commands.Bot(
	command_prefix=getCommandPrefix,
	description=description,
	pm_help=True
)


# Generate files if they don't exist
necessaryFiles = ['bible.json', 'customCommands.json', 'userMoney.json', 'buyableRoles.json', 'userWarns.json']
for i in necessaryFiles:
    try:
        with open('./Storage/{}'.format(i)) as a:
            pass
    except FileNotFoundError:
        with open('./Storage/{}'.format(i), 'w') as a:
            a.write('{}')


initialExtentions = [
    'EventHandler',
    'ScriptureCommands',
    'UserModeration',
    'UserMoney',
    'UserWarnings',
    'OwnerOnlyCommands',
    'MiscCommands',
    'CustomCommands',
    'RoleModeration',
]


@bot.event
async def on_ready():
    # Some classic prints
    print('-----')
    print('User :: {}'.format(bot.user))
    print('ID :: {}'.format(bot.user.id))
    print('-----')

    # Nicely set the game
    game = '.help'
    await bot.change_presence(game=discord.Game(name=game))

    # Load up all the extentions
    for extension in initialExtentions:

        # This is necessary because I'm bad at code
        try:
            bot.load_extension('Cogs.'+extension)

        # Print out any errors
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(argv[1])
