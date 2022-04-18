# utf-8
import io
import ast
import tempfile
import os
import sqlite3


from flask import Flask, g
from flask_login import LoginManager
from UserLogin_2 import UserLogin
from FDataBase import FDataBase


temp_dict = {}


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'pr_ot.db')))


login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Модуль для проверки результатов тестов
def check_edu_test(list_answer_just, data_answer):
    sum_just = 0
    for answer in data_answer:
        if answer in list_answer_just:
            sum_just += 1
    return sum_just


# Считывание статистики по ID
def status_user(user_id):
    name, firstname, lastname = dbase.getStatus_name(user_id=user_id)
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    id_course, theme, edu_materials, edu_other, edu_additional = dbase.getCourse()
    data = {
        'id_course': id_course,
        'theme': theme,
        'edu_materials': edu_materials,
        'edu_other': edu_other,
        'edu_additional': edu_additional,
        'status': status_exzam,
        'count_prob': count_prob,
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'user_id': user_id,
        'sum_just': 0,
        }
    if dbase.check_exist(user_id=user_id):
        id, theme_1, protocol, sertificate, name_protocol, name_sert = dbase.read_sertificat(user_id)
        data['sert'] = 1 # todo ПОЧЕМУ ОДИН?

        # TODO data['protocol'], data['sertificate'] - это ссылки на файлы в БД
        # TODO проверка  рендерится - если скачать сертификат, то запускается скрипт
        # ToDO скрипт - Передается user_id, theme_1. Формируется запрос в БД. ОТвет конвертируется в docx.
        # TODO Ответ формируется во временной памяти. Открывается новая страница браузера с параметром download.
        # TODO Предлагается путь для сохранения.

        blob_data = protocol
        filename = name_protocol
        protocol = convert_from_binary_data(filename, blob_data)
        data['protocol'] = protocol

        blob_data = sertificate
        filename = name_sert
        sertificate = convert_from_binary_data(filename, blob_data)
        data['sertificate'] = sertificate
    return data


# Распаковка теста из БД
def unpacking_edutest(user_id):
    list_answer_just = []
    temp_dict = {}
    qa_dict, dict_just, list_label_use = dbase.read_test('pr_ot.db')
    for label, val in qa_dict.items():
        for qestion, answer in val.items():
            answer = ast.literal_eval(answer)  # Избавляет от кавычек список
            answer_not_resp = []
            for ans in answer:
                answer_not_resp.append(ans)  # список всех ответов
            temp_dict[qestion] = answer_not_resp  # словарь из ключа - вопроса, значений - вариантов ответов
    for value in dict_just:
        answer_just = value
        list_answer_just.append(answer_just)
    return temp_dict, list_answer_just, list_label_use


# Сравнение ответов в тесте
# TODO Разделить ответы на экзаменационные и пробные??
def read_list_just(user_id, data_answer):
    list_label_just = dbase.read_list_just(user_id)
    if not list_label_just:
        print('не прочитались данные')
    list_answer_just = []
    list_label_use = []
    for i in list_label_just:
        laj = tuple(i)
        list_answer_just = laj[0]
        list_label_use = laj[1]
    sum_just = check_edu_test(list_answer_just, data_answer)  # модуль проверки формы
    return sum_just, list_answer_just, data_answer, list_label_use


# Проверка на изменения в профиле
def check_save_profile(user_id, save_profile, profile_data):
    for key, value in profile_data.items():
        if value == '':
            profile_data[key] = save_profile[key]
        elif value not in save_profile[key]:
            profile_data[key] = save_profile[key]
    print('after check', profile_data)
    return profile_data


# Распаковка файла протокола или сертификата из БД
def convert_from_binary_data(filename, blob_data):
    # TODO 1. передать в функцию имя файла и бинарный файл,
    # TODO 2. сразу бинарный файл и  название файла в БД (название файла удостоверения иил протокола сохранить в БД)
    # TODO 3. открыть файл с навазнием из БД, закачать бинарные данные данные , закрыть файл, вернуть файл из конвертера
    name_file = filename
    b_file = io.BytesIO(blob_data)
    # TODO при открытии файла -  файл сохраняется в корневом каталоге в нужном docx формате. как оставить его в памяти
    # TODO и перенести в к пользователю
    with open(name_file, 'wb') as file:
        name_file = file.write(blob_data)
    b_file.close()


    return name_file


# Конвертирование файла для записи в БД
def convert_path(prot, sert):
    with tempfile.TemporaryDirectory() as tmpdirname:
        prot = f'{tmpdirname}\_{prot}'
        with open(prot, 'rb') as doc:
            blob_data_prot = doc.read()
        sert = f'{tmpdirname}\_{sert}'
        with open(sert, 'rb') as doc:
            blob_data_sert = doc.read()
        return blob_data_prot, blob_data_sert


# Создание Сертификата и протокола
def create_sert(user_id):
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    theme2, course_hourses = dbase.read_for_sert()
    data_org = dbase.read_organization()
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id=user_id)
    print('read_DB!')
    data_sert={}
    for key in data_org.keys():
        data_sert[key] = data_org[key]
    data_sert['name'] = name
    data_sert['firstname'] = firstname
    data_sert['lastname'] = lastname
    data_sert['dateborn'] = dateborn
    data_sert['name_suborganization'] = name_suborganization
    data_sert['position'] = position
    data_sert['data_exzam'] = data_exzam
    data_sert['status_exzam'] = status_exzam
    data_sert['theme'] = theme
    data_sert['course_hourses'] = course_hourses
    return data_sert
    # name_sert, sert_doc = convert_sert(data_sert) # TODO заменить модуль создания  сертификата
    # name_protocol, prot_doc = convert_protocol(data_sert)
    # print("convert sert_prot!")
    # # Сохранить следующий номер протокола и сертификата в БД
    # data_save = {}
    # data_save['protocol_N'] = data_org['protocol_N']
    # data_save['number_sert'] = data_org['number_sert']
    # data_save['id_org'] = data_org['id_org']
    # dbase.save_protocol_N(data_save)
    #
    # blob_sertificate = sert_doc
    # blob_protocol = prot_doc
    # print('theme2, blob_sertificate, blob_protocol, name_protocol, name_sert',
    #       theme2, blob_sertificate, blob_protocol, name_protocol, name_sert)
    # return theme2, blob_sertificate, blob_protocol, name_protocol, name_sert


# Извлечение из БД учебных материалов по курсу
def get_course():
    id_course, theme, edu_materials, edu_other, edu_additional = dbase.getCourse()
    return id_course, theme, edu_materials, edu_other, edu_additional


# Запись в БД правильных ответов и использованных вопросов
def save_(user_id, list_answer_just, list_label_use):
    dbase.save_(user_id, list_answer_just, list_label_use)
    return


# Извлечение из БД имени пользователя(если оно есть)
def get_user_byname(name_user):
    name = dbase.getUserByName(name_user)
    return name


# Обновление профиля пользователя в БД
def update_profile(user_id, new_profile_data):
    dbase.update_profile(user_id, new_profile_data)
    return

# Записать статус экзамена
def save_status_user(user_id, data):
    dbase.save_status_user(user_id=user_id, data=data)
    return


# Вызов из БД личных данных пользователя
def getprofile(user_id):
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id=user_id)
    profile_data = {
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'dateborn': dateborn,
        'name_suborganization': name_suborganization,
        'position': position,
        'email': email
        }
    return profile_data


# Запись в БД созданного сертификата
def save_sertificat(user_id, theme, blob_sertificate, blob_protocol, name_protocol, name_sert):
    dbase.save_sertificat(user_id, theme, blob_sertificate, blob_protocol, name_protocol, name_sert)
    return


# Запись курса в БД
data_course = {}
def create_course(data):
    data_course = data
    list_input = ['edu_materials', 'edu_other', 'edu_additional', 'template_protocol','template_sertificat']
    for key in list_input:
        file = data_course[key]
        name = os.path.basename(file)
        filename, file_extension = os.path.splitext(file)
        key_name = 'name' + '_' + key
        data_course[key_name] = name


        with open(file, 'rb') as f:
            blob_data = f.read()
            data_course[key] = blob_data
    dbase.create_course(data_course)
    return


# чтение из БД,  конвертация в первоначальный формат
def read_course(id_course):
    prot, sert, name_prot, name_sert = dbase.read_templates(id_course=id_course)
    with open(name_prot,'wb') as f:
        protocol = f.write(prot)
    with open(name_sert,'wb') as f:
        sertificat = f.write(sert)
    return protocol, sertificat

