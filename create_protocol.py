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
    name_template_protocol = dbase.read_templates_protocol(id_course)
    data_org = dbase.read_organization()
    data_users_id = dbase.read_users_exzam(current_date)
    print('data_users_id', data_users_id)
    if not data_users_id:
        exit()
    # print('id', data_users_id)
    id_course, theme2, course_hourses, template_sertificat, template_protocol, name_template_sertificat, \
    name_template_protocol = dbase.read_for_sert()

    data_for_prot = []
    for user_id in data_users_id:
        data_sert_exzam = dbase.read_sertificat(user_id)
        id, theme, count_prob, status_exzam, data_exzam = dbase.checkStatus_exzam(user_id)
        status_exzam = status_exzam
        number_sert = data_sert_exzam['number_sert']
        data_id = dbase.getProfile(user_id)
        full_name = [data_id['name'], data_id['firstname'], data_id['lastname']]
        name_user = ' '.join(full_name)
        user_id_data = [user_id, name_user, data_id['position'], data_org['name_suborganization'], status_exzam,
                        number_sert, data_org['reason_for_checking']]
        data_for_prot.append(user_id_data)

    protocol_N = data_org['protocol_N']
    date_protocol = [str(protocol_N), str(current_date), name_template_protocol]
    name_protocol = ('_').join(date_protocol)

    data_save = {}
    data_save['protocol_N'] = data_org['protocol_N']
    data_save['id_org'] = data_org['id_org']
    dbase.save_protocol_N(data_save)
    print('data_for_prot', data_for_prot)
    return name_protocol, data_for_prot, data_org


def convert_protocol(data):
    doc = DocxTemplate('static/templates_sert/template_protocol.docx')
    data_sert = data
    context = {
               'protocol_N': data_sert['protocol_N'],
               'name_organization': data_sert['name_organization'],
               'name_suborganization': data_sert['name_suborganization'],
               'date_exzam': '01/01/2021',
               'date_order': data_sert['data_order'],
               'number_order': data_sert['number_order'],
               'name_chairman': data_sert['name_chairman'],
               'position_chairman': data_sert['position_chairman'],
               'name_member_1': data_sert['name_member_1'],
               'position_member_1': data_sert['position_member_1'],
               'name_member_2': data_sert['name_member_2'],
               'position_member_2': data_sert['position_member_2'],
               'name_course': 'Охрана труда',
               'course_hourses': '20',
               }
    doc.render(context)
    doc.save('static/templates_sert/template_protocol_2.docx')
    return


def read_template(data_for_prot, name_protocol):
    path = 'static/templates_sert/template_protocol_2.docx'
    doc = Document(path)
    # pars = doc.paragraphs
    tables = doc.tables
    # for num, par in enumerate(pars):
    #     print(num, par.text)
    for table in tables:
        for i, row in enumerate(table.rows):
            row_list = []
            for cell in row.cells:
                row_list.append(cell.text)
    for row in data_for_prot:
        cells = table.add_row().cells
        print(row)
        for i, val in enumerate(row):
            print(i, val)
            cells[i].text = str(val)
    doc.save(name_protocol)


def run(id_course):
    name_protocol, data_for_prot, data_org = create_prot(id_course)
    # TODO добавить в data_org - дату экзамена, 'name_course': data_sert['theme'], 'course_hourses': data_sert['course_hourses'],
    convert_protocol(data_org)
    read_template(data_for_prot, name_protocol)
    print('ВСЁ!')


if __name__ == '__main__':
    schedule.every().day.at("19:00").do(run(1))


