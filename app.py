


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

port = 5433
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://admin:admin@localhost:{port}/alar"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
import routes
if __name__ == '__main__':
    app.run()
