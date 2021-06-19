# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os
# # from models import Result

# app = Flask(__name__)
# app.config.from_object('config')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///alar"
# db = SQLAlchemy(app)




# @app.route('/')
# def hello():
#     return "Hello World!"


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)


# if __name__ == '__main__':
#     app.run()