from flask import Flask
from app.db import init_db
from app.routes import main  # o el nombre de tu blueprint principal

def create_app():
    app = Flask(
        __name__,
        template_folder="../libreria_web/templates",
        static_folder="../libreria_web/static"
    )

    app.secret_key = "cambia-esto-por-uno-seguro"
    
    # Registrar el Blueprint principal
    app.register_blueprint(main)
    
    # Inicializar la base de datos
    init_db(app)

    return app

