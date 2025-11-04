import mysql.connector
from flask import g
import hashlib

DB_CONFIG = {
    "host": "yamabiko.proxy.rlwy.net",
    "user": "root",
    "password": "xoimbwPTbaEajNJsWeQCxpYUOUKdLYmY",  # contraseña de Railway
    "database": "prueba",  # 👈 tu base de datos real
    "port": 19478
}

def get_db():
    """Devuelve la conexión activa o crea una nueva."""
    if "db" not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    """Cierra la conexión."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def hash_password(password):
    """Cifra contraseñas con SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db(app):
    """Configura la base de datos al iniciar Flask"""
    app.teardown_appcontext(close_db)

