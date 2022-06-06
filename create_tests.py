# utf-8
import openpyxl
import sqlite3
from FDataBase import FDataBase


# конфигурация
DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'  # TODO сделать отдельный файл с паролем


def connect_db():
    conn = sqlite3.connect('pr_ot.db')
    conn.row_factory = sqlite3.Row
    return conn


def unpacking_file():
    path = "static/courses/test_ot.xlsx"
    wb_obj = openpyxl.load_workbook(path)
    sheet = wb_obj.active
    max_rows = sheet.max_row
    j = 2
    id_qestion = 0
    dict_id_qestion = {}
    for i in range(2, max_rows):
        cell_obj = sheet.cell(row=i, column=j)
        qestion = cell_obj.value
        cell_obj_1 = sheet.cell(row=i, column=j + 1)
        answer_1 = cell_obj_1.value
        cell_obj_2 = sheet.cell(row=i, column=j + 2)
        answer_2 = cell_obj_2.value
        cell_obj_3 = sheet.cell(row=i, column=j + 3)
        answer_3 = cell_obj_3.value
        cell_obj_4 = sheet.cell(row=i, column=j + 4)
        answer_4 = cell_obj_4.value
        cell_obj_5 = sheet.cell(row=i, column=j + 5)
        number_answer_just = cell_obj_5.value

        if number_answer_just == 1:
            answer_just = answer_1
        elif number_answer_just == 2:
            answer_just = answer_2
        elif number_answer_just == 3:
            answer_just = answer_3
        elif number_answer_just == 4:
            answer_just = answer_4
        else:
            print('ошибка,  нет правильного ответа', number_answer_just)
            continue
        # Компоновка словаря с данными
        id_qestion += 1
        list_answers = [answer_1, answer_2, answer_3, answer_4]
        dict_id_qestion[id_qestion] = {'qestion': qestion, 'list_answers': list_answers, 'answer_just': answer_just}

    return dict_id_qestion


# проверка на дубли, если будет полный тезка то его удалит
# TODO эта проверка только в тексте файла, а есть еще  и БД???
def del_double(dict_id_qestion):
    dict_qestion = dict_id_qestion
    double_key = []
    key_lict = []
    for id_qestion, value in dict_qestion.items():
        # print(id_qestion, value)
        for key, val in value.items():
            # print(key, val)
            if key == 'qestion':
                # print('qestion')
                if dict_qestion[id_qestion][key] not in key_lict:
                    # print('добавлен вопрос в лист вопросов')
                    key_lict.append(dict_qestion[id_qestion][key])
                else:
                    # print('добавлен двойной вопрос')
                    double_key.append(id_qestion)  # cоздание списка двойных ключей
                    continue
            else:
                continue
    # удаление ключей в словаре из списка дублей
    for id_qestion in double_key:
        del dict_id_qestion[id_qestion]
    return dict_qestion


def save_in_db(dict_rezult):
    db = connect_db()
    dbase = FDataBase(db)
    dict_rezult = dict_rezult
    for id_qestion, value in dict_rezult.items():
        qestion_txt, list_answers, answer_just = None, [], None,
        for key, val in value.items():
            if key == 'qestion':
                qestion_txt = dict_rezult[id_qestion][key]
            elif key == 'list_answers':
                list_answers = dict_rezult[id_qestion][key]
                print(list_answers)
            elif key == 'answer_just':
                answer_just = dict_rezult[id_qestion][key]
        print('save_in_db', id_qestion, qestion_txt, list_answers, answer_just)
        dbase.create_test(qestion_txt, list_answers, answer_just)


if __name__ == '__main__':
    dict_id_qestion = unpacking_file()
    dict_rezult = del_double(dict_id_qestion)
    save_in_db(dict_rezult)
    # print(dict_rezult)
