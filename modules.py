# utf-8
import io
import ast
import os
import sqlite3

from PIL import Image
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
UPLOAD_FOLDER = 'Upload_folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    id_course, theme, edu_materials, edu_grafica, edu_additional, edu_instr = dbase.getCourse()
    data_status = {
        'id_course': id_course,
        'theme': theme,
        'edu_materials': edu_materials,
        'edu_grafica': edu_grafica,
        'edu_additional': edu_additional,
        'edu_instr': edu_instr,
        'status': status_exzam,
        'count_prob': count_prob,
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'user_id': user_id,
        'sum_just': 0,
        }
    if dbase.check_exist(user_id=user_id):
        id, theme_1, sertificate, name_sert, number_sert, date_sert = dbase.read_sertificat(user_id)
        path = r'Upload_folder'
        os.chdir(path)
        sertificate = convert_blob(sertificate, name_sert)
        os.chdir('..')
        data_status['sertificat'] = sertificate
        data_status['name_sert'] = name_sert
    return data_status


def check_status_exzam(user_id):
    if not dbase.checkStatus_exzam(user_id=user_id):
        dbase.insertStatus_exzam(user_id=user_id)
        print('добавлен статус экзамена!')
    else:
        print('уже есть!')
    return


def status_user_sertificat(user_id):
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    data_status = {
        'theme': theme,
        'status': status_exzam,
        'data_exzam': data_exzam,
        'user_id': user_id,
    }
    if dbase.check_exist(user_id=user_id):
        id, theme_1, sertificate, name_sert, number_sert, date_sert = dbase.read_sertificat(user_id)
        data_status['sertificat'] = sertificate
        data_status['name_sert'] = name_sert
    return data_status


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
        if not value:
            profile_data[key] = save_profile[key]
        elif value not in save_profile[key]:
            profile_data[key] = save_profile[key]
    return profile_data


# Создание Сертификата
def create_name_sert(user_id,  id_course):
    theme, name_template_sertificat = dbase.read_templates_sert(id_course)
    name, first_name, last_name, dateborn, name_organization, position, email = dbase.getProfile(user_id)
    name_sert = name_template_sertificat
    name_list = [name, first_name, last_name, name_sert]
    name_sert = '_'.join(name_list)
    # Сохранить следующий номер сертификата в БД
    data_org = dbase.read_organization()
    data_save = {}
    data_save['protocol_N'] = data_org['protocol_N']
    data_save['number_sert'] = data_org['number_sert']
    data_save['id_org'] = data_org['id_org']
    dbase.save_sert_N(data_save)
    return theme, name_sert,


# Извлечение из БД учебных материалов по курсу
def get_course():
    id_course, theme, edu_materials, edu_other, edu_additional, edu_instr = dbase.getCourse()
    return id_course, theme, edu_materials, edu_other, edu_additional, edu_instr


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
def save_sertificat(user_id, theme, blob_sertificate, name_sert, number_sert, date_sert):
    dbase.save_sertificat(user_id, theme, blob_sertificate, name_sert, number_sert, date_sert)
    return


# Конвертация изображения в BLOB для БД
def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


# Ковертация из БД в изображение
def convert_blob(file_sert, file_name):
    with open(file_name, 'wb') as f:
        f.write(file_sert)
        return f


# Запись курса в БД
data_course = {}
def create_course(data):
    data_course = data
    list_input = ['edu_materials', 'edu_other', 'edu_additional', 'template_protocol', 'template_sertificat']
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

# переделка даты в нужный формат
def invert_psw(psw):
    len_psw = len(psw)
    if len_psw == 7:
        day = psw[:1]
        month = psw[1:3]
        year = psw[3:]
        if len(day) == 1:
            day = '0' + day
        form_psw = year + '-' + month + '-' + day
        return form_psw
    elif len_psw == 8:
        day = psw[:2]
        month = psw[2:4]
        year = psw[4:]
        form_psw = year + '-' + month + '-' + day
        return form_psw
    elif len_psw == 9:
        split_index = psw[1]
        psw_split = psw.split(split_index)
        day, month, year = psw_split[0], psw_split[1], psw_split[2]
        if len(day) == 1:
            day = '0' + day
        form_psw = year + '-' + month + '-' + day
        return form_psw
    elif len_psw == 10:
        split_index = psw[2]
        psw_split = psw.split(split_index)
        day, month, year = psw_split[0],  psw_split[1], psw_split[2]
        form_psw = year + '-' + month + '-' + day
        return form_psw
    else:
        return psw


def read_add(file):
    data_add = {}
    with open(file, "r", encoding='utf-8') as file1:
        while True:
            line = file1.readline()
            if not line:
                break
            name_str, link_str = line.split(sep='--', maxsplit=1)
            data_add[name_str] = link_str
    return data_add

def read_organization():
    data_sert = dbase.read_organization()
    return data_sert


#  создание протокола по времени и о наличию  сдавших экзамен.
#  как настраивается событие на сервере по времени??
#  обращение к БД - проверка, есть ли СДАВШИЕ екзамен за ТЕКУЩИЕ сутки -  день или текущую неделю
#  если человек сдал, то из БД берется текущий номер протокола для вставки в удостоверение
#  в 00.01 все сдавшие за прошедшие сутки формируются в список для записи в протокол.
#  создается протокол и записывается в БД, номер протокола в профиле организации изменяется.

