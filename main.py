import datetime
import os
import sqlite3
import time
import random

from flask import Flask, render_template, redirect, make_response, jsonify, request, session, url_for
from dotenv import load_dotenv
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from flask_restful import Api
from wtforms import MultipleFileField, SubmitField
from flask_wtf import FlaskForm

from data import db_session
from data.__all_models import User, Test
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
        data['answers'] = []
        session['test'] = data
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
                filename = image.filename
                path = os.path.join('static/images', filename)
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
        test = session.get('test', None)
        data = test['answers']
        if request.form.get('next') is None:
            question = request.form.get('question')
            description = request.form.get('description')
            id_ = int(request.form.get('id'))
            que = {}
            que['path'] = os.path.join('static/images', name_img[int(id_)])

            answer = {'file': que, 'name': question, 'description': description, 'id': id_}
            asd = list(filter(lambda x: x['id'] == id_, data))
            if len(asd) == 0:
                test['answers'].append(answer)
            else:
                ind = test['answers'].index(*asd)
                test['answers'][ind] = answer
            session['test'] = test
        else:
            test = session.get('test', None)
            data = test['question']
            id = list(map(int, list(i['id'] for i in data)))
            need_id = []
            for i in range(len(name_img)):
                if i not in id:
                    need_id.append(i)
            need_id = list(map(lambda x: x + 1, need_id))
            if len(need_id) != 0:
                return render_template('add_text_question.html', img=name_img, ln=len(name_img), mas=need_id)
            else:
                test = session.get('test', None)

                return redirect('/')
                answers = []
                for answer in test['answers']:
                    answer.pop('id')
                    answers.append(answer)
                test_to_db = {
                    'is_published': test['test_type'] != 'hidden',
                    'description': test['test_description'],
                    'image': test['preview'],
                    'name': test['test_name'],
                    'user_id': session['user_id'],
                    'answers': answers
                }
                my_test = Test()
                db_sess = db_session.create_session()
                my_test.insert_test(db_sess, **test_to_db)
                return redirect('/profile')
    return render_template('add_text_question.html', img=name_img, ln=len(name_img), mas=[])


@app.route('/tests', methods=['GET', 'POST'])
def change_test():
    session['all'] = None
    session['choise'] = 0
    items = [
        {
            "id": 1,
            "title": "Item 1",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 1",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "id": 2,
            "title": "Item 2",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 2",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "id": 3,
            "title": "Item 3",
            "image": "https://via.placeholder.com/300x300",
            "description": "Description of Item 3",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "id": 4,
            "title": "Item 2",
            "image": "/static/images/end.gif",
            "description": "Description of Item 2",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        },
        {
            "id": 5,
            "title": "Item 2",
            "image": "/static/images/end.gif",
            "description": "GHBdtn",
            "detail1": "qwe",
            "detail2": "qwe",
            "detail3": "qwe"
        }
    ]
    if request.method == 'POST':
        content = request.json
        session['id'] = content['id']
        return redirect('/test')
    return render_template('test_change.html', items=items)


@app.route('/test', methods=['GET', 'POST'])
def test():
    zxc = {'answers': [{'file': {'created_date': '2023-04-06 12:29:34',
                                 'path': '/static/images/end.gif', 'id': 3, 'answer_id': 3}, 'id': 3,
                        'name': 'first_answer',
                        'test_id': 3, 'description': 'pervii otvet'},
                       {'file': {'created_date': '2023-04-06 12:29:34',
                                 'path': '/static/images/end1.gif', 'id': 4, 'answer_id': 4}, 'id': 4,
                        'name': 'second_answer',
                        'test_id': 3, 'description': 'vtoroii otvet'}, {'file': {'created_date': '2023-04-06 12:29:34',
                                                                                 'path': '/static/images/Снимок экрана (48).png',
                                                                                 'id': 4, 'answer_id': 4}, 'id': 4,
                                                                        'name': 'second_answer',
                                                                        'test_id': 3, 'description': 'vtoroii otvet'},
                       {'file': {'created_date': '2023-04-06 12:29:34',
                                 'path': '/static/images/left.png', 'id': 3, 'answer_id': 3}, 'id': 3,
                        'name': 'first_answer',
                        'test_id': 3, 'description': 'pervii otvet'},
                       {'file': {'created_date': '2023-04-06 12:29:34',
                                 'path': '/static/images/right.png', 'id': 4, 'answer_id': 4}, 'id': 4,
                        'name': 'second_answer',
                        'test_id': 3, 'description': 'vtoroii otvet'}, {'file': {'created_date': '2023-04-06 12:29:34',
                                                                                 'path': '/static/images/Снимок экрана (48).png',
                                                                                 'id': 4, 'answer_id': 4}, 'id': 4,
                                                                        'name': 'second_answer',
                                                                        'test_id': 3, 'description': 'vtoroii otvet'}],
           'info': {'id': 3, 'created_date': '2024-04-06 12:29:34', 'user_id': 1, 'is_published': False,
                    'description': 'qweqweqwe', 'image': '/path', 'name': 'first_test', 'type': 'Image'}}
    session['test_inf'] = zxc['info']
    if session.get('all', None) is not None:
        ls_in_suit = session['ls_in_suit']
        ls_all = session['all']
    else:
        ls_all = zxc['answers']
        ls_in_suit = random.sample(ls_all, 2)
        for ans in ls_in_suit:
            ls_all.remove(ans)
        session['all'] = ls_all
        session['ls_in_suit'] = ls_in_suit

    if request.method == 'POST':
        content = request.json
        session['all'] = ls_all
        if content['section'] == 'left':
            if len(ls_all) == 0:
                session['win'] = ls_in_suit[0]
                return redirect('/test/end')
            rem = random.sample(ls_all, 1)
            ls_in_suit = [ls_in_suit[0]] + rem
            session['choise'] = 1
            ls_all.remove(*rem)
        else:
            if len(ls_all) == 0:
                session['win'] = ls_in_suit[1]
                return redirect('/test/end')
            rem = random.sample(ls_all, 1)
            ls_in_suit = [ls_in_suit[1]] + rem
            session['choise'] = 2
            ls_all.remove(*rem)
        session['ls_in_suit'] = ls_in_suit
        return redirect('/test')
    left = ls_in_suit[0]
    right = ls_in_suit[1]
    return render_template('test_inf.html', left=left, right=right, choise=session['choise'])


@app.route('/test/end', methods=['GET', 'POST'])
def end():
    form = ImageForm()
    inf = session['test_inf']
    if request.method == 'POST':
        dictt = request.form.to_dict()
        if dictt == {}:
            return redirect('/')
        else:
            return redirect('/')  # СЮДА НАДО ДОБАВИТЬ ДОБАВЛЕНИЕ РЕЙТИНГА В ДБ
    return render_template('end.html', win=session['win'], inf=inf, form=form)


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
            session['user_id'] = user.id
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
        session['user_id'] = None
        logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/DBase.sqlite')
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
