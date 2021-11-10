import sqlite3 as sql
from datetime import timezone
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Flask
from flask_login import LoginManager, login_manager, UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey, engine, create_engine, inspect
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref, session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()   # Inicializando SALAlchemy 
DB_NAME = 'database.db' # Asignando el nombre de la base de daots
Session = sessionmaker(bind=db)
session = Session()



def crear_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1ab2c3d4e5f6g7'
    app.config['UPLOAD_FOLDER']="static/images"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, ur_lprefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # from .modelos import User, Role, Post, Comment

    create_database(app)

    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('acinoyx_jubatus/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')



#   Aqui se definen los modelos para las tablas en la base de datos
Base = declarative_base() 

role_user = Table(
    "role_user",
    Base.metadata,
    Column("id", Integer, ForeignKey("role.id")),
    Column("id", Integer, ForeignKey("user.id")),
)

user_post = Table(
    "user_post",
    Base.metadata,
    Column("id", Integer, ForeignKey("user.id")),
    Column("id", Integer, ForeignKey("post.id")),
)

user_comment = Table(
    "user_comment",
    Base.metadata,
    Column("id", Integer, ForeignKey("user.id")),
    Column("id", Integer, ForeignKey("comment.id")),
)

post_comment = Table(
    "post_comment",
    Base.metadata,
    Column("id", Integer, ForeignKey("post.id")),
    Column("id", Integer, ForeignKey("comment.id")),
)

class User(db.Model, UserMixin, Base):
    __tablename__ = 'user'   
    id = db.Column(db.Integer, primary_key=True)
    profile_photo = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  # Unique = True hace que no sea posible que dos usuarios tengan el mismo correo
    user_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    age = db.Column(db.String(3))
    posts = relationship("Post", backref=backref("user"))
    comments = db.relationship("Comment", backref=backref("user"))
    role_id = db.Column(Integer, ForeignKey('role.id'))
    
class Role(db.Model, UserMixin, Base):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    users = db.relationship("User", backref=backref("role"))


class Post(db.Model, UserMixin, Base):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String)
    foot_note = db.Column(db.String)
    post_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer)
    photo_user_name = db.Column(db.String, ForeignKey('user.user_name'))
    comments = db.relationship("Comment", backref=backref("post"))

class Comment(db.Model, UserMixin, Base):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    comment = db.Column(db.String) 
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    like = db.Column(db.Integer)

