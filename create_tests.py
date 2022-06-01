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
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


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
    dict_qestion = {}
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
            answer_just = 0
            print('ошибка,  не правильного ответа')
            continue  # TODO  выкинуть этот вопрос!
        # Компоновка словаря с данными
        id_qestion += 1
        list_answers = [answer_1, answer_2, answer_3, answer_4]
        dict_qestion[id_qestion] = {'qestion': qestion, 'list_answers': list_answers, 'answer_just': answer_just}
    return dict_qestion


# TODO сделать проверку на корректность шаблона excel
# TODO  сделать функцию записи в БД
if __name__ == '__main__':
    pass

