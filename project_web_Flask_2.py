# utf-8
import create_user_sert
import modules

from modules import app
from flask import request, render_template, url_for, redirect, flash, session
from flask_login import login_user, login_required
from werkzeug.security import check_password_hash  # generate_password_hash
from UserLogin_2 import UserLogin


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name_user = request.form['name']
        user = modules.get_user_byname(name_user)
        #  проверки в базе
        if not user:
            flash('ОШИБКА, проверьте фамилию!')
        elif check_password_hash(user['hpsw'], request.form['psw']):
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            user_id = UserLogin.get_id(userLogin)
            session['name'] = request.form['name']
            return redirect(url_for('courses', user_id=user_id))
        else:
            flash('ОШИБКА, проверьте фамилию и пароль')
    return render_template('index.html')


@app.route('/logout')
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('name', None)
    return redirect(url_for('index'))


@app.route('/courses/<user_id>')
@login_required
def courses(user_id):
    data = modules.status_user(user_id)
    return render_template('courses.html', data=data)


@app.route('/edu_mat/<user_id>')
@login_required
def edu_mat(user_id):
    data = modules.status_user(user_id)
    id_course, theme, edu_mat, edu_other, edu_additional = modules.get_course()
    data['edu_mat'] = edu_mat
    data['edu_other'] = edu_other
    data['edu_additional'] = edu_additional
    return render_template('edu_mat.html', data=data)


@app.route('/edu_test/<user_id>')
@login_required
def edu_test(user_id):
    data = modules.status_user(user_id=user_id)
    temp_dict, list_answer_just, list_label_use = modules.unpacking_edutest(user_id)
    modules.save_(user_id, list_answer_just, list_label_use)  # Сохранить в БД правильные ответы
    modules.temp_dict = temp_dict
    return render_template('edu_test.html', data=data, temp_dict=temp_dict)


@app.route('/edutest_rezult/,<user_id>', methods=['GET', 'POST'])
@login_required
def edutest_rezult(user_id):
    data = modules.status_user(user_id=user_id)
    list_label_use, list_answer_just, data_answer = None, None, None
    if request.method == 'POST':
        data_answer = request.form.getlist('ans')
        if data_answer:
            sum_answer = len(data_answer)
            if sum_answer > 5:
                print('Ответов больше, чем нужно')
                flash('Ответов больше, чем нужно')
            else:
                data['sum_just'], list_answer_just, data_answer, list_label_use = \
                    modules.read_list_just(user_id, data_answer)
        else:
            flash('Нет отмеченных ответов!')
    data['data_answer'] = data_answer
    data['all_answer'] = list_label_use  # список номеров вопросов
    data['just_answer'] = list_answer_just

    temp_dict = modules.temp_dict
    return render_template('edutest_rezult.html', data=data, temp_dict=temp_dict)


@app.route('/edu_exz/<user_id>')
@login_required
def edu_exz(user_id):
    data = modules.status_user(user_id=user_id)
    temp_dict, list_answer_just, list_label_use = modules.unpacking_edutest(user_id)
    modules.save_(user_id, list_answer_just, list_label_use)  # Сохранить в БД правильные ответы
    modules.temp_dict = temp_dict
    count_prob = data['count_prob']

    if count_prob in [None, 0, 1, 2]:
        count_prob += 1
        data['count_prob'] = count_prob
    else:
        data['message'] = 'Попыток больше нет!'
        return redirect(url_for("courses", user_id=user_id))
    print(data['count_prob'])
    modules.save_status_user(user_id=user_id, data=data)
    return render_template('edu_exz.html', data=data, temp_dict=temp_dict)


@app.route('/eduexz_rezult/,<user_id>', methods=['GET', 'POST'])
@login_required
def eduexz_rezult(user_id):
    data = modules.status_user(user_id=user_id)
    count_prob = data['count_prob']
    list_label_use, list_answer_just, data_answer = None, None, None
    if request.method == 'POST':
        data_answer = request.form.getlist('ans')
        if data_answer:
            sum_answer = len(data_answer)
            if sum_answer > 5:
                print('Ответов больше, чем нужно')
            else:
                data['sum_just'], list_answer_just, data_answer, list_label_use = \
                    modules.read_list_just(user_id, data_answer)
        else:
            flash('Нет отмеченных ответов!')
    data['data_answer'] = data_answer
    data['all_answer'] = list_label_use  # список номеров вопросов
    data['just_answer'] = list_answer_just
    if data['sum_just'] >= 3:
        data['status'] = 'Сдал'
    # if count_prob in [None, 0, 1, 2]:
    #     count_prob += 1
    # else:
    #    data['message'] = 'Попыток больше нет!'
    # data['count_prob'] = count_prob
    modules.save_status_user(user_id=user_id, data=data)

    temp_dict = modules.temp_dict
    return render_template('eduexz_rezult.html', data=data, temp_dict=temp_dict)


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id): 
    data = modules.status_user(user_id=user_id)
    profile_data = modules.getprofile(user_id)
    save_profile = {}
    if request.method == 'POST':
        save_profile['name'] = request.form['name']
        save_profile['firstname'] = request.form['firstname']
        save_profile['lastname'] = request.form['lastname']
        save_profile['dateborn'] = request.form['dateborn']
        save_profile['name_suborganization'] = request.form['name_suborganization']
        save_profile['position'] = request.form['position']
        save_profile['email'] = request.form['email']  # request.form.get('email')
        new_profile_data = modules.check_save_profile(user_id, save_profile, profile_data)
        modules.update_profile(user_id, new_profile_data)
        return redirect(url_for("courses", user_id=user_id))
    return render_template('profile.html', data=data, profile_data=profile_data)


@app.route('/check_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def check_profile(user_id):
    data = modules.status_user(user_id)
    profile_data = modules.getprofile(user_id)
    save_profile = {}
    if request.method == 'POST':
        save_profile['name'] = request.form['name']
        save_profile['firstname'] = request.form['firstname']
        save_profile['lastname'] = request.form['lastname']
        save_profile['dateborn'] = request.form['dateborn']
        save_profile['name_suborganization'] = request.form['name_suborganization']
        save_profile['position'] = request.form['position']
        save_profile['email'] = request.form['email']
        new_profile_data = modules.check_save_profile(user_id, save_profile, profile_data)
        profile_data = new_profile_data
        modules.update_profile(user_id, new_profile_data)
        return redirect(url_for("sertification", user_id=user_id))
    return render_template('check_profile.html', data=data, profile_data=profile_data)


@app.route('/sertification/<user_id>')
@login_required
def sertification(user_id): #   протокол и удостоверение созданы и записаны в БД
    print('sertification')
    # TODO Создать изображения сертификатов
    data_sert = create_user_sert.create_sert(user_id)
    sertificat_file = create_user_sert.past_in_templates_sertificat(data_sert)
    protocol_file = create_user_sert.past_in_templates_protocol(data_sert)
    theme, name_protocol, name_sert = modules.create_name_sert_and_protocol(user_id)

    modules.save_sertificat(user_id, theme, protocol_file, sertificat_file, name_protocol, name_sert)
    return redirect(url_for('courses', user_id=user_id))


@app.route('/register')
def register():
    return render_template('templates_rich/registration.html')


@app.route("/exit")
def exit():
    session.pop('name', None)
    return render_template('exit.html')


@app.route("/create_course", methods=['GET', 'POST'])
def create_course():
    data_course = {}
    if request.method == 'POST':
        data_course['theme'] = request.form['theme']
        print(request.form.get('edu_materials'))  #  ['edu_materials']
        data_course['edu_materials'] = request.form['edu_materials']
        data_course['edu_other'] = request.form['edu_other']
        data_course['edu_additional'] = request.form['edu_additional']
        data_course['template_protocol'] = request.form['template_protocol']
        data_course['template_sertificat'] = request.form['template_sertificat']
        data_course['course_hourses'] = request.form['course_hourses']

        modules.create_course(data_course)
    return render_template('create_course.html')


if __name__ == '__main__':
    app.run(debug=True)
