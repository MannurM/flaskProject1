import datetime
import sqlite3
import random
from datetime import date


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        self.name_test = None
        self.qestion = None
        self.answer = ''
        self.answer_just = None
        self.path = None
        self.label = None
        self.rez_dict = {}
        self.n_qestion = 5
        self.list_answer_just = []

    def getCourse(self):
        try:
            self.__cur.execute(f"SELECT id_course, theme, edu_materials, edu_grafica, edu_additional, edu_instr FROM courses")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД " + str(e))
        return False

    def read_for_sert(self):
        val = 'id_course, theme, course_hourses, template_sertificat, template_protocol, ' \
              'name_template_sertificat, name_template_protocol'
        try:
            self.__cur.execute(f"SELECT {val} FROM courses")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД " + str(e))
        return False

    def getStatus_name(self, user_id):
        try:
            user_id = user_id
            self.__cur.execute(f"SELECT name, firstname, lastname FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
            else:
                print('res_false', res)
        except sqlite3.Error as e:
            print("Ошибка получения статуса имени " + str(e))
        return False


    def getStatus_exzam(self, user_id):
        try:
            user_id = user_id
            self.__cur.execute(f"SELECT theme, count_prob, status_exzam, data_exzam FROM exzam_rezult WHERE id={user_id}")
            res = self.__cur.fetchone()
            if res:
                return res
            else:
                theme = 'нет'
                count_prob = 0
                status_exzam = 'Не сдано'
                date_exzam = 0
                return theme, count_prob, status_exzam, date_exzam
        except sqlite3.Error as e:
            print("Ошибка получения статуса экзамена " + str(e))
        return False

    def checkStatus_exzam(self, user_id):
        try:
            self.__cur.execute(f"SELECT id, theme, count_prob, status_exzam, data_exzam FROM exzam_rezult WHERE id='{user_id}'")
            res = self.__cur.fetchone()
            if not res:
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения статуса экзамена " + str(e))
        return

    def insertStatus_exzam(self, user_id):
        try:
            user_id = user_id
            theme = 'theme'
            count_prob = 0
            status_exzam = 'Не сдано'
            date_exzam = date.today()
            values = (user_id, theme, count_prob, status_exzam, date_exzam)
            self.__cur.execute("INSERT OR IGNORE INTO exzam_rezult VALUES(?, ?, ?, ?, ?)", values)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи начального статуса экзамена " + str(e))
        return

    def getProfile(self, user_id):
        try:
            select_data = ('name', 'firstname', 'lastname', 'dateborn', 'name_organization', 'position', 'email')
            self.__cur.execute(f"SELECT name, firstname, lastname, dateborn, name_suborganization, position, email FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения данных профиля" + str(e))
        return False

    def getCourseEdu(self, id_course):
        try:
            self.__cur.execute(f"SELECT edu_materials, edu_grafica, edu_additional, edu_instr FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(getCourseEdu) " + str(e))
        return

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUser) " + str(e))
        return False

    def read_organization(self):
        try:
            self.__cur.execute("SELECT * FROM organization_com")
            res = self.__cur.fetchone()
            if not res:
                print("Организация не найдена!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(organization) " + str(e))
        return

    def save_sert_N(self, data):
        try:
            protocol_N = data['protocol_N']
            number_sert = data['number_sert'] + 1
            id_org = data['id_org']  # - номер организации в БД
            up_date = (number_sert, id_org)
            self.__cur.execute("UPDATE or IGNORE organization_com SET number_sert=? WHERE id_org=?",
                               up_date)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(sert_N) " + str(e))
        return

    def save_protocol_N(self, data):
        try:
            protocol_N = data['protocol_N'] + 1
            id_org = data['id_org']  # - номер организации в БД
            up_date = (protocol_N, id_org)
            self.__cur.execute("UPDATE or IGNORE organization_com SET protocol_N=? WHERE id_org=?",
                               up_date)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(protocol_N) " + str(e))
        return


    def save_sertificat(self, user_id, theme, sertificate, name_sert, number_sert, date_sert):
        try:
            values = (user_id, theme, sertificate, name_sert, number_sert, date_sert)
            self.__cur.execute("INSERT OR IGNORE INTO docs VALUES(?,?,?,?,?,?)", values)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(save_sertificat) " + str(e))
        return

    # def read_sertificat(self, user_id):
    #     try:
    #         self.__cur.execute(f"SELECT * FROM docs where id = {user_id}")
    #         res = self.__cur.fetchone()
    #         if not res:
    #             return False
    #         return res
    #     except sqlite3.Error as e:
    #         print("Ошибка записи данных в БД(save_sertificat) " + str(e))
    #     return
    #
    def check_exist(self, user_id):
        self.__cur.execute(f"SELECT * FROM docs where id = {user_id}")
        res = self.__cur.fetchone()
        return res


    def read_sertificat(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM docs WHERE id = {user_id}")
            res = self.__cur.fetchone()
            if not res:
                print("Ошибка нет данных в БД")
                return None, None, None, None, None, None
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_sertificat) " + str(e))
        return

    def read_users_exzam(self, current_day):
        try:
            self.__cur.execute(f"SELECT id FROM exzam_rezult WHERE data_exzam = '{current_day}'")
            res = self.__cur.fetchone()
            if not res:
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения статуса экзамена(read_users_exzam) " + str(e))
        return


    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUserByEmail) " + str(e))
        return False

    def getUserByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUserByName) " + str(e))
        return False

    def read_list_just(self, user_id):
        try:
            self.__cur.execute(f"SELECT laj, llu FROM a_just WHERE id = {user_id} ")
            res = self.__cur.fetchall()
            if not res:
                print("Нет списка правильных ответов!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_list_just) " + str(e))

    def save_status_user(self, user_id, data):  # обновление статуса экзамена в БД
        theme = data['theme']
        status_course = data['status']
        count_prob = data['count_prob']
        date_exzam = date.today()
        up_date = (theme, status_course, count_prob, date_exzam)
        try:
            self.__cur.execute(f"UPDATE exzam_rezult SET theme=?, status_exzam=?, count_prob=?, data_exzam=? WHERE id = {user_id}", up_date)
            self.__db.commit()
            return
        except  sqlite3.Error as e:
            print("Ошибка обновления данных в БД(save_status_user) " + str(e))

    def read_count_prob(self, user_id):
        try:
            print('read_count_prob')
            self.__cur.execute(f"SELECT count_prob FROM exzam_rezult WHERE id = {user_id}")
            res = self.__cur.fetchone()
            if not res:
                print("Ошибка нет данных в БД")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_count_prob) " + str(e))

    def save_count_prob(self, user_id, data):  # обновление результатов экзамена в БД
        count_prob = data['count_prob']
        id = data['user_id']
        up_date = (count_prob, id)
        self.__cur.execute(f"UPDATE exzam_rezult SET count_prob = ? WHERE id = {id}", up_date)
        self.__db.commit()
        return

    def update_profile(self, user_id, profile_data):
        self.profile_data = profile_data
        name = self.profile_data['name']
        firstname = self.profile_data['firstname']
        lastname = self.profile_data['lastname']
        dateborn = self.profile_data['dateborn']
        name_suborganization = self.profile_data['name_suborganization']
        position = self.profile_data['position']
        email = self.profile_data['email']
        user_id = user_id
        up_date = (name, firstname, lastname, dateborn, name_suborganization, position, email, user_id)
        try:
            sqlite_update = ('Update users set name=?, firstname=?, lastname=?, dateborn=?, name_suborganization=?,\n'
                             '            position=?, email=? where id = ?')
            self.__cur.execute(sqlite_update, up_date)
            self.__db.commit()
            return
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(update_profile) " + str(e))

    def read_test(self, path):
        list_label_use = []
        list_label = []
        try:
            self.__cur.execute(f'SELECT label from tests')
            result = self.__cur.fetchall()
            for res in result:
                label_res = dict(res)['label']
                list_label.append(label_res)

            # Создание случайного набора вопросов c ответами
            for i in range(self.n_qestion):
                self.rnd_label = random.choice(list_label)
                self.__cur.execute(f"SELECT qestion, answer FROM tests WHERE label = {self.rnd_label}")
                res = self.__cur.fetchone()
                q_res = dict(res)['qestion']
                a_res = dict(res)['answer']
                self.rez_dict[self.rnd_label] = {q_res: a_res}
                list_label_use.append(self.rnd_label)

                # Список правильных ответов
                self.__cur.execute(f"SELECT a_just FROM tests WHERE label = {self.rnd_label}")
                res = self.__cur.fetchone()
                j_res = dict(res)['a_just']
                self.list_answer_just.append(j_res)
                list_label.remove(self.rnd_label)

        except sqlite3.Error as e:
            print("Ошибка получения вопросов из БД(read_test) " + str(e))
        return self.rez_dict, self.list_answer_just, list_label_use

    def save_(self, user_id, list_answer_just, list_label_use):
        try:
            laj = str(list_answer_just)
            llu = str(list_label_use)
            self.__cur.execute(f"INSERT INTO a_just (id, laj, llu) VALUES(?, ?, ?)", (user_id, laj, llu))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(save_list_just) " + str(e))
        return

    def theme_for_sert(self, user_id):
        try:
            self.__cur.execute(f"select theme from exzam_rezult WHERE id = {user_id}")
            res = self.__cur.fetchone()
            if not res:
                print("Ошибка нет темы в результатах в БД")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения данных из БД(theme_for_sert) " + str(e))
        return

    def create_template_prot(self, data):
        sert = data['template_protocol']
        name_file = data['name_template_protocol']
        theme_in = data['theme']
        val = (sert, name_file, theme_in)
        try:
            sqlite_update = 'UPDATE courses SET template_protocol=?, name_template_protocol=? where theme=?'
            self.__cur.execute(sqlite_update, val)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка создания шаблона сертификата в БД (create_template_sert) " + str(e))
        finally:
            return

    def create_template_sert(self, data):
        sert = data['template_sertificat']
        name_file = data['name_template_sertificat']
        theme_in = data['theme']
        val = (sert, name_file, theme_in)
        try:
            sqlite_update = 'UPDATE courses SET template_sertificat=?, name_template_sertificat=? where theme=?'
            self.__cur.execute(sqlite_update, val)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка создания шаблона сертификата в БД (create_template_sert) " + str(e))
        finally:
            return

    def create_course(self, data):
        data['time'] = datetime.date
        values = data['theme'], data['edu_materials'], data['edu_grafica'], data['edu_additional'],\
                 data['edu_instr'], data['time'], data['template_protocol'], data['template_sertificat'],\
                 data['course_hourses'], data['name_edu_materials'], data['name_edu_other'],\
                 data['name_edu_additional'], data['name_template_protocol'], data['name_template_sertificat']
        try:
            self.__cur.execute('INSERT OR IGNORE INTO courses VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
            self.__db.commit()
            return
        except sqlite3.Error as e:
            print("Ошибка создания шаблона сертификата в БД (create_template_sert) " + str(e))

    def read_templates(self, id_course):
        value = 'theme, template_protocol, template_sertificat, name_template_protocol, name_template_sertificat'
        try:
            self.__cur.execute(f"SELECT {value}  FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(read_templates) " + str(e))
        return

    def read_templates_sert(self, id_course):
        value = 'theme, name_template_sertificat'
        try:
            self.__cur.execute(f"SELECT {value}  FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(read_templates) " + str(e))
        return

    def read_templates_protocol(self, id_course):
        value = 'name_template_protocol'
        try:
            self.__cur.execute(f"SELECT {value}  FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(read_templates_protocol) " + str(e))
        return

    def read_name_course(self, id_course):

        try:
            self.__cur.execute(f"SELECT theme, course_hourses FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(read_name_course) " + str(e))
        return

    def create_user(self, id, name, firstname, lastname, dateborn, position, name_suborganization, email,  hpsw, time,
                    role):
        values = id, name, firstname, lastname, dateborn, name_suborganization, position, email,  hpsw, time, role
        try:
            self.__cur.execute('INSERT OR REPLACE INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?)', values)
            self.__db.commit()
            return
        except sqlite3.Error as e:
            print("Ошибка создания пользователя в БД (create_user) " + str(e))

    def create_test(self, qestion_txt, list_answers, answer_just):
        self.label = random.randint(0, 10000)
        self.label = self.check_label(self.label)  # проверка метки в БД на совпадение и выбор новой
        values = self.label, qestion_txt, str(list_answers), answer_just
        try:
            # self.__cur.execute('CREATE TABLE IF NOT EXISTS tests')
            self.__cur.execute('INSERT or REPLACE INTO tests VALUES(?,?,?,?)', values)
            self.__db.commit()
            return
        except sqlite3.Error as e:
            print("Ошибка создания теста в БД (create_test) " + str(e))

    def check_label(self, label):
        self.label = label
        label_set = self.all_label()
        if not label_set:
            return self.label
        else:
            list_label = []
            for res in label_set:
                label_res = dict(res)['label']
                list_label.append(label_res)
            label_set = set(list_label)
            while self.label not in label_set:
                if len(label_set) >= 10000:
                    break
                break
            else:
                self.label = random.randint(0, 10000)
            return self.label

    def all_label(self):
        try:
            self.__cur.execute(f"SELECT label FROM tests ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения списка label из test " + str(e))
        return

    def all_qestion(self):
        try:
            self.__cur.execute(f"SELECT qestion FROM tests")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения списка qestion из test " + str(e))
        return

    def all_users(self):
        try:
            self.__cur.execute(f"SELECT name, firstname, lastname FROM users")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения списка name из users " + str(e))
        return

    def number_id_user(self):
        try:
            self.__cur.execute(f"SELECT id FROM users")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения списка id из users " + str(e))
        return

    def save_insubd(self, file):
        pass
