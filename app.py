# pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from project import create_app, mongo

app = create_app('dev')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

if __name__ == "__main__":
    app.run(debug=True)
