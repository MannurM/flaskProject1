
import schedule
import sqlite3
from datetime import date

import create_user_sert
from create_user_sert import create_protocol, past_in_templates_protocol
import modules
from FDataBase import FDataBase


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_prot(id_course):
    db = connect_db()
    dbase = FDataBase(db)
    current_date = date.today()
    # Скачать имя шаблона протокола
    theme, name_template_protocol = dbase.read_templates_protocol(id_course)

    # Извлечь номер по организации из БД
    data_org = dbase.read_organization()
    protocol_N = data_org['protocol_N']

    # Собрать имя протокола
    date_protocol = [protocol_N, current_date, name_template_protocol]
    name_protocol = ('_').join(date_protocol)

    # Сделать функцию запроса всех данных из БД за прошедший день и сдавших экзамен по теме
    status_exzam = 'Сдано'
    data_users_id = dbase.read_users_exzam(theme, current_date, status_exzam) # id сдавших


    date_protocol = [str(protocol_N), str(current_date), name_template_protocol]
    name_protocol = ('_').join(date_protocol)

    # Извлечь из БД начинку для протокола
    # 'name', 'firstname', 'lastname', 'dateborn', 'name_organization', 'position', 'email'
    #
    for user_id in data_users_id:
        data_id = dbase.getProfile(user_id)
        id_course, theme2, course_hourses, template_sertificat, template_protocol, name_template_sertificat, name_template_protocol \
            = dbase.read_for_sert()

        protocol_file = create_user_sert.past_in_templates_protocol(data_sert)
        protocol_file = modules.image_to_byte_array(protocol_file)


    # Сохранить следующий номер протокола в БД
    data_save = {}
    data_save['protocol_N'] = data_org['protocol_N']
    data_save['id_org'] = data_org['id_org']
    dbase.save_protocol_N(data_save)
    # TODO Записать протокол в папку upload_folder/protocol
    return theme, name_protocol

def read_data_exzam(id_course):
    db = connect_db()
    dbase = FDataBase(db)




def run(id_course):
    schedule.every().day.at("23:45").do(create_protocol(id_course))


if __name__ == '__main__':
    run(1)

# data_sert = create_user_sert.create_sert(user_id)
# sertificat_file = create_user_sert.past_in_templates_sertificat(data_sert)
# protocol_file = create_user_sert.past_in_templates_protocol(data_sert)

# protocol_file = modules.image_to_byte_array(protocol_file)