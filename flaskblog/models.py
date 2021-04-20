from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
now = datetime.now()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default1.jpg')
    password = db.Column(db.String(60), nullable=False)
    passes = db.relationship('Pass', backref='author', lazy=True)
    wallet = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"User('{self.fullname}','{self.username}','{self.email}','{self.image_file}', '{self.wallet})"

class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    dest = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False, default=200)
    pass_type = db.Column(db.String(100), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False,default=datetime.now)
    expiry = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User Pass('{self.source}', '{self.dest}', '{self.date}', '{self.user_id}', '{self.id}')"


def init_db():
    db.create_all()
    db.session.commit()
    
if __name__ == '__main__':
    init_db()

