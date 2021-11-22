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

class Baraja(db.Model, UserMixin, Base):
    __tablename__ = 'baraja'
    id = db.Column(db.Integer, primary_key=True)
    baraja_id1 = db.Column(db.Integer, db.ForeignKey('baraja1.id'))
    baraja_id2 = db.Column(db.Integer, db.ForeignKey('baraja2.id'))
    baraja_id3 = db.Column(db.Integer, db.ForeignKey('baraja3.id'))
    baraja_id4 = db.Column(db.Integer, db.ForeignKey('baraja4.id'))

class Baraja1(db.Model, UserMixin, Base):
    __tablename__ = 'baraja1'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    carta_id = db.Column(db.Integer, db.ForeignKey('carta.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    baraja_id = db.Column(db.Integer, db.ForeignKey('baraja.id'))

class Baraja2(db.Model, UserMixin, Base):
    __tablename__ = 'baraja2'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    carta_id = db.Column(db.Integer, db.ForeignKey('carta.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    baraja_id = db.Column(db.Integer, db.ForeignKey('baraja.id'))

class Baraja3(db.Model, UserMixin, Base):
    __tablename__ = 'baraja3'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    carta_id = db.Column(db.Integer, db.ForeignKey('carta.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    baraja_id = db.Column(db.Integer, db.ForeignKey('baraja.id'))

class Baraja4(db.Model, UserMixin, Base):
    __tablename__ = 'baraja4'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    carta_id = db.Column(db.Integer, db.ForeignKey('carta.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    baraja_id = db.Column(db.Integer, db.ForeignKey('baraja.id'))

class Carta(db.Model, UserMixin, Base):
    __tablename__ = 'carta'
    id = db.Column(db.Integer, primary_key=True)
    frente = db.Column(db.String(10000))
    detras = db.Column(db.String(10000))
    dificultad = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    baraja_id = db.Column(db.Integer, db.ForeignKey('baraja.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    baraja1 = db.relationship('Baraja1')
    baraja2 = db.relationship('Baraja2')
    baraja3 = db.relationship('Baraja3')
    baraja4 = db.relationship('Baraja4')

class Note(db.Model, UserMixin, Base):   #Logic for the notes in the website (it's main purpose)
    __tablename__ = 'note'   
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    #This user_id will be directly related to id integer attribute from the class User


class User(db.Model, UserMixin, Base):
    __tablename__ = 'user'   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)  # Unique = True hace que no sea posible que dos usuarios tengan el mismo correo
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    cartas = db.relationship('Carta')
    notes = db.relationship('Note')
    baraja1 = db.relationship('Baraja1')
    baraja2 = db.relationship('Baraja2')
    baraja3 = db.relationship('Baraja3')
    baraja4 = db.relationship('Baraja4')
    
