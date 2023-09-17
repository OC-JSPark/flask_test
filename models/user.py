from googlekaap import db   ## init.py에서 sqlalchemy가 정의되있는거 불러오기

## class는 이제 sql에서 table이 될것이다. 거기서 table명이 User이다.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    