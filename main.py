import os

from dotenv import load_dotenv

from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import jinja2.exceptions

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from app.utils.service import get_category, get_details, get_orders, get_tickets

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    # Redirigir a la página de inicio de sesión o a cualquier otra página después del logout
    return redirect(url_for('login'))  # Reemplaza 'login' con la ruta correcta si es diferente

# Obtener los datos del usuario
def get_user_data():
    # Lógica para obtener los datos del usuario, desde la sesión o una base de datos
    if 'username' in session:
        return {'username': session['username']}
    return None

# Decorador para cargar los datos del usuario antes de cada request
@app.before_request
def load_user_data():
    g.user = get_user_data()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/<pagename>')
@login_required
def admin(pagename):
    return render_template(pagename+'.html')

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@login_required
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
@login_required
def not_found(e):
    return render_template('404.html')

def check_submit_button(submit_button):
    return submit_button.lower() == 'buscar'

@app.route('/orders/', methods=['GET', 'POST'])
@login_required
def orders_completed():

    page = int(request.args.get("page", 1))
    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button and check_submit_button(submit_button):
        if after:
            orders, total_pages = get_orders(date_type='delivery', after=after)

    return render_template('orders.html', orders = orders, total_pages = total_pages, page = page)


@app.route('/tickets/', methods=['GET', 'POST'])
@login_required
def tickets_delivery():

    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button and check_submit_button(submit_button):
        if after:
            orders, total_pages = get_details(date_type='delivery', after=after)

    return render_template('tickets.html', orders=orders, total_pages=total_pages)

@app.route('/details/')
@login_required
def orders_details():

    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button and check_submit_button(submit_button):
        if after:
            orders, total_pages = get_details(date_type='delivery', after=after)

    return render_template('details.html', orders=orders)

@app.route('/category/')
@login_required
def category():
    category = request.args.get('category')
    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button and check_submit_button(submit_button):
        if after:
            orders, total_pages = get_category(date_type='period', after=after, before=before, category=category)
    # Procesa los datos para la tabla
    table_data = []
    headers = set() # Usaremos un conjunto para recopilar todos los nombres de usuario únicos
    if orders:
            for order in orders:
                product_name = order['name']
                total_quantity = order['total_quantity']
                user_data = order['users']

                # Agrega los nombres de usuario a los encabezados
                headers.update(user_data.keys())

                # Creamos una fila para la tabla con los valores que necesitas
                row = {
                    'product_name': product_name,
                    'total_quantity': total_quantity,
                    **user_data  # Desempaqueta todos los usuarios y sus cantidades
                }
                table_data.append(row)

            # Convierte los encabezados a una lista para ordenarlos
            headers = sorted(list(headers))


    return render_template('category.html', table_data=table_data, headers=headers)

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=False)