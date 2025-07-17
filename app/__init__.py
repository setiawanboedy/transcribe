import os
from flask import Flask
from app.db.database import db
from app.api.transcript_api import bp as transcript_bp
from app.api.stt_api import bp_stt
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcripts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Swagger(app, config={
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/apidocs/'
    })
    app.register_blueprint(transcript_bp)
    app.register_blueprint(bp_stt)
    return app
