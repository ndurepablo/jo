import os

from dotenv import load_dotenv

from flask import Flask, render_template, g

import jinja2.exceptions

from flask_migrate import Migrate

from models.user import db, User

from app.auth.auth import auth_bp
from app.general.index import index_bp
from app.func.func import func_bp


from app.auth.service import get_user_data

from app.auth.auth import bcrypt
from app.auth.service import login_required

import click

load_dotenv()

app = Flask(__name__)

db_user = os.getenv('DB_USERNAME')
db_pass = os.getenv('DB_ROOT_PASSWORD')
db_host = os.getenv('DB_SERVICE')
db_name = os.getenv('DB_NAME')
# Conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'

# 'mysql+pymysql://usuario:contraseña@nombre_del_servicio_db/nombre_de_la_base_de_datos'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("create-user")
@click.option("--username", prompt="Enter username", help="Username for the superuser")
@click.option("--email", prompt="Enter email", help="Email for the superuser")
@click.option("--password", prompt="Enter password", hide_input=True, confirmation_prompt=True, help="Password for the superuser")
@click.option("--first-name", prompt="Enter first name", help="First name for the superuser")
@click.option("--last-name", prompt="Enter last name", help="Last name for the superuser")
@click.option("--is-admin", prompt="Is admin? (y/n)", type=click.BOOL, default=False, help="Is the user an admin?")
def createsuperuser(username, email, password, first_name, last_name, is_admin):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    """Create a superuser"""
    try:
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
        db.session.add(user)
        db.session.commit()
        click.echo("Superuser created successfully")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Failed to create superuser: {str(e)}")

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@login_required
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
@login_required
def not_found(e):
    return render_template('404.html')

# Decorador para cargar los datos del usuario antes de cada request
@app.before_request
def load_user_data():
    g.user = get_user_data()

app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)
app.register_blueprint(func_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)