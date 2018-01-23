import vk
import logging

from constants import *
from DataBase import Data
from regularEXP import REXP


def start_logging():
    string = "%(asctime)s :%(levelname)-8s | FUNC: %(funcName)s | [LINE: %(lineno)d]: %(message)s"
    logfile = "logs.log"
    logging.basicConfig(format=string, filename=logfile, level=logging.DEBUG)
    logging.debug(" Bot started")


def makeVK_API():
    session = vk.Session(access_token=TOKEN_GROUP)
    vkAPI = vk.API(session, v='5.68')
    return vkAPI


def main():
    global vkAPI
    global DataBase
    global regularExp

    regularExp = REXP()
    start_logging()
    vkAPI = makeVK_API()
    DataBase = Data(FILE_BASE)

    while True:
        try:
            dictMessages = vkAPI.messages.getDialogs(unanswered=1)
        except:
            pass
        else:
            for eachMessageDict in dictMessages['items']:
                checkCommand(eachMessageDict)


def onlyRegistered():
    def checkRegistration(func):
        def wrapped(user_id):
            isRegistered = DataBase.isAccountRegistered(user_id)
            if isRegistered:
                return func(user_id)
            return CLASS_TIP

        return wrapped

    return checkRegistration


def onlyAdmin():
    def isUserAdmin(func):
        def wrapped(user_id, *args):
            isTeacher = DataBase.isTeacher(user_id)

            admins = vkAPI.groups.getMembers(group_id=GROUP_NUMBER, filter='managers')['items']

            admins = [admin['id'] for admin in admins]
            isAdmin = user_id in admins

            if isTeacher or isAdmin:
                return func(user_id, *args)

            logging.warning(
                "SOMEONE KNOW ABOUT TEACHER'S COMMAND: user_id = " + str(user_id) + " || " + str(func) + "(" +
                str(args) + ")")
            return ERROR_ANS

        return wrapped

    return isUserAdmin


def checkCommand(messageDict):
    fullString = messageDict['message']['body']
    stringCommand = fullString.split()[0].lower()
    user_id = messageDict['message']['user_id']

    simulateWriting(user_id)

    if getCommandExist(stringCommand):
        logging.debug(str(messageDict))

        messageToClient = activateFunction(messageDict, stringCommand)
        writeMessageToClient(messageToClient, user_id)
    else:
        writeMessageToClient(ERROR_ANS, user_id)


def writeMessageToClient(message, user_id):
    vkAPI.messages.send(user_id=user_id, message=message)


def simulateWriting(user_id):
    vkAPI.messages.setActivity(user_id=user_id, type='typing')


def activateFunction(message, stringCommand):
    stringText = message['message']['body'].strip()
    command, args = getCommandAndArgs(stringText, stringCommand)
    user_id = message['message']['user_id']

    # Сообщение откладки.
    logging.debug(str(message))
    if command == HELLO_WORD:
        return MESSAGE_HELLO
    elif command == HELP_WORD:
        return MESSAGE_COMMANDS
    elif command == CLASS_SET:
        return setUserClass(user_id, args)
    elif command == ADMIN_COMMAND_SEND:
        return sendMessagesFromTeacher(stringText)
    elif command == COMMAND_SPAM:
        return setSpamToClient(user_id)
    elif command == COMMAND_TEACHER_RESPONSE:
        return createLeaderResponse(user_id)
    elif command == COMMAND_TEACHER_LIST:
        return getLeaderResponseList(user_id)
    elif command == COMMAND_TEACHER_CONFIRM:
        return confirmLeaderResponse(user_id, stringText)
    elif command == COMMAND_TEACHER_DENY:
        return denyLeaderResponse(user_id, stringText)
    else:
        return ERROR_ANS


def sendMessagesFromTeacher(args):
    adminCommandSend = regularExp.getAdminSendCommand()

    isCorrect = adminCommandSend.search(args)

    if isCorrect:
        responseFromTeacher = isCorrect
        return prepareMassSpam(responseFromTeacher)
    else:
        return ADMIN_SEND_TIP


def prepareMassSpam(responseFromCTeacher):
    stringClassNumbers = responseFromCTeacher.group("classes")
    teacherContent = responseFromCTeacher.group("content")
    studentsID = []

    listClassesToSend = getListClassesToSend(stringClassNumbers)
    if listClassesToSend:
        for classToSend in listClassesToSend:

            if classToSend and len(classToSend) == 2:
                IDs = getAllStudentsFromClass(classToSend[0], classToSend[1])
                if IDs:
                    studentsID.append(IDs)
                else:
                    continue
            else:
                IDs = getAllStudentsFromClass(classToSend[0])
                if IDs:
                    studentsID.append(IDs)
                else:
                    continue

        if studentsID:
            compliteMassSpamByTeacher(studentsID, teacherContent)
            return SEND_SUCCSESSFUL
        else:
            return SEND_UNSUCCSESSFUL_NO_STUDENT_EXISTS
    else:
        return ADMIN_SEND_TIP


def compliteMassSpamByTeacher(listsOfIDs, teacherContent, photo=''):
    for oneListOfID in listsOfIDs:
        if oneListOfID:
            for eachPersonID in oneListOfID:
                writeMessageToClient(teacherContent, int(eachPersonID))
        else:
            continue


def getAllStudentsFromClass(classNumber, classChar=""):
    studentsID_list = []
    if classChar:
        studentsID = DataBase.getClassToSpam(classNumber, classChar)
        if studentsID:
            studentsID = studentsID[0]
    else:
        studentsID = DataBase.getClassToSpam(classNumber)
        if studentsID:
            studentsID = studentsID[0]

    studentsID_list = [int(studentID) for studentID in studentsID]

    return studentsID_list


def getListClassesToSend(stringClasses):
    """
        Метод, возвращающий лист классов с
    """
    isMoreThanOneClass = stringClasses.find(',')
    listToReturn = []

    if isMoreThanOneClass != -1:
        listOfClasses = stringClasses.split(',')

        for eachClass in listOfClasses:
            listOfClass = splitClass(eachClass, maybeOnlyNumber=True)

            if None not in listOfClass:
                listToReturn.append(listOfClass)
            else:
                return None

        return listToReturn
    else:
        formatedClass = splitClass(stringClasses, True)
        if None == formatedClass:
            return None
        return [formatedClass[0]]


@onlyAdmin()
def denyLeaderResponse(user_id, fulltext):
    regExp = regularExp.getDenyLeaderCommand()
    isCommandCorrect = regExp.search(fulltext)
    if isCommandCorrect:
        ID = int(isCommandCorrect.group('id'))
        isDeleted = DataBase.getLeaderResponseWithDelete(ID)
        if isDeleted:
            return TEACHER_DENY_MSG
        else:
            return ERROR
    else:
        return ERROR



@onlyRegistered()
def createLeaderResponse(user_id):
    """
     Метод, позволяющий создать запрос для добавляения в БД нового учителя.
    :param user_id:
    :return:
    """
    fullname = getName(user_id)
    DataBase.createLeaderResponse(user_id, fullname)
    return TEACHER_RESP_MSG


@onlyAdmin()
def confirmLeaderResponse(user_id, fulltext):
    """

    :param user_id:
    :return:
    """
    regExp = regularExp.getAcceptLeaderCommand()
    isCommandCorrect = regExp.search(fulltext)
    if isCommandCorrect:
        ID = int(isCommandCorrect.group('id'))
        isConfirmed = DataBase.confirmLeader(ID)
        if isConfirmed:
            user_id = isConfirmed
            logging.debug('NEW LEADER %d' % user_id)
            writeMessageToClient(YOU_TEACHER, user_id)
            return LEADER_CONFIRM_MSG
        else:
            return ERROR
    else:
        return ERROR


@onlyAdmin()
def getLeaderResponseList(user_id):
    """
    Позволяет админу узнать список запросов на добавление
        старосты.

    :param user_id:
    :return:
    """
    requests = DataBase.getLeadersResponseList()
    text = REQUESTS_LIST_FOR_ADMIN
    for request in requests:
        text += str(request[0]) + " - " + str(request[-1]) + "\n"
    if text == REQUESTS_LIST_FOR_ADMIN:
        text = REQUESTS_ARE_CLEAR_LIST_FOR_ADMIN
    return text


def getName(user_id):
    un_name = vkAPI.users.get(user_ids=user_id)
    first_name = un_name[0]['first_name']
    second_name = un_name[0]['last_name']
    name = first_name.title() + ' ' + second_name.title()
    return name


def setUserClass(user_id, writtenData):
    """
    Использовать re, чтобы проверить, что вторая часть - числа
    :param user_id:
    :param usersData:
    :return:
    """
    if writtenData:
        userClassNumber, userClassChar = splitClass(writtenData)

        if not (userClassNumber) or not (userClassChar):
            return CLASS_TIP

        if userClassChar and userClassNumber:
            DataBase.createOrUpdate_Student(user_id, userClassNumber, userClassChar)
            return MESSAGE_CLASS_REMEMBER

    else:
        return showUserClass(user_id)


def showUserClass(user_id):
    """
        Метод, позволяющий узнать класс пользователя.
    """
    userClass = DataBase.class_num(user_id)

    if userClass:
        return UR_CLASS % userClass

    return CLASS_IS_NOT_SET + "\n\n" + CLASS_TIP


def splitClass(unsplitedClass, maybeOnlyNumber=False):
    """

                Функция, позволяющая разбирать строку на цифру и букву класса.
                Принимает строку из полного значения цифрабуква (без пробелов)
    """
    unsplitedClass = unsplitedClass.strip()

    # Последний сивмол присваевается значению liter
    # Предполагается, что это будет буква.
    liter = unsplitedClass[-1]
    number = unsplitedClass[:-1]

    # Проверка на то, что последний символ является буквой.
    # isalpha() - вовзращает True, если это символ.
    if liter.isalpha():
        if number and number.isdigit() and 0 < int(number) <= 11:
            return [number, liter.upper()]
        else:
            return [None, None]
    else:
        if maybeOnlyNumber:
            number = unsplitedClass
            if number.isdigit() and 0 < int(number) <= 11:
                return [number]

        return [None, None]


@onlyRegistered()
def setSpamToClient(user_id):
    """
    Метод, который обновляет значения для рассылки спама (?)

    :param user_id: User client ID
    :type user_id: int

    :return: str
    """
    boolAnswerFromBD = DataBase.spam(user_id)
    if boolAnswerFromBD:
        return NOW_SPAM_YES
    else:
        return NOW_SPAM_NO


def getCommandAndArgs(unseporatedText, stringCommand):
    # Возвращать аргумент и команду
    """

    :param unseporatedText:
    :param stringCommand:
    :return:
    """

    args = unseporatedText.split(stringCommand)[-1]
    command = stringCommand.lower()

    return [command, args]


def getCommandExist(stringCommand):
    if stringCommand in COMMANDS:
        return True
    return False


"""
def getLogsForAdmin():
	with open("logs.log"):
		pass
"""

if __name__ in "__main__":
    print(ABOUT_BOT)
    main()
