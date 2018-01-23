class Data:
    """ Класс с методами для БД. """

    def __init__(self, FILE_BASE):
        """ Инициализация. """
        import sqlite3
        self.connect = sqlite3.connect(FILE_BASE)  # Коннект к базе данных.
        self.cursor = self.connect.cursor()  # Курсор.
        self._create_table()
        self._create_Requests_table()
        self._createView()
        # self.cursor.execute('DROP TABLE students')
        # self.cursor.execute('DROP TABLE requests')

    def _create_table(self):
        """ Метод, создающий таблицы в БД. """

        # Основная таблица студентов.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                            class_number INTEGER NOT NULL,
                            class_char VARCHAR(1) NOT NULL,
                            messages_spam INTEGER DEFAULT 1,
                            status INTEGER DEFAULT 0)''')
        self.connect.commit()

        # Отдельная таблица для запросов учителей.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS requests(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL UNIQUE,
                            teacher_name STRING,
                            class_number INTEGER NOT NULL,
                            class_char VARCHAR(1) NOT NULL)''')
        self.connect.commit()
        """

    def _createView(self):
        self.cursor.execute('''CREATE VIEW IF NOT EXISTS studentsAllowedToSpam AS
                               SELECT user_id, class_number, class_char FROM students WHERE messages_spam = 1''')
        self.connect.commit()

    def _create_Requests_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS requests(
    		id INTEGER PRIMARY KEY AUTOINCREMENT,
    		full_name STRING, 
    		user_id_FK INT NOT NULL,
    		FOREIGN KEY (user_id_FK) REFERENCES students(user_id))""")
        self.connect.commit()

    def createOrUpdate_Student(self, user_id, class_number, class_char):
        """ Метод, добавляющий/изменяющий студента."""
        try:
            self.cursor.execute("INSERT INTO students(user_id, class_number, class_char) VALUES (?, ?, ?)",
                                (user_id, class_number, class_char))
        except self.connect.DatabaseError:
            self.cursor.execute("UPDATE students SET class_number={0}, class_char ={1} WHERE user_id = {2})".format(
                class_number, class_char, user_id))
        self.connect.commit()

    def all(self):
        """ Чисто тест. """
        self.cursor.execute('SELECT * FROM students')
        ans = self.cursor.fetchone()
        return ans

    def class_num(self, user_id):
        """ Метод, позволяющий сформировать номер + литера класса ученика. Пр: 9Б"""
        self.cursor.execute('SELECT class_number, class_char FROM students WHERE user_id={0}'.format(user_id))
        ans = self.cursor.fetchone()
        if ans:
            ans = str(ans[0]) + str(ans[1])
            return ans
        else:
            return None

    def spam(self, user_id):
        """ Метод, отвечающий за рассылку сообщений. """
        # print(user_id.isdigit())
        self.cursor.execute('SELECT messages_spam FROM students WHERE user_id = {0}'.format(user_id))
        i = self.cursor.fetchone()[0]
        if i:
            self.cursor.execute('UPDATE students SET messages_spam = 0 WHERE user_id = {0}'.format(user_id))
            self.connect.commit()
            return False
        else:
            self.cursor.execute('UPDATE students SET messages_spam = 1 WHERE user_id = {0}'.format(user_id))
            self.connect.commit()
            return True
    '''
        def getLeaderResponseList(self):
            self.cursor.execute('SELECT id, teacher_name, class_number, class_char FROM requests')
            ans = self.cursor.fetchall()
            return ans
    '''
    def teacher_confirm_or_deny(self, req_id):
        self.cursor.execute('SELECT user_id, class_number, class_char FROM requests WHERE id = {0}'.format(req_id))
        ans = self.cursor.fetchall()
        self.cursor.execute('DELETE FROM requests WHERE id = {0}'.format(req_id))
        self.connect.commit()
        return ans

    def new_teacher(self, user_id):
        cor_dic = user_id[-1]
        self.connect.execute('INSERT INTO students(user_id, class_number, class_char, status) VALUES (?, ?, ?, ?)',
                             (cor_dic[0], cor_dic[1], cor_dic[2], 'teacher'))
        self.connect.commit()

    def all_by_user(self, user_id):
        self.cursor.execute(
            "SELECT class_number, class_char, messages_spam, status FROM students WHERE user_id = {0}".format(
                user_id))
        info = self.cursor.fetchall()
        if info:
            info = info[-1]
            full_class = str(info[0]) + info[1]
            diction = {
                'class': full_class,
                'spam': info[-2],
                'status': info[-1],
            }
            return diction
        else:
            return False

    def isAccountRegistered(self, user_id):
        self.cursor.execute("SELECT * FROM students WHERE user_id = {0}".format(user_id))
        isExist = self.cursor.fetchone()
        if isExist:
            return True
        return False

    def isTeacher(self, user_id):
        self.cursor.execute("SELECT user_id FROM students WHERE user_id={0} AND status = 'teacher'".format(user_id))
        answer = self.cursor.fetchone()
        if answer:
            return True
        return False

    def getClassToSpam(self, class_number, class_char=''):
        if class_char:
            self.cursor.execute(
                "SELECT user_id FROM studentsAllowedToSpam WHERE class_char='{0}' and class_number={1}".format(
                    class_char, class_number))
        else:
            self.cursor.execute("SELECT user_id FROM studentsAllowedToSpam WHERE class_number={0}".format(class_number))
        IDs = self.cursor.fetchall()
        return IDs

    def getLeadersResponseList(self):
        self.cursor.execute("SELECT id, full_name FROM requests")
        responseList = self.cursor.fetchall()
        return responseList

    def getLeaderResponseWithDelete(self, id):
        try:
            self.cursor.execute("SELECT user_id_FK FROM requests WHERE id={0}".format(id))
        except:
            return None
        else:
            user_id = self.cursor.fetchone()

            self.cursor.execute("DELETE FROM requests WHERE id={0}".format(id))
            self.connect.commit()

            return user_id

    def confirmLeader(self, id):
        user_id = self.getLeaderResponseWithDelete(id)
        if user_id:
            try:
                self.cursor.execute("UPDATE students SET status=1 WHERE user_id={0}".format(user_id[0]))
            except Exception as e:
                return False
            else:
                self.connect.commit()
                return user_id[0]
        else:
            return False

    def createLeaderResponse(self, user_id, full_name):
        self.cursor.execute("INSERT INTO requests(user_id_FK, full_name) VALUES (?, ?)", (user_id, full_name))
        self.connect.commit()
