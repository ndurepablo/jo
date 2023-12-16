from flask import (
    session, redirect, url_for, request,
    render_template, flash, Blueprint
    )
from flask_bcrypt import Bcrypt

from models.user import User
from app.general.index import index_bp

bcrypt = Bcrypt()

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates',
    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('index_bp.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user = User.query.filter_by(username=username).first()

            if user and bcrypt.check_password_hash(user.password, password):
                session['logged_in'] = True
                session['username'] = username
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('auth_bp.login'))
            else:
                flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')
                print('Error, credenciales incorrect')
        except Exception as e:
            print(f"Error al iniciar sesión: {str(e)}")
            flash('Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo.', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    # Redirigir a la página de inicio de sesión o a cualquier otra página después del logout
    return redirect(url_for('auth_bp.login'))  # Reemplaza 'login' con la ruta correcta si es diferente