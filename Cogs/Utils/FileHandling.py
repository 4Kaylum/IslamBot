from json import loads, dumps


if '\\' in __file__:
    cwd = '/'.join(__file__.split('\\')[:-1])
else:
    cwd = '/'.join(__file__.split('/')[:-1])


def getFileJson(jsonName):
    '''
    Gets the json file and dumps/returns it.
    '''

    # Reads from the file
    with open(cwd + '/../../Storage/{}'.format(jsonName)) as a:
        data = a.read()

    # Loads it into a dictionary to return it
    return loads(data)


def saveFileJson(jsonName, jsonData):
    '''
    Saves some data into a json file
    '''

    # Makes it look nice
    data = dumps(jsonData, indent=4)

    # Puts it into the file
    with open(cwd + '/../../Storage/{}'.format(jsonName), 'w') as a:
        a.write(data)


def getCogConfigurations(bot):
    serverSettings = getFileJson('Configs.json')
    mainServerID = serverSettings['Server ID']
    mainServer = bot.get_server(mainServerID)

    logChannels = {}
    logMessages = serverSettings['Messages']['Logs']
    privateMessages = serverSettings['Messages']['PMs']

    for i, o in serverSettings['Channels'].items():
        logChannels[i] = mainServer.get_channel(o)

    return logChannels, logMessages, privateMessages, serverSettings
