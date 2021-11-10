#Aqui se definen y se guardan las rutas estandar de la pagina (a donde los usuarios pueden ir)
import os
import sqlite3 as sql
import datetime
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import desc
from walj_study import db
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .__init__ import *
from flask import Blueprint, render_template, request, flash, redirect, current_app # Estos importes permiten tener este archivo como un plano para la pagina (Blueprint), a renderizar las vistas html
from flask.helpers import url_for                                                   # a pedir informacion (request) y mostrar mensajes en la pantalla (flash)
from flask_login import login_required, current_user    # El metodo de current_user detectara si el usuario se encuentra logeado o no

views = Blueprint('views', __name__)    #Asi es como se definira el "plano" (Blueprint)
basedir = os.path.abspath(os.path.dirname(__file__))
""" engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)()

Base = declarative_base() """



# Desde aqui empiezan las limitaciones a vistas del usuario.
# Es necesario que el usuario se encuentre logeado para poder entrar
# a estas URL's de la pagina

@views.route('/', methods=['GET', 'POST'])
@login_required
def barajas():  
    return render_template("barajas.html", user=current_user)


@views.route('/estadisticas', methods=['GET', 'POST'])
@login_required
def estadisticas():  
    return render_template("estadisticas.html", user=current_user)

@views.route('/tutorial', methods=['GET', 'POST'])
@login_required
def tutorial():  
    return render_template("tutorial.html", user=current_user)

@views.route('/pagina_repaso', methods=['GET', 'POST'])
@login_required
def pagina_repaso():  
    return render_template("pagina_repaso.html", user=current_user)

@views.route('/crear_carta', methods=['GET', 'POST'])
@login_required
def crear_carta():  
    return render_template("crear_cartas.html", user=current_user)

"""
@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        user_id = request.cookies.get("user_id")
        photo_user_name = request.cookies.get("photo_user_name")
        post_title = request.form['title']
        post_date = datetime.datetime.now()
        upload_image = request.files['upload_image']   
        if upload_image.filename != '':
            filepath = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], upload_image.filename)
            upload_image.save(filepath)
        new_post = Post(photo=upload_image.filename, foot_note=post_title, post_date=post_date, user_id=user_id, photo_user_name=photo_user_name)   
        db.session.add(new_post)
        db.session.commit()
        flash('Publicacion exitosa!', category='succes')
        return redirect(url_for('views.feed'))

    return render_template("crear_post.html", user=current_user)
"""


