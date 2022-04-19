# utf-8

import os
import sqlite3
from FDataBase import FDataBase
from PIL import Image, ImageDraw, ImageColor, ImageFont


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


def past_in_templates(data_sert):
    dict_label_user = {}
    file = 'template_sert.png'
    path_file = os.path.normpath(os.getcwd() + '/' + 'static/templates_sert/' + file)
    image_user = Image.open(path_file)
    draw = ImageDraw.Draw(image_user)
    dict_label_user = create_dict_label_user()

    for label in dict_label_user.keys():
        print(label)
        if label in data_sert.keys():
            text = str(data_sert[label])
            coordinat = dict_label_user[label]['coordinat']
            font = dict_label_user[label]['font']
            fill = dict_label_user[label]['fill']
            print(text)
            print(coordinat, font, fill)
            draw.text(coordinat, text, font=font, fill=fill)
    image_user.show(10)


def create_dict_label_user():
    dict_label_user = {
        'name_organization': {
            'label_name': ' ',
            'coordinat': (45, 38),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'number_order': {
            'label_name': ' ',
            'coordinat': (118, 195),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_user': {
            'label_name': ' ',
            'coordinat': (65, 93),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'firstname': {
            'label_name': ' ',
            'coordinat': (135, 93),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'lastname': {
            'label_name': ' ',
            'coordinat': (185, 93),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_suborganization': {
            'label_name': ' ',
            'coordinat': (185, 113),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'position': {
            'label_name': ' ',
            'coordinat': (75, 133),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'course_hourses': {
            'label_name': ' ',
            'coordinat': (55, 193),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'protocol_N': {
            'label_name': ' ',
            'coordinat': (217, 213),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'date_exzam': {
            'label_name': ' ',
            'coordinat': (247, 213),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_director': {
            'label_name': ' ',
            'coordinat': (55, 253),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'date_signature': {
            'label_name': ' ',
            'coordinat': (35, 283),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            }
    }
    return dict_label_user


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_sert(user_id):
    db = connect_db()
    dbase = FDataBase(db)
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    theme2, course_hourses = dbase.read_for_sert()
    data_org = dbase.read_organization()
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id=user_id)
    print('read_DB!')
    data_sert = {}
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




    # draw.text((130, 5), user_data, font=font, fill=ImageColor.colormap['black'])
    # TODO Создать места для вставки текста из словаря
    # TODO потом перебрать словарь  в цикле? и вставить в места для вставки
    # TODO нужна маркировка мест для вставки
    # TODO сохранить результат в файл, в БД





# with tempfile.TemporaryDirectory() as tmpdirname:
#     print('created temporary directory', tmpdirname)
#     name_tmpdir_prot = f"{tmpdirname}\protocol_n_{data_sert['protocol_N']}_{data['name']}.docx"
#     print('name_tmpdirprot', name_tmpdir_prot)
#     doc.save(name_tmpdir_prot)
#     print('doc.save')
#     # TODO конвертировать в ПДФ?? потом перевести в бинарные данные
#     pdf = 'sertif.pdf'
#     # convert("input.docx")
#     convert(doc, pdf)
#     # convert("my_docx_folder/")
#     print('after convert!')
#     with open(name_tmpdir_prot, 'rb') as file:
#         pdf = file.read()
#         # file.seek(0)


if __name__ == '__main__':
    user_id = '1'
    # open_template()
    data_sert = create_sert(user_id)
    past_in_templates(data_sert)