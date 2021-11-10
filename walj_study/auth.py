from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from werkzeug.wrappers import response
from .__init__ import *
from werkzeug.security import generate_password_hash, check_password_hash
from walj_study import db    
from flask_login import login_user, login_required, logout_user, current_user       
import sqlite3 as sql
from datetime import timezone

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('correo')
        password = request.form.get('Contraseña')
        checkid = request.form.get('checkid')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Logueado exitosamente como {user.user_name}', category='success')
                if checkid:
                    login_user(user, remember=True)
                    redirect(url_for('views.barajas'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             


                    response = make_response(render_template("feed.html", user=current_user))                   
                    response.set_cookie("user_id",
                                        f"{user.id}",
                                        secure=True)
                    response.set_cookie("photo_user_name",
                                        f"{user.user_name}",
                                        secure=True)
                    return response
                else:
                    login_user(user, remember = False)
                    redirect(url_for('views.barajas'))


                    response = make_response(render_template("barajas.html", user=current_user))
                    redirect(url_for('views.barajas'))
                    response.set_cookie("user_id",
                                        f"{user.id}",
                                        secure=True)
                    response.set_cookie("photo_user_name",
                                        f"{user.user_name}",
                                        secure=True)
                    return response
            else:
                flash('Contraseña incorrecta, intentelo de nuevo.', category='error')
                return render_template("login.html", user=current_user)
        else:
            flash('El correo electronico no exite', category='error')
        return render_template("login.html", user=current_user)

    return render_template("login.html", user=current_user) #Depending on the status of the current_user (signed in or not), the login button is displayed

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ha salido de su cuenta exitosamente!")
    return redirect(url_for('auth.login'))

@auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == 'POST':
        name = request.form['nombre']
        email = request.form['correo']
        password = request.form['Contraseña']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('El correo ya existe', category='error')

        elif len(name) < 2:
            flash('Su nombre debe tener al menos dos letras.', category='error')
            pass
        elif len(email) < 4:
            flash('Su correo debe ser mayor a 4 caracteres.', category='error')
            pass
        elif len(password) < 7:
            flash('Debe tener almenos 18 años', category='error')
            pass
        else:   # add user to the database 
            new_user = User(email=email, user_name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso!', category='succes')
            return redirect(url_for('auth.login'))
            
    return render_template("registro.html", user=current_user)   #Depending on the status of the current_user (signed in or not), the sign up button is displayed
    




