#pylint: disable = missing-function-docstring ,cyclic-import ,missing-final-newline, missing-module-docstring, missing-function-docstring, line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

################
#### routes ####
################
from . import home_blueprint
@home_blueprint.route('/')
def get():
    return "Test"
