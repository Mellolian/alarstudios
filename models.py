from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String(25))
    privileges = db.Column(db.Boolean, default=False, nullable=False)


    def __init__(self, username, password, privileges=False):
        self.username = username
        self.password = password
        self.privileges = privileges


    def __repr__(self):
        return str(self.username)
