# utf-8

import os
import sqlite3
from FDataBase import FDataBase
from PIL import Image, ImageDraw, ImageColor, ImageFont


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


def convert_blob(file_sert, file_name):
    with open(file_name, 'wb') as f:
        f.write(file_sert)
        return file_name


def past_in_templates_sertificat(data_sert):
    file_sert = data_sert['template_sertificat']
    file_name = data_sert['name_template_sertificat']
    file_name = convert_blob(file_sert, file_name)
    image_user = Image.open(file_name)
    draw = ImageDraw.Draw(image_user)
    dict_label_user = create_dict_label_user()
    for label in dict_label_user.keys():
        if label in data_sert.keys():
            text = str(data_sert[label])
            coordinat = dict_label_user[label]['coordinat']
            font = dict_label_user[label]['font']
            fill = dict_label_user[label]['fill']
            draw.text(coordinat, text, font=font, fill=fill)
    return image_user


def past_in_templates_protocol(data_sert):
    file_sert = data_sert['template_protocol']
    file_name = data_sert['name_template_protocol']
    file_name = convert_blob(file_sert, file_name)
    image_user = Image.open(file_name)
    draw = ImageDraw.Draw(image_user)
    dict_label_user = create_dict_label_user_prot()
    for label in dict_label_user.keys():
        if label in data_sert.keys():
            text = str(data_sert[label])
            coordinat = dict_label_user[label]['coordinat']
            font = dict_label_user[label]['font']
            fill = dict_label_user[label]['fill']
            draw.text(coordinat, text, font=font, fill=fill)
    return image_user


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_sert(user_id):
    db = connect_db()
    dbase = FDataBase(db)
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    id_course, theme2, course_hourses, template_sertificat, template_protocol, name_template_sertificat, name_template_protocol\
        = dbase.read_for_sert()
    data_org = dbase.read_organization()
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id=user_id)
    # print('read_DB!')
    data_sert = {}
    for key in data_org.keys():
        data_sert[key] = data_org[key]
    data_sert['id_course'] = id_course
    data_sert['name_user'] = name
    data_sert['firstname'] = firstname
    data_sert['lastname'] = lastname
    data_sert['date_signature'] = data_exzam[:11]
    data_sert['name_suborganization'] = name_suborganization
    data_sert['position'] = position
    data_sert['data_exzam'] = data_exzam[:11]
    data_sert['status_exzam'] = status_exzam
    data_sert['theme'] = theme2
    data_sert['course_hourses'] = course_hourses
    data_sert['template_sertificat'] = template_sertificat
    data_sert['template_protocol'] = template_protocol
    data_sert['name_template_sertificat'] = name_template_sertificat
    data_sert['name_template_protocol'] = name_template_protocol
    data_sert['name_chairman_sing'] = data_org['name_chairman']
    data_sert['name_member_1_sing'] = data_org['name_member_1']
    data_sert['name_member_2_sing'] = data_org['name_member_2']
    return data_sert


def create_dict_label_user():
    dict_label_user = {
        'name_organization': {
            'label_name': ' ',
            'coordinat': (45, 38),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'number_sert': {
            'label_name': ' ',
            'coordinat': (265, 75),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_user': {
            'label_name': ' ',
            'coordinat': (55, 93),
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
            'coordinat': (215, 93),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_suborganization': {
            'label_name': ' ',
            'coordinat': (105, 113),
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
        'theme': {
            'label_name': ' ',
            'coordinat': (65, 173),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'course_hourses': {
            'label_name': ' ',
            'coordinat': (65, 193),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'protocol_N': {
            'label_name': ' ',
            'coordinat': (220, 213),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'data_exzam': {
            'label_name': ' ',
            'coordinat': (267, 213),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'director_name': {
            'label_name': ' ',
            'coordinat': (155, 253),
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


def create_dict_label_user_prot():
    dict_label_user = {
        'name_organization': {
            'label_name': ' ',
            'coordinat': (245, 68),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'number_sert': {
            'label_name': ' ',
            'coordinat': (467, 7),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_user': {
            'label_name': ' ',
            'coordinat': (75, 631),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=12),
            'fill': ImageColor.colormap['black']
            },
        'firstname': {
            'label_name': ' ',
            'coordinat': (75, 647),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=12),
            'fill': ImageColor.colormap['black']
            },
        'lastname': {
            'label_name': ' ',
            'coordinat': (75, 662),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=12),
            'fill': ImageColor.colormap['black']
            },
        'name_suborganization': {
            'label_name': ' ',
            'coordinat': (365, 647),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'position': {
            'label_name': ' ',
            'coordinat': (230, 647),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'theme': {
            'label_name': ' ',
            'coordinat': (265, 423),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'course_hourses': {
            'label_name': ' ',
            'coordinat': (165, 480),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'protocol_N': {
            'label_name': ' ',
            'coordinat': (467, 7),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'data_exzam': {
            'label_name': ' ',
            'coordinat': (567, 143),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'director_name': {
            'label_name': ' ',
            'coordinat': (1000,0),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'date_signature': {
            'label_name': ' ',
            'coordinat': (1555, 143),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'status_exzam':{
            'label_name': ' ',
            'coordinat': (500, 647),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_chairman': {
            'label_name': ' ',
            'coordinat': (200, 267),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'position_chairman': {
            'label_name': ' ',
            'coordinat': (500, 267),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_member_1': {
            'label_name': ' ',
            'coordinat': (200, 307),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'position_member_1': {
            'label_name': ' ',
            'coordinat': (500, 307),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_member_2': {
            'label_name': ' ',
            'coordinat': (200, 347),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'position_member_2': {
            'label_name': ' ',
            'coordinat': (500, 347),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'reason_for_checking': {
            'label_name': ' ',
            'coordinat': (590, 647),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'data_order': {
            'label_name': ' ',
            'coordinat': (150, 207),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'number_order': {
            'label_name': ' ',
            'coordinat': (420, 207),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_chairman_sing': {
            'label_name': ' ',
            'coordinat': (220, 720),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_member_1_sing': {
            'label_name': ' ',
            'coordinat': (220, 770),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        'name_member_2_sing': {
            'label_name': ' ',
            'coordinat': (220, 820),
            'text': '',
            'font': ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), size=14),
            'fill': ImageColor.colormap['black']
            },
        }
    return dict_label_user