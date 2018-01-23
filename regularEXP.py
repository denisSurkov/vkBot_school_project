import re

class REXP:

    def __init__(self):

        self.adminSendCommand = re.compile(r"""
            ^(отправить)\s?
            (?P<classes>(\s?[0-9][0-9]?[а-яёЁА-Я]?\s?,?)+)\s?
            (сообщение|Сообщение)\s+
            (?P<content>.*)""", re.VERBOSE)
        self.acceptLeader = re.compile(r"^(подтвердить|Подтвердить)\s+(?P<id>\d*)")
        self.denyLeader = re.compile(r"^(отклонить|Отклонить)\s+(?P<id>\d*)")

        #self.onlySelfLogs = re.compile("""%(asctime)s :%(levelname)-8s | FUNC: %(funcName)s | [LINE: %(lineno)d]: %(message)s""")

    def getAdminSendCommand(self):
        return self.adminSendCommand

    def getAcceptLeaderCommand(self):
        return self.acceptLeader

    def getDenyLeaderCommand(self):
        return self.denyLeader

