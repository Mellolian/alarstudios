from app import app, db
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, make_response, session
from models import User
from sqlalchemy import and_
import json
import aiohttp
import asyncio


# Главная страница сайта с отображением списка пользователей, если пользователь залогинен
app.config['SECRET_KEY'] = 'super secret'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    # SELECT username FROM public.users

    current_user = request.cookies.get('name')
    cookie = session.get('name')
    if User.query.order_by(User.id.asc()).first():
        User.query.order_by(User.id.asc()).first().privileges = True
    else:
        user = User(username='admin', password='admin')
        db.session.add(user)
    # 'UPDATE public.users SET privileges=true WHERE id = (SELECT id FROM public.users ORDER BY id ASC LIMIT 1)'
    db.session.commit()
    if current_user and User.query.filter(User.username == current_user).first():
        admin = User.query.filter(
            User.username == current_user).first().privileges
    else:
        admin = False

    lst = []
    for i in range(len(users)):
        lst.append(str(users[i]))
# добавление пользователя под записью администратора
    if request.method == "POST" and admin:
        if 'username' in list(request.form.keys()):
            username = request.form.get("username")
            password = request.form.get("password")
            check = User.query.filter(User.username == username).first()
            # SELECT username FROM public.users WHERE username=username LIMIT 1

            if not check and username and password:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                res = make_response("")
                res.headers['location'] = url_for('index')
                flash("You have added user successfully")
                return res, 302
            elif check and username:
                flash('Login already in use')
                return redirect(url_for('index'))
            elif not username or not password:
                flash('Username and password required')
                return redirect(url_for('index'))
        else:
            user = list(request.form.keys())[0]

            # удаление пользователя
            if user in lst and request.form.get((list(request.form.keys())[0])) == 'delete':

                User.query.filter(User.username == user).delete()
                # DELETE FROM public.users WHERE username='user'

                db.session.commit()
                res = make_response("")
                res.headers['location'] = url_for('index')
                return res, 302
            # редактирование пользователя (смена пароля)
            if user in lst and request.form.get((list(request.form.keys())[0])) == 'edit':
                res = make_response("")
                res.headers['location'] = url_for('edit', username=user)
                return res, 302

    return render_template('index.html', title='Home', users=users, username=current_user, cookie=cookie, admin=admin)


# обработка логина пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    name = session.get('name')

    if name:

        res = make_response("")
        res.headers['location'] = url_for('index')
        return res, 302

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        check = User.query.filter(
            and_(User.username == username, User.password == password)).first()
        # 'SELECT username FROM public.users username=username AND password=password ORDER BY id ASC LIMIT 1'

        if check:
            session['name'] = request.form.get('username')
            res = make_response("")
            res.set_cookie("name", request.form.get('username'), 60*60*24*15)
            res.headers['location'] = url_for('index')
            return res, 302
        flash('Wrong login or/and password')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In')

# регистрация пользователя


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = session.get('name')

    if name:
        res = make_response("")
        res.headers['location'] = url_for('index')
        return res, 302
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        check = User.query.filter(User.username == username).first()
        # SELECT * FROM public.users WHERE username=username LIMIT 1
        if not check:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have registered successfully')
            return redirect(url_for('index'))
        flash('Login already in use')
        return redirect(url_for('index'))

    return render_template('register.html', title='Sign up')

# выход из учетной записи


@app.route('/logout')
def logout():
    session['name'] = ''
    res = make_response("")
    res.set_cookie('name', expires=0)
    res.headers['location'] = url_for('index')
    return res, 302

# редактирование пользователя (смена пароля)


@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
    user = session.get('name')
    cookie = session.get('name')
    admin = User.query.filter(User.username == user).first().privileges
    if request.method == "POST" and admin:

        password = request.form.get("password")
        set_admin = (request.form.get("admin") == 'on')
        print(set_admin)
        User.query.filter(User.username == username).update(
            dict(password=password, privileges=set_admin))
        # User.query.filter(User.username == username).update(
        #     dict(privileges=set_admin))
        # UPDATE public.users SET password=password WHERE username=username
        db.session.commit()
        res = make_response("")

        res.headers['location'] = url_for('index')
        return res, 302

    return render_template('edit.html', title='Edit', admin=admin, cookie=cookie)

# асинхронная функция для получения данных из API в виде json


async def fetch(session, url):
    async with session.get(url) as response:
        try:
            return await asyncio.wait_for(response.json(), timeout=2)
        except asyncio.TimeoutError:
            return {}
        except:
            return {}

# асинхронная функция для получения списка объектов и сортировки их по id


async def result():
    tasks = []
    URLS = ['http://127.0.0.1:5000/api/0',
            'http://127.0.0.1:5000/api/2', 'http://127.0.0.1:5000/api/2']
    async with aiohttp.ClientSession() as session:
        for url in URLS:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
    data = []
    for lst in htmls:
        data.extend(lst)
    data = (sorted(data, key=lambda x: x.get('id')))
    return jsonify(data)

# вторая часть задания: псевдо-API


@app.route('/api/<id>', methods=['GET'])
def json_list(id):
    data = []
    try:
        with open(f'data{id}.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}

    return jsonify(data)

# вторая часть задания: получение информации из API


@app.route('/json')
def json_getter():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(result())
    data = asyncio.run(result())
    return data
