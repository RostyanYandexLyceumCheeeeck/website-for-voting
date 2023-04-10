import datetime
import os
import sqlite3
import time
import random

from flask import Flask, render_template, redirect, make_response, jsonify, request, session
from dotenv import load_dotenv
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from flask_restful import Api
from wtforms import MultipleFileField, SubmitField
from flask_wtf import FlaskForm

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


class ImageForm(FlaskForm):
    images = MultipleFileField('Select Images')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def start_screan():
    return render_template('start_scr.html')


@app.route('/create', methods=['GET', 'POST'])
def start_scre1an():
    form = ImageForm()
    test_name = request.form.get('test-name')
    test_description = request.form.get('test-description')
    test_type = request.form.get('test-type')
    test_kol = request.form.get('test-kol')
    if test_kol is None:
        return render_template('create.html', flag=False, form=form, file=False)
    else:
        try:
            test_kol = int(test_kol)
        except Exception:
            return render_template('create.html', flag=True, form=form, file=False)
        if len(form.images.data) != 1:
            return render_template('create.html', flag=True, form=form, file=True)
        filename = form.images.data[0].filename
        file = form.images.data[0]
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.jfif')):
            path = os.path.join('static/images', filename)
            file.save(path)
        else:
            return render_template('create.html', flag=True, form=form, file=True)
        data = {}
        data['test_name'] = test_name
        data['test_description'] = test_description
        data['test_type'] = test_type
        data['test_kol'] = test_kol
        data['preview'] = path
        session['img'] = data
        test = {"head": data, 'question': []}
        session['test'] = test
        return redirect('/img')


@app.route('/img', methods=['GET', 'POST'])
def upload_images():
    form = ImageForm()
    test = session.get('test', None)
    session['test'] = test
    kol_img = session.get('img', None)['test_kol']
    if form.validate_on_submit():
        ls_name = [image.filename for image in form.images.data]
        session['img_name'] = ls_name
        ls_is_file = [os.path.isfile(image.filename) for image in form.images.data]
        ls_is_img = [not x for x in ls_is_file]
        if all(ls_is_img) and len(form.images.data) == \
                kol_img:
            for image in form.images.data:
                filname = image.filename
                path = os.path.join('static/images', filname)
                image.save(path)
            return redirect("/add")
        else:
            return render_template('img.html', form=form, isimg=True, kol=kol_img)
    return render_template('img.html', form=form, isimg=False, kol=kol_img)


@app.route('/add', methods=['GET', 'POST'])
def add_text_question():
    name_img = session.get('img_name', None)
    message = ''
    if request.method == 'POST':
        if request.form.get('next') is None:
            question = request.form.get('question')
            description = request.form.get('description')
            id_ = request.form.get('id')
            que = {}
            que['question'] = question
            que['description'] = description
            content = {'id': id_, 'data': que}
            test = session.get('test', None)
            data = test['question']
            asd = list(filter(lambda x: x['id'] == id_, data))
            if len(asd) == 0:
                test['question'].append(content)
            else:
                ind = test['question'].index(*asd)
                test['question'][ind] = content
            session['test'] = test
        else:
            test = session.get('test', None)
            data = test['question']
            print(data)
            id = list(map(int, list(i['id'] for i in data)))
            need_id = []
            for i in range(len(name_img)):
                if i not in id:
                    need_id.append(i)
            need_id = list(map(lambda x: x + 1, need_id))
            if len(need_id) != 0:
                return render_template('add_text_question.html', img=name_img, ln=len(name_img), mas=need_id)
            else:
                return redirect('/')
    return render_template('add_text_question.html', img=name_img, ln=len(name_img), mas=[])

@app.route('/test')
def index():
    items = [
        {
            "title": "Item 1",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 1",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "title": "Item 2",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 2",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "title": "Item 3",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 3",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "title": "Item 2",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 2",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "title": "Item 2",
            "image": "https://via.placeholder.com/300x300",
            "description": "GHBdtn Как дела соси у ле   йм чмо придор уелбан ты ",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        }
    ]
    return render_template('test_change.html', items=items)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


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
        return redirect('/profile')
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
    db_session.global_init('db/DBase.sqlite')
    session = db_session.create_session()
    my_test = data.tests.Test()
    #     #
    zxc = {'answers': [{'file': {'name': 'image', 'created_date': '2023-04-06 12:29:34',
                                 'path': '/path/to/image', 'id': 3, 'answer_id': 3}, 'id': 3, 'name': 'first_answer',
                                 'test_id': 3, 'description': 'pervii otvet'},
                       {'file': {'name': 'two_image', 'created_date': '2023-04-06 12:29:34',
                                 'path': '/path/to/do', 'id': 4, 'answer_id': 4}, 'id': 4, 'name': 'second_answer',
                                 'test_id': 3, 'description': 'vtoroii otvet'}],
           'id': 3, 'created_date': '2024-04-06 12:29:34', 'user_id': 1, 'is_published': False,
           'description': 'qweqweqwe', 'image': '/path', 'name': 'first_test', 'type': 'Image'}
    my_test.insert_test(session=session, **zxc)
    qwe = my_test.get_test(session, 3)
    print(qwe)
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
