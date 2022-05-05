# utf-8
import io
import os
import sqlite3
from FDataBase import FDataBase
from PIL import Image, ImageDraw, ImageColor, ImageFont


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

#  скачать файл фона от организатора
#  скачать названия полей - наименование организации, должность, подпись,  тема  и другие
#  взять из формы запроса информации - содержание полей. сохранить в БД
#  сохранить шаблон в БД


def open_fon():
    font_path = os.path.join('fonts', 'arial.ttf')
    path_template = os.path.normpath(os.getcwd() + '/' + 'images/templ.png')
    image_template = Image.open(path_template)
    draw = ImageDraw.Draw(image_template)
    print(path_template)
    font = ImageFont.truetype(font_path, size=14)
    text = 'УДОСТОВЕРЕНИЕ'
    draw.text((130, 5), text, font=font, fill=ImageColor.colormap['black'])
    text = 'О ПРОВЕРКЕ ЗНАНИЙ ТРЕБОВАНИЙ ОХРАНЫ ТРУДА'
    draw.text((30, 20), text, font=font, fill=ImageColor.colormap['black'])
    text = '____________________________________________________'
    draw.text((5, 40), text, font=font, fill=ImageColor.colormap['black'])
    font = ImageFont.truetype(font_path, size=10)
    text = '(полное наименование организации)'
    draw.text((115, 55), text, font=font, fill=ImageColor.colormap['black'])
    font = ImageFont.truetype(font_path, size=14)
    text = 'УДОСТОВЕРЕНИЕ № '
    draw.text((120, 75), text, font=font, fill=ImageColor.colormap['black'])
    font = ImageFont.truetype(font_path, size=12)
    text = 'ФИО: '
    draw.text((5, 95), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Место работы: '
    draw.text((5, 115), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Должность: '
    draw.text((5, 135), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Прошел(прошла) проверку знаний требований '
    draw.text((5, 155), text, font=font, fill=ImageColor.colormap['black'])
    text = 'по теме: '
    draw.text((5, 175), text, font=font, fill=ImageColor.colormap['black'])
    text = 'в объеме:'
    draw.text((5, 195), text, font=font, fill=ImageColor.colormap['black'])
    text = ' часов '
    draw.text((95, 195), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Протокол заседания комиссии'
    draw.text((5, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = '№'
    draw.text((205, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = 'от'
    draw.text((245, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Директор '
    draw.text((5, 255), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Дата'
    draw.text((5, 285), text, font=font, fill=ImageColor.colormap['black'])
    # draw.text((286, 259), date, font=font, fill=ImageColor.colormap['black'])  # время

    file = 'template_sert.png'
    # Изменить путь сохранения  изображения
    path_file = os.path.normpath(os.getcwd() + '/' + 'static/templates_sert/')
    # image_teplate.show()
    # перейти в директорию для сохранения файла
    os.chdir(path_file)
    image_template.save(file)
    file = image_to_byte_array(image_template)

    # file = image_template.save(file)

    # TODO стандартизировать размер изображения!! на А5
    print(type(file))
    return file


def read_names_courses():
    pass


def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def save_in_subd(file_sert):
    db = connect_db()
    dbase = FDataBase(db)
    data_file = {}
    # file_convert = convert_blob(file_sert)  # TODO нужно сконвертировать в  бинарный файл
    data_file['theme'] = 'Охрана труда'
    data_file['template_sertificat'] = file_sert
    data_file['name_template_sertificat'] = 'sertificat.png'
    dbase.create_template_sert(data_file)
    # dbase.save_insubd(file)


def convert_blob(file):
    print(type(file), file)
    with open(file, 'rb') as f:
        file_blob = f.read()
        return file_blob


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    file_sert = open_fon()
    save_in_subd(file_sert)

