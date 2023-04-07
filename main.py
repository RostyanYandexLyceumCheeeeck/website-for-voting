import datetime
import os
import time
import random

from flask import Flask, render_template, redirect, make_response, jsonify
from dotenv import load_dotenv
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from flask_restful import Api

import data.tests
from data import db_session
from data.__all_models import User
from forms.registerForm import RegisterForm
from forms.loginForm import LoginForm
from resources import user_resource

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
api = Api(app)
api.add_resource(user_resource.UserListResource, '/api/v2/users')
api.add_resource(user_resource.UserResource, '/api/v2/users/<int:user_id>')
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def start_screan():
    return render_template('start_scr.html')


@app.route('/create', methods=['GET', 'POST'])
def start_scre1an():
    return render_template('create.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        time.sleep(random.random())
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile', methods=['GET'])
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html')
    return redirect("/login")


@app.route('/settings-profile', methods=['GET'])
def settings_profile():
    if current_user.is_authenticated:
        return render_template('settings-profile.html')
    return redirect("/login")


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/DataBase.sqlite')
    session = db_session.create_session()
    my_test = data.tests.Test()
    qwe = my_test.get_test(session, 1)
    print(qwe)
    zxc = {'questions': [{'id': 3, 'name': 'first_question', 'test_id': 3, 'description': 'vopros',
                          'answers': [{'file': {'name': 'image', 'created_date': '2023-04-06 12:29:34',
                                                'path': '/path/to/image', 'id': 3}, 'id': 3, 'name': 'first_answer',
                                       'question_id': 3, 'description': 'pervii otvet', 'file_id': 3},
                                      {'file': {'name': 'two_image', 'created_date': '2023-04-06 12:29:34',
                                                'path': '/path/to/do', 'id': 4}, 'id': 4, 'name': 'second_answer',
                                       'question_id': 3, 'description': 'vtoroii otvet', 'file_id': 4}]}], 'id': 3,
           'created_date': '2024-04-06 12:29:34', 'is_published': False, 'description': 'qweqweqwe', 'image': '/path',
           'name': 'first_test', 'type': 'Image'}
    my_test.insert_test(session=session, **zxc)
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
