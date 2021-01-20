"""
The recipes Blueprint handles the creation, modification, deletion,
and viewing of profile for this application.
"""
#pylint: disable = line-too-long, wrong-import-position, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

from flask import Blueprint

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')
from . import routes
