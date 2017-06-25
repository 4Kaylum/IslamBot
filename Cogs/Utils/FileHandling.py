from json import loads


def getFileJson(jsonName):
    '''
    Gets the json file and dumps/returns it.
    '''

    # Reads from the file
    with open(workingDirectory + '/../Storage/{}'.format(jsonName)) as a:
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
    with open(workingDirectory + '/../Storage/{}'.format(jsonName), 'w') as a:
        a.write(data)


def getConfigs():
    return getJson('Storage/Configs.json')


def getCogConfigurations(bot):
    serverSettings = getConfigs()
    mainServerID = serverSettings['Server ID']
    mainServer = bot.get_server(mainServerID)

    logChannels = {}
    logMessages = serverSettings['Messages']['Logs']
    privateMessages = serverSettings['Messages']['PMs']

    for i, o in serverSettings['Channels'].items():
        logChannels[i] = mainServer.get_channel(o)

    return logChannels, logMessages, privateMessages
