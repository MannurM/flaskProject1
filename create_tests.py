# utf-8
# сделать из экселя??
import openpyxl

import modules
import os
import datetime
import sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash
from modules import app
from flask import request, render_template, url_for, redirect, flash, session, send_from_directory
from flask_login import login_user, login_required
from werkzeug.security import check_password_hash  # generate_password_hash
from UserLogin_2 import UserLogin


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'  # TODO сделать отдельный файл с паролем


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def unpacking_file():
    path = "test_ot.xlsx"
    wb_obj = openpyxl.load_workbook(path)
    sheet = wb_obj.active
    max_rows = sheet.max_row
    j = 2
    id_qestion = 0
    dict_id_qestion = {}
    for i in range(2, max_rows):
        cell_obj = sheet.cell(row=i, column=j)
        qestion = cell_obj.value

        cell_obj = sheet.cell(row=i, column=j + 1)
        answer_1 = cell_obj.value

        cell_obj = sheet.cell(row=i, column=j + 2)
        answer_2 = cell_obj.value

        cell_obj = sheet.cell(row=i, column=j + 3)
        answer_3 = cell_obj.value

        cell_obj = sheet.cell(row=i, column=j + 4)
        answer_4 = cell_obj.value

        cell_obj = sheet.cell(row=i, column=j + 5)
        number_answer_just = cell_obj.value
        if number_answer_just == 1:
            answer_just = answer_1
        elif number_answer_just == 2:
            answer_just = answer_2
        elif number_answer_just == 3:
            answer_just = answer_3
        elif number_answer_just == 4:
            answer_just = answer_4
        else:
            print('ошибка,  не правильного ответа')
            continue
        # Компоновка словаря с данными
        id_qestion += 1
        list_answers = [answer_1, answer_2, answer_3, answer_4]
        dict_id_qestion[id_qestion] = {'qestion': qestion, 'list_answers': list_answers, 'answer_just': answer_just}
    return dict_id_qestion


# проверка на дубли, если будет полный тезка то его удалит
def del_double(dict):
    dict_qestion = dict
    double_key = []
    key_lict = []
    for id_qestion, value in dict_qestion.items():
        for key, val in value.items():
            if key == 'qestion':
                if dict_qestion[key] not in key_lict:
                    key_lict = dict_qestion[key]
                else:
                    double_key.append(id_qestion)  # cоздание списка двойных ключей
                    continue
        else:
            continue
    # удаление ключей в словаре из списка дублей
    for id_qestion in double_key:
        del dict_id_qestion[id_qestion]
    return dict_qestion


def save_in_db(dict):
    db = connect_db()
    dbase = FDataBase(db)
    dict_rezult = dict
    for id_qestion, value in dict_rezult.items():
        qestion_txt, answer_1, answer_2, answer_3, answer_4, answer_just = None, None, None, None, None, None
        for key, val in value.items():
            if key == 'qestion':
                qestion_txt = value[key]
            elif key == 'list_answer':
                answer_1 = value[key][0]
                answer_2 = value[key][1]
                answer_3 = value[key][2]
                answer_4 = value[key][3]
            elif key == 'answer_just':
                answer_just = value[key]
        dbase.create_test(id_qestion, qestion_txt, answer_1, answer_2, answer_3, answer_4, answer_just)
# TODO сделать проверку на корректность шаблона excel


if __name__ == '__main__':
    dict_id_qestion = unpacking_file()
    dict_rezult = del_double(dict_id_qestion)
    save_in_db(dict_rezult)
    # print(dict_rezult)
