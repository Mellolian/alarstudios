import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Fljufk93@localhost/alar"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


import routes

if __name__ == '__main__':
    app.run()

