from datetime import datetime, timedelta
from random import randint
from Cogs.Utils.FileHandling import getFileJson, saveFileJson

class UserModel(object):

    def __init__(self, message):
        # self.lastSent = message.timestamp
        self.lastSent = 0
        # self.changeAmount(message.author.id)

    def timeCheck(self, message):
        if datetime.now() > self.lastSent + timedelta(seconds=30):
            self.lastSent = datetime.now()
            return True 
        else:
            return False

    def changeAmount(self, authorID):
        jsonData = getFileJson('userMoney.json')
        changeInt = randint(5, 10)
        currentMoney = jsonData.get(authorID, 0)

        # Change stored data
        currentMoney += changeInt
        jsonData[authorID] = currentMoney
        saveFileJson('userMoney.json', jsonData)

    def onMessage(self, message):
        if self.timeCheck(message):
            self.changeAmount(message.author.id)
        return


class Banker(object):

    def __init__(self):
        self.handled = {}  # UserID: UserModel

    def handle(self, message):
        author = message.author.id
        userObj = self.handled.get(author)
        if not userObj:
            userObj = UserModel(message)
            self.handled[author] = userObj
        userObj.onMessage(message)
