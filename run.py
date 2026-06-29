"""
Punto de entrada principal para ejecutar TaskFlow IA.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie solo al guardar cambios
    app.run(debug=True)