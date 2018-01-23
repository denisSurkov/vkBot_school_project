
# Константа SQL базы данных.
FILE_BASE = 'group_data.db'

# Константа токена группы.
TOKEN_GROUP = ""

# Константа номера группы.
GROUP_NUMBER = '142645986'

""" Простые ответы на сообщения. """
MESSAGE_HELLO = '''&#128521; Привет! \n\n &#127760; Я бот группы вконтакте МАОУ СОШ №19. 
                   &#128172; Чтобы посмотреть мои команды, введи "помощь".'''
MESSAGE_CLASS_REMEMBER = '&#10004; Отлично, я запомнил твой класс.'
ERROR_ANS = '&#128558; Прости, я тебя не понимаю. \n\n &#128221; Введи "помощь", чтобы узнать все команды.'
MESSAGE_COMMANDS = '''&#128242;  Мои команды: \n
                   \t Класс - позволяет установить твой класс;
                   \t Настройки - выводит твои настройки;
                   \t Рассылка - позволяет включить\отключить рассылку;
                   \n &#128284;  Команды будут дополняться.'''
ERROR_ANS_UNC_CLASS = '&#9940; Ошибка!'
UR_CLASS = '&#128218; Ваш класс %s'
NOW_SPAM_NO = '&#128235; Теперь вам не будут рассылать сообщения.'
NOW_SPAM_YES = '&#128237; Теперь вам будут рассылаться новости по вашей параллели.'
CLASS_TIP = '''&#128172; Используй: Класс (номер вашего класса)" 
               \n &#128270; Пример: Класс 9Б'''
SETTINGS_NONE = '''{0}, я не могу вывести твои настройки. 
                  \n Возможно, у тебя не указан класс ("класс").'''
ADMIN_SEND_STATUS = '''Сообщение: {0} \n\n Было отправлено {1} пользователям. 
                       \n Отправил сообщение администратор {2}'''
ADMIN_SEND_TIP = '''&#128172; Используйте:
                    отправить (цифра класса, или множества классов) Сообщение (сообщение) \n
                    &#128270; Пример: отправить 9А, 10 Сообщение Добрый день, старшеклассники! 
                    Завтра есть изменения в расписании, просьба всех ознакомиться.'''
ADMIN_COMMANDS = 'Команды администратора.'
LEADER_CONFIRM_MSG = '&#10004; Заявка подтверждена.'
TEACHER_DENY_MSG = '&#10060; Заявка отклонена.'
TEACHER_RESP_MSG = '&#10004; Ваша заявка отправлена!'
REQUESTS_LIST_FOR_ADMIN = '&#128270; Текущие заявки: \n'
REQUESTS_ARE_CLEAR_LIST_FOR_ADMIN = '&#128270; Заявок нет.'
ERROR = '&#9940; Ошибка'
SPAM_SET_YES = '&#128237; Рассылка сообщений включена'
SPAM_SET_NO = '&#128235; Рассылка сообщений отключена'
YOU_TEACHER = '&#128214; Вы староста'
CLASS_IS_NOT_SET = '&#128172; У тебя не указан класс.'
SEND_SUCCSESSFUL = '&#10004; Сообщение отправлены.'
SEND_UNSUCCSESSFUL_NO_STUDENT_EXISTS = "&#128172; Сообщения не отправлены, поскольку "
SEND_UNSUCCSESSFUL_NO_STUDENT_EXISTS += " нет зарегистрированных из данных классов, либо все отключили рассылку."

EMPTY_MESSAGE_ERORR = ERROR + "\n\n" + "&#9940; Нельзя отправлять пустые сообщения."

""" Основные команды бота без аргументов. """
HELLO_WORD = 'привет'
HELP_WORD = 'помощь'
CLASS_SET = 'класс'
#ADMINS_ALL_COMMAND = 'админ'
COMMAND_SPAM = 'рассылка'
MY_SETTINGS = 'настройки'
ADMIN_COMMAND_SEND = 'отправить'
COMMAND_TEACHER_RESPONSE = 'староста'
COMMAND_TEACHER_LIST = 'заявки'
COMMAND_TEACHER_CONFIRM = 'подтвердить'
COMMAND_TEACHER_DENY = 'отклонить'
COMMANDS = [HELLO_WORD, HELP_WORD, CLASS_SET,
            MY_SETTINGS, ADMIN_COMMAND_SEND,
            COMMAND_SPAM,
            COMMAND_TEACHER_RESPONSE,
            COMMAND_TEACHER_LIST, COMMAND_TEACHER_CONFIRM, COMMAND_TEACHER_DENY]

ABOUT_BOT = """ 
            |\t CHAT - BOT FOR GROUP IN SOCIAL NETWORK VKONTAKTE \t|
            |\t ALL STRINGS CONSTANTS ARE IN String_constatns.py \t|
            |\t ALL LOGS ARE IN TXT FILES (String_constatns.py)  \t|
            |\t MADE BY DENIS SURKOV IN 2018                     \t|"""