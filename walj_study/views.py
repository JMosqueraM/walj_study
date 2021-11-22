#Aqui se definen y se guardan las rutas estandar de la pagina (a donde los usuarios pueden ir)
import os
import json
import sqlite3 as sql
import datetime
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.sqltypes import JSON
from walj_study import db
from sqlalchemy import create_engine, update
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .__init__ import *
from flask import Blueprint, render_template, request, flash, redirect, jsonify, current_app # Estos importes permiten tener este archivo como un plano para la pagina (Blueprint), a renderizar las vistas html
from flask.helpers import make_response, url_for                                                   # a pedir informacion (request) y mostrar mensajes en la pantalla (flash)
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
    if request.method == 'POST':
        id_baraja_fijo = request.form.get("cargar_baraja")
        id_baraja = request.form.get("cargar_baraja")
        print(id_baraja)
        if id_baraja:
            id_baraja = int(id_baraja)
            response = make_response(render_template("barajas.html", user=current_user))
            response.set_cookie("baraja",
                    f"{id_baraja}",
                    secure=True)
            response.set_cookie("contador",
                    f"{0}",
                    secure=True)
            print(int(request.cookies.get("baraja")))
            redirect(url_for('views.barajas'))
            return response
        else:
            frente = request.form.get('frente')
            detras = request.form.get('detras')
            baraja = request.form.get('valor_boton')
            baraja_estudio = request.form.get('valor_boton_estudio')
            print(baraja_estudio)

            if (len(frente) or len(detras)) < 1:
                flash('La informacion en una carta es muy corta!', category='error')
            else:
                nueva_carta = Carta(frente=frente, detras=detras, dificultad=0, baraja_id=baraja, user_id=current_user.id)
                db.session.add(nueva_carta)
                db.session.commit()
                flash('Carta agregada exitosamente!', category='success')

            info_cartas = db.engine.execute(
                            """
                        SELECT frente, detras
                        FROM carta
                        ORDER
                        BY id DESC
                            """
                    )



        return render_template("barajas.html", user=current_user)
    if request.method == "GET":
        id_baraja = int(request.cookies.get("baraja"))
        print(id_baraja)
        print("pepesabe")
        numero = request.form.get('cargar_baraja')
        print(numero)



        """ response = make_response(render_template("barajas.html", user=current_user))
        response.set_cookie("baraja",
                    f"{id_baraja}",
                    secure=True) 
        response.set_cookie("contador",
                    f"{0}",
                    secure=True) """

    return render_template("barajas.html", user=current_user)

@views.route('/notas', methods=['GET', 'POST'])
@login_required
def notas():    #This function will run whenever you go to '/URL'
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('La nota es demasiado corta!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota agregada!', category='success')
        return render_template("home.html", user=current_user)

    if request.method == 'GET':
        result = db.engine.execute(
                """
            SELECT frente, detras
            FROM carta
            ORDER
            BY id DESC
                """
        )
        return render_template("home.html", posts=result, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

@views.route('/delete-carta', methods=['POST'])
def delete_carta():
    carta = json.loads(request.data)
    cartaId = carta['cartaId']
    print(cartaId)
    carta = Carta.query.get(cartaId)
    print(carta)
    if carta:
        if carta.user_id == current_user.id:
            db.session.delete(carta)
            db.session.commit()
            
    return jsonify({})

@views.route('/cambiar-dificultad', methods=['POST'])
def cambiar_dificultad():
        muy_dificil = request.form.get('muy_dificil')
        dificil = request.form.get('dificil')
        facil = request.form.get('facil')
        muy_facil = request.form.get('muy_facil')
        baraja = request.cookies.get("baraja")

        if muy_dificil:
            carta = json.loads(request.data)
            cartaBaraja_id = carta['cartaBaraja_id']
            carta = Carta.query.get(cartaBaraja_id)
            if carta:
                if carta.baraja_id == baraja:
                    db.session.delete(carta.dificultad)
                    db.session.commit()
                    db.session.add(int(muy_dificil))
                    db.session.commit()


        if dificil:
            carta = json.loads(request.data)
            cartaBaraja_id = carta['cartaBaraja_id']
            carta = Carta.query.get(cartaBaraja_id)
            if carta:
                if carta.baraja_id == baraja:
                    db.session.delete(carta.dificultad)
                    db.session.commit()
                    db.session.add(int(dificil))
                    db.session.commit()

        if facil:
            carta = json.loads(request.data)
            cartaBaraja_id = carta['cartaBaraja_id']
            carta = Carta.query.get(cartaBaraja_id)
            if carta:
                if carta.baraja_id == baraja:
                    db.session.delete(carta.dificultad)
                    db.session.commit()
                    db.session.add(int(facil))
                    db.session.commit()

        if muy_facil:
            carta = json.loads(request.data)
            cartaBaraja_id = carta['cartaBaraja_id']
            carta = Carta.query.get(cartaBaraja_id)
            if carta:
                if carta.baraja_id == baraja:
                    db.session.delete(carta.dificultad)
                    db.session.commit()
                    db.session.add(int(muy_facil))
                    db.session.commit()


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
    if request.method == 'POST':
        redirect(url_for('views.pagina_repaso'))



        lista_frente = []
        lista_detras = []
        lista_dificultades = []
        lista_cartas = []
        info_carta = []
        cartas = db.engine.execute(
                """
            SELECT *
            FROM carta
            ORDER BY
                carta.dificultad
                """
        )

        baraja = request.cookies.get("baraja")

        # print(baraja)
        cartas_copia = cartas

        print(baraja)
        print("andale23")
        for carta in cartas_copia:
            print(f"baraja: {baraja}")
            if carta.baraja_id == int(baraja):
                print(f"carta baraja ID: {carta.baraja_id}")
                lista_dificultades.append(carta.dificultad)
                lista_frente.append(carta.frente)
                lista_detras.append(carta.detras)


                info_carta.append(carta.user_id)
                info_carta.append(carta.dificultad)
                info_carta.append(carta.detras)
                info_carta.append(carta.frente)
                lista_temp = info_carta.copy()
                lista_cartas.append(list(lista_temp))
                info_carta.clear()
                lista_temp.clear()


        print(info_carta)
        print(f"La lista de cartas es: {lista_cartas}")
        print(f"La lista de frente es: {lista_frente}")
        print(f"La lista de detras es: {lista_detras}")
        print(f"La lista de dificultades es: {lista_dificultades}")
       

        print("pepe post")
        contador = int(request.cookies.get("contador"))
        print(f"El contador es {contador}")
        response = make_response(render_template("pagina_repaso.html", carta=carta, user=current_user, baraja=int(baraja), lista_cartas=list(lista_cartas), contador=int(contador), lista_frente=list(lista_frente), lista_detras=list(lista_detras), lista_dificultades=list(lista_dificultades)))
        response.set_cookie("contador",
                    f"{contador + 1}",
                    secure=True)


    
        return response
    if request.method == 'GET': 
        redirect(url_for('views.pagina_repaso'))



        lista_frente = []
        lista_detras = []
        lista_dificultades = []
        lista_cartas = []
        info_carta = []
        cartas = db.engine.execute(
                """
            SELECT *
            FROM carta
            ORDER BY
                carta.dificultad
                """
        )

        baraja = request.cookies.get("baraja")

        # print(baraja)
        cartas_copia = cartas

        print(baraja)
        print("andale23")
        for carta in cartas_copia:
            print(f"baraja: {baraja}")
            if carta.baraja_id == int(baraja):
                print(f"carta baraja ID: {carta.baraja_id}")
                lista_dificultades.append(carta.dificultad)
                lista_frente.append(carta.frente)
                lista_detras.append(carta.detras)


                info_carta.append(carta.user_id)
                info_carta.append(carta.dificultad)
                info_carta.append(carta.detras)
                info_carta.append(carta.frente)
                lista_temp = info_carta.copy()
                lista_cartas.append(list(lista_temp))
                info_carta.clear()
                lista_temp.clear()


        print(info_carta)
        print(f"La lista de cartas es: {lista_cartas}")
        print(f"La lista de frente es: {lista_frente}")
        print(f"La lista de detras es: {lista_detras}")
        print(f"La lista de dificultades es: {lista_dificultades}")
       

        print("pepe post")
        contador = int(request.cookies.get("contador"))
        print(f"El contador es {contador}")
        response = make_response(render_template("pagina_repaso.html", carta=carta, user=current_user, baraja=int(baraja), lista_cartas=list(lista_cartas), contador=int(contador), lista_frente=list(lista_frente), lista_detras=list(lista_detras), lista_dificultades=list(lista_dificultades)))
        response.set_cookie("contador",
                    f"{contador + 1}",
                    secure=True)


    
        return response



