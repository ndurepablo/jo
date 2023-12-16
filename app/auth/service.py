
from functools import wraps
from flask import redirect, url_for, session, g

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

# Obtener los datos del usuario
def get_user_data():
    # Lógica para obtener los datos del usuario, desde la sesión o una base de datos
    if 'username' in session:
        return {'username': session['username']}
    return None