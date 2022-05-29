import io
import os
import sqlite3
from FDataBase import FDataBase
from PIL import Image, ImageDraw, ImageColor, ImageFont


def open_fon():
    font_path = os.path.join('fonts', 'arial.ttf')
    path_template = os.path.normpath(os.getcwd() + '/' + 'images/protokol_ot.jpg')
    image_template = Image.open(path_template)
    draw = ImageDraw.Draw(image_template)
    file = 'template_prot.png'
    image_template.save(file)
    file = image_to_byte_array(image_template)
    return file


def read_names_courses():
    pass


def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def save_in_subd(file_sert):
    data_file = {}
    data_file['theme'] = 'Охрана труда'
    data_file['template_protocol'] = file_sert
    data_file['name_template_protocol'] = 'protocol.jpg'
    db = connect_db()
    dbase = FDataBase(db)
    dbase.create_template_prot(data_file)
    return


def convert_blob(file):
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