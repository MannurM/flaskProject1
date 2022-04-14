# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

import os
from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(fio, from_, to, date, out_name_file=None):
    fio, from_, to, date = fio, from_, to, date
    font_path = os.path.join('fonts', 'arial.ttf')
    path_teplate = os.path.normpath(os.getcwd() + '/' + 'images/ticket_template.png')

    image_teplate = Image.open(path_teplate)
    draw = ImageDraw.Draw(image_teplate)
    print(path_teplate)
    font = ImageFont.truetype(font_path, size=18)

    draw.text((45, 120), fio, font=font, fill=ImageColor.colormap['black'])  # ФИО
    draw.text((45, 190), from_, font=font, fill=ImageColor.colormap['black'])  # откуда
    draw.text((45, 255), to, font=font, fill=ImageColor.colormap['black'])  # куда
    font = ImageFont.truetype(font_path, size=14)
    draw.text((286, 259), date, font=font, fill=ImageColor.colormap['black'])  # время

    image_teplate .show()
    out_name_file = out_name_file if out_name_file else 'probe_ticket.png'
    image_teplate.save(out_name_file)
    print(f'Post card saved az {out_name_file}')


if __name__ == '__main__':
    make_ticket(fio='Пирцхилава Ираклий Батькович', from_='Лондон', to='Париж', date='01.01.2021')