"""
Módulo de inicialización de la aplicación Flask (Application Factory).
"""

from flask import Flask
from app.models import db
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def create_app():
    """
    Crea y configura la instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    # Configuración básica (idealmente en config.py, pero la definimos aquí para arrancar)
    app.config['SECRET_KEY'] = 'dev_secret_key_super_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones (vincula SQLAlchemy con nuestra app de Flask)
    db.init_app(app)

    # Importar y registrar los Blueprints (Rutas)
    # Importamos aquí dentro para evitar errores de dependencias circulares
    from app.routes.main_routes import main_bp
    from app.routes.task_routes import task_bp
    
    # Registramos las rutas en la aplicación
    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp)

    # Crear el archivo taskflow.db y las tablas si no existen
    with app.app_context():
        db.create_all()

    return app