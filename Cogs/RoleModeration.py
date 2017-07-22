from discord.ext import commands
from Cogs.Utils.FileHandling import getFileJson, saveFileJson
from Cogs.Utils.Permissions import permissionChecker 


class RoleModeration(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @permissionChecker(check='manage_roles')
    async def buyablerole(self, ctx):
        '''
        Manage the roles that users can buy on the server
        '''

        pass

    @buyablerole.command(pass_context=True)
    @permissionChecker(check='manage_roles')
    async def add(self, price:int, *, roleName:str):
        '''
        Add a role that users can buy
        '''

        if price < 0:
            await self.bot.say('Nice try, buddy. Making the price below 0? Despicable. You make me sick.')
            return

        roleData = getFileJson('buyableRoles.json')
        serverRoles = list(ctx.message.roles)

        # Determine what role they were trying to search for
        wantedRole = [i for i in serverRoles if roleName.lower() in i.name.lower() or roleName == i.id]

        # Determine if that role exists
        if len(wantedRole) == 0:
            await self.bot.say('There were no roles that matched the hitstring `{}`.'.format(roleName))
            return
        elif len(wantedRole) > 1:
            v = 'There were multiple roles that matched the hitstring `{}`; \n* {}'.format(roleName, '\n* '.join(wantedRole))
            await self.bot.say(v)
            return
        else:
            # There was only one role that matched that hitstring
            pass

        r = wantedRole[0]
        roleData[r.id] = price
        saveFileJson('buyableRoles.json', roleData)
        await self.bot.say(f'The role `{r.name}` (`{r.id}`) has been added as a buyable role for `{price}` credits.')

    @buyablerole.command(pass_context=True, aliases=['rem', 'del', 'delete'])
    @permissionChecker(check='manage_roles')
    async def remove(self, *, roleName:str):
        '''
        Remove a role that users can buy
        '''

        roleData = getFileJson('buyableRoles.json')
        roleIDs = list(roleData.keys())
        serverRoles = list(ctx.message.roles)
        availableRoles = [i for i in serverRoles if i.id in roleIDs]

        # Determine what role they were trying to search for
        wantedRole = [i for i in availableRoles if roleName.lower() in i.name.lower() or roleName == i.id]

        # Determine if that role exists
        if len(wantedRole) == 0:
            await self.bot.say('There were no roles that matched the hitstring `{}`.'.format(roleName))
            return
        elif len(wantedRole) > 1:
            v = 'There were multiple roles that matched the hitstring `{}`; \n* {}'.format(roleName, '\n* '.join(wantedRole))
            await self.bot.say(v)
            return
        else:
            # There was only one role that matched that hitstring
            pass

        try:
            del roleData[wantedRole[0]]
        except Exception as e:
            pass

        r = wantedRole[0]
        await self.bot.say(f'The role `{r.name}` (`{r.id}`) has been successfully deleted as a buyable role.')


def setup(bot):
    x = RoleModeration(bot)
    bot.add_cog(x)
