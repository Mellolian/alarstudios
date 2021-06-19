from sqlalchemy.sql.expression import delete
from app import app, db
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, make_response, session
from models import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import json, aiohttp, asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def result():
    tasks = []
    URLS = ['http://127.0.0.1:5000/api/0', 'http://127.0.0.1:5000/api/1', 'http://127.0.0.1:5000/api/2']
    async with aiohttp.ClientSession() as session:
        for url in URLS:        
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
    data = []
    for lst in htmls:
        data.extend(lst)
    data = (sorted(data, key=lambda x: x.get('id')))
    return jsonify(data)


app.config['SECRET_KEY'] = 'super secret'
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    current_user = request.cookies.get('name')
    cookie = session.get('name')
    User.query.order_by(User.id.asc()).first().privileges = True
    db.session.commit()
    if (str(User.query.order_by(User.id.asc()).first()) == current_user):
        admin = True
    else:
        admin = False

    lst = []
    for i in range(len(users)):
        lst.append(str(users[i]))

    if request.method == "POST":
        if 'username' in list(request.form.keys()):
            username = request.form.get("username")
            password = request.form.get("password")
            check = User.query.filter(User.username==username).all()

            if not check:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                res = make_response("")
                res.headers['location'] = url_for('index')
                return res, 302
            else:
                flash('Login already in use')    
                return redirect(url_for('index'))
        else:
            user = list(request.form.keys())[0]

            if user in lst and request.form.get((list(request.form.keys())[0])) == 'delete':

                User.query.filter(User.username==user).delete()

                db.session.commit()
                res = make_response("")
                res.headers['location'] = url_for('index')
                return res, 302
            
            if user in lst and request.form.get((list(request.form.keys())[0])) == 'edit':
                res = make_response("")
                res.headers['location'] = url_for('edit',username=user)
                return res, 302
 
    return render_template('index.html', title='Home', users=users, username=current_user, cookie=cookie, admin=admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    name = session.get('name')

    if name:

        res = make_response("")
        res.headers['location'] = url_for('index')
        return res, 302

    if request.method == "POST":
        username= request.form.get("username")
        password = request.form.get("password")
        

        check = User.query.filter(and_(User.username==username, User.password==password)).first()

        if check:
            session['name'] = request.form.get('username')
            res = make_response("")
            res.set_cookie("name", request.form.get('username'), 60*60*24*15)
            res.headers['location'] = url_for('index')
            return res, 302
        flash('Wrong login or/and password')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In')

@app.route('/register', methods=['GET', 'POST'])
def register():
    name = session.get('name')

    if name:
        res = make_response("")
        res.headers['location'] = url_for('index')
        return res, 302
    if request.method == "POST":
        username= request.form.get("username")
        password = request.form.get("password")

        check = User.query.filter(User.username==username).all()
        if not check:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have registered successfully')
            return redirect(url_for('index'))
        flash('Login already in use')    
        return redirect(url_for('index'))

    return render_template('register.html', title='Sign up')

@app.route('/logout')
def logout():
    session['name'] = ''
    res = make_response("")
    res.set_cookie('name', expires=0)
    res.headers['location'] = url_for('index')
    return res, 302

@app.route('/edit/<username>', methods=['GET','POST'])
def edit(username): 
    user = session.get('name')
    cookie = session.get('name')
    if (str(User.query.order_by(User.id.asc()).first()) == user):
        admin = True
    else:
        admin = False
    if request.method == "POST":
        password = request.form.get("password")
        User.query.filter(User.username==username).update(dict(password=password))
        db.session.commit()
        res = make_response("")

        res.headers['location'] = url_for('index')
        return res, 302

    return render_template('edit.html', title='Edit', admin=admin, cookie=cookie)

@app.route('/add', methods=['GET','POST'])
def add(): 
    cookie = session.get('name')
    if (str(User.query.order_by(User.id.asc()).first()) == cookie):
        admin = True
    else:
        admin = False

    if request.method == "POST":
        username= request.form.get("username")
        password = request.form.get("password")

        check = User.query.filter(User.username==username).all()
        if not check:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

             
            flash("You have added user successfully")    
            return redirect(url_for('index'))
        else:

            flash('Login already in use')    
            return redirect(url_for('add'))

    return render_template('add.html', title='Sign up', cookie=cookie, admin=admin)
  
@app.route('/api/<id>',methods=['GET'])
def json_list(id):
    data = []
    with open(f'data{id}.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/json')
def json_getter():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(result())  
    data = asyncio.run(result())
    return data

if __name__ == '__main__':
    app.run()