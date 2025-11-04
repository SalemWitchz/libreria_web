from flask import Flask
import os
from app.routes import main  # Importa el Blueprint principal

def create_app():
    # Obtiene la ruta base absoluta del proyecto
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Crea la aplicación Flask
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "libreria_web", "templates"),
        static_folder=os.path.join(base_dir, "libreria_web", "static")
    )

    # Clave secreta para sesiones y cookies seguras
    app.secret_key = "clave_super_secreta"

    # Registrar el Blueprint principal
    app.register_blueprint(main)

    return app


# ------------------------------
# Punto de entrada principal
# ------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
