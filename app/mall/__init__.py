from flask import Blueprint

mall = Blueprint('mall', __name__)

from . import views
