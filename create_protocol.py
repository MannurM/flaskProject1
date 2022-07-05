import sqlite3
import schedule


from docx import Document
from docxtpl import DocxTemplate
from datetime import date, datetime
from FDataBase import FDataBase


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_prot(id_course):
    db = connect_db()
    dbase = FDataBase(db)
    current_date = date.today()
    # Проверка на количество сдавших экзамен - есди имеются,то протокл создается
    data_users_id = dbase.read_users_exzam(current_date)
    if not data_users_id:
        exit()
    # сбор данных для создания шаблона протокола
    data_org = dbase.read_organization()
    name_courses, course_hourses = dbase.read_name_course(id_course)
    context = {
        'protocol_N': data_org['protocol_N'],
        'name_organization': data_org['name_organization'],
        'name_suborganization': data_org['name_suborganization'],
        'date_exzam': current_date,
        'date_order': data_org['data_order'],
        'number_order': data_org['number_order'],
        'name_chairman': data_org['name_chairman'],
        'position_chairman': data_org['position_chairman'],
        'name_member_1': data_org['name_member_1'],
        'position_member_1':data_org['position_member_1'],
        'name_member_2': data_org['name_member_2'],
        'position_member_2': data_org['position_member_2'],
        'name_course': name_courses,
        'course_hourses': course_hourses
    }
    # кортеж списков с данными сдавших успешнео экзамен для протокола
    data_for_prot = []
    for user_id in data_users_id:
        data_sert_exzam = dbase.read_sertificat(user_id)
        id, theme, count_prob, status_exzam, data_exzam = dbase.checkStatus_exzam(user_id)
        status_exzam = status_exzam
        number_sert = data_sert_exzam['number_sert']
        data_id = dbase.getProfile(user_id)
        full_name = [data_id['name'], data_id['firstname'], data_id['lastname']]
        name_user = ' '.join(full_name)
        user_id_data = (user_id, name_user, data_id['position'], data_org['name_suborganization'], status_exzam,
                        number_sert, data_org['reason_for_checking'], ' ',)
        data_for_prot.append(user_id_data)
    # создание имени протокола
    protocol_N = data_org['protocol_N']
    value_protocol = [str(protocol_N), str(current_date)]
    date_protocol = ('_').join(value_protocol)
    data_save = {}
    # Изменение номера протокола в БД
    data_save['protocol_N'] = data_org['protocol_N']
    data_save['id_org'] = data_org['id_org']
    dbase.save_protocol_N(data_save)
    return date_protocol, data_for_prot, context


def convert_protocol(context):
    doc = DocxTemplate('static/templates_sert/template_protocol.docx')
    doc.render(context)
    doc.save('static/templates_sert/template_protocol_2.docx')
    return


def read_template(data_for_prot, date_protocol):
    path = 'static/templates_sert/template_protocol_2.docx'
    doc = Document(path)
    tables = doc.tables
    cells, count = 0, 0
    for table in tables:
        for i, row in enumerate(table.rows):
            row_list = []
            for cell in row.cells:
                row_list.append(cell.text)
            # добавление строки к таблице
            for row in data_for_prot:
                cells = table.add_row().cells
    count += 1
    # добавление данных в новую строку
    for i, val in enumerate(row):
        if i == 0:
            cells[i].text = str(count)
        else:
            cells[i].text = str(val)
    # сохранение протокола в папку 'upload_folder'
    upload_folder = 'upload_folder'
    protocol =[date_protocol, 'protocol.docx']
    name_protocol = '_'.join(protocol)
    paste_path = [upload_folder, name_protocol]
    path_protocol = '/'.join(paste_path)
    doc.save(path_protocol)
    return


def run(id_course):
    date_protocol, data_for_prot, context = create_prot(id_course)
    convert_protocol(context)
    read_template(data_for_prot, date_protocol)


if __name__ == '__main__':
    # schedule.every().day.at("08:48").do(run(1))
    run(1)


