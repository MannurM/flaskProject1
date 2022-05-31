# utf-8
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


@app.route('/admin', methods=['POST'])
def index():
    if request.method == 'POST':
        name_user = request.form['name']
        user = modules.get_user_byname(name_user)
        #  проверки в базе
        if not user:
            flash('ОШИБКА, проверьте фамилию!')
        else:
            db_psw = user['hpsw']
            form_psw = request.form['psw']
            form_psw = modules.invert_psw(form_psw)  # приведение к нормальному виду
            if check_password_hash(db_psw, form_psw):
                userLogin = UserLogin().create(user)
                rm = True if request.form.get('remainme') else False
                login_user(userLogin, remember=rm)
                user_id = UserLogin.get_id(userLogin)
                session['name'] = request.form['name']
                return redirect(url_for('courses', user_id=user_id))
            else:
                flash('ОШИБКА, проверьте фамилию и пароль')
    return render_template('admin.html')


@app.route('/logout')
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('name', None)
    return redirect(url_for('admin'))


@app.route('/admin_panel/<user_id>')
@login_required
def courses(user_id):
    data = modules.status_user(user_id)
    modules.check_status_exzam(user_id)
    return render_template('admin_panel.html', data=data)