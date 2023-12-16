from flask import (
    render_template, Blueprint
    )
from app.auth.service import login_required

index_bp = Blueprint(
    'index_bp', __name__,
    template_folder='templates',
    static_folder='static'
    )

@index_bp.route('/')
@index_bp.route('/index')
@login_required
def index():
    return render_template('index.html')
