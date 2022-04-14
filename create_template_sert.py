# utf-8
import os
from PIL import Image, ImageDraw, ImageColor, ImageFont

#  скачать файл фона от организатора
#  скачать названия полей - наименование организации, должность, подпись,  тема  и другие
#  взять из формы запроса информации - содержание полей. сохранить в БД
#  сохранить шаблон в БД
def open_fon():
    font_path = os.path.join('fonts', 'arial.ttf')
    path_teplate = os.path.normpath(os.getcwd() + '/' + 'images/templ.png')
    image_teplate = Image.open(path_teplate)
    draw = ImageDraw.Draw(image_teplate)
    print(path_teplate)
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
    text = 'Выдано'
    draw.text((5, 95), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Место работы'
    draw.text((5, 115), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Должность'
    draw.text((5,135), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Проведена проверка знаний требований охраны труда по'
    draw.text((5,155), text, font=font, fill=ImageColor.colormap['black'])
    text = 'в объеме'
    draw.text((5, 195), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Протокол заседания комиссии'
    draw.text((5, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = '№'
    draw.text((205, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = 'от'
    draw.text((245, 215), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Директор (руководитель)'
    draw.text((5, 255), text, font=font, fill=ImageColor.colormap['black'])
    text = 'Дата'
    draw.text((5, 285), text, font=font, fill=ImageColor.colormap['black'])



    # draw.text((286, 259), date, font=font, fill=ImageColor.colormap['black'])  # время
    print('!!!!')

    file = 'template_sert.png'
    # TODO Изменить путь сохранения  изображения
    path_file = os.path.normpath(os.getcwd() + '/' + 'static/templates_sert/')
    image_teplate.save(file)
    # image_teplate.show()
    # TODO стнадартизировать размер изображения!! на А5
open_fon()