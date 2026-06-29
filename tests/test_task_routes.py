import pytest
from app.models import Task

def test_create_task_route(client):
    """Prueba la integración: enviar un formulario y verificar que se guarde en la BD."""
    
    # 1. Datos simulados del formulario
    data = {
        'title': 'Test de Integración',
        'description': 'Probando el endpoint de creación',
        'priority': 'Alta',
        'due_date': '2026-07-01 10:00'
    }
    
    # 2. Realizar petición POST al endpoint definido en task_routes.py
    # Usamos follow_redirects=True para ver el resultado final después del redirect
    response = client.post('/tasks/nueva', data=data, follow_redirects=True)
    
    # 3. Validaciones
    assert response.status_code == 200 # Aseguramos que la página cargó (redirigió al dashboard)
    
    # Verificamos que realmente existe en la base de datos
    with client.application.app_context():
        task = Task.query.filter_by(title='Test de Integración').first()
        assert task is not None
        assert task.priority == 'Alta'