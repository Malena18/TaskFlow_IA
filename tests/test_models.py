from app.models import Task

def test_create_task(app):
    """Prueba que una tarea se puede crear y guardar en la base de datos."""
    with app.app_context():
        from app import db
        
        # Usamos los nombres definidos en tu models.py (title, description, etc.)
        new_task = Task(
            title="Probar arquitectura",
            description="Validar la integración con Pytest",
            priority="Alta",
            status="Pendiente"
        )
        db.session.add(new_task)
        db.session.commit()
        
        # Consultamos la tarea usando el campo 'title'
        task_in_db = Task.query.filter_by(title="Probar arquitectura").first()
        
        # Verificaciones
        assert task_in_db is not None
        assert task_in_db.title == "Probar arquitectura"
        assert task_in_db.priority == "Alta"
        assert task_in_db.status == "Pendiente"