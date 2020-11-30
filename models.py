from . import db


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone = db.Column(db.String())
    sex = db.Column(db.String())
    birth_day = db.Column(db.DateTime())
    friend_rank = db.Column(db.String())
    hobby = db.Column(db.String())

    def __repr__(self):
        return f"friend('{self.name}', '{self.last_name}', '{self.friend_rank}')"
