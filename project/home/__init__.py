"""
The recipes Blueprint handles the viewing of home for this application.
"""
#pylint: disable = line-too-long, wrong-import-position, missing-final-newline, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
from flask import Blueprint


home_blueprint = Blueprint('home', __name__, template_folder='templates')
from . import routes
