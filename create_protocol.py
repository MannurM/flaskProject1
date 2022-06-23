
import schedule
import time
import sqlite3
from datetime import date
from FDataBase import FDataBase


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_protocol(id_course):
    db = connect_db()
    dbase = FDataBase(db)
    # Скачать шаблон протокола
    theme, name_template_protocol = dbase.read_templates_protocol(id_course)
    # name, first_name, last_name, dateborn, name_organization, position, email = dbase.getProfile()
    data_org = dbase.read_organization()

    # TODO Сделать функцию запроса всех данных из БД за прошедший день и сдавших экзамен по теме
    # name_protocol = name_template_protocol
    name_protocol =  + protocol_N + '_' + name_protocol


    # Сохранить следующий номер протокола и сертификата в БД

    data_save = {}
    data_save['protocol_N'] = data_org['protocol_N']
    data_save['id_org'] = data_org['id_org']
    dbase.save_protocol_N(data_save)
    # TODO Записать протокол в папку upload_folder/protocol
    return theme, name_protocol

def read_users_exzam(id_course):
    db = connect_db()
    dbase = FDataBase(db)
    data_protocol = dbase.data_protocol(id_course)
    current_date = date.today()
    if data_protocol == current_date:
        dbase.read_users_exzam(id_course)
    else:
        data_protocol = current_date
    return



def run(id_course):
    schedule.every().day.at("00:15").do(create_protocol(id_course))


if __name__ == '__main__':
    run(1)

# data_sert = create_user_sert.create_sert(user_id)
# sertificat_file = create_user_sert.past_in_templates_sertificat(data_sert)
# protocol_file = create_user_sert.past_in_templates_protocol(data_sert)

# protocol_file = modules.image_to_byte_array(protocol_file)