from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '925709c46e120ecd46eb5aa502757785'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lqadnwzpkfpxik:10427c1c4db815184bbce51e127aa0cbfd6e6e1177e8b67275f682cdf65ce14c@ec2-52-21-252-142.compute-1.amazonaws.com:5432/d8gh3145k53ho9'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes