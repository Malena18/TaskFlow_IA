"""
Rutas para las operaciones CRUD de las tareas.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Task
from datetime import datetime
from flask import jsonify

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/nueva', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Capturar los datos del formulario
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')
        
        # Procesar la fecha si el usuario la ingresó
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            
        # Crear la instancia de la tarea y guardarla en SQLite
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        # Redirigir al dashboard después de guardar
        return redirect(url_for('main.dashboard'))
        
    # Si es GET, mostrar el formulario
    return render_template('tasks/create.html')

# ... (código anterior de create_task) ...

@task_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    # Buscar la tarea por ID, si no existe devuelve un error 404
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status') # Importante: capturar el nuevo estado
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        else:
            task.due_date = None
            
        db.session.commit()
        return redirect(url_for('main.dashboard'))
        
    return render_template('tasks/edit.html', task=task)

@task_bp.route('/eliminar/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@task_bp.route('/api/suggest-priority', methods=['POST'])
def api_suggest_priority():
    """
    Endpoint asíncrono para sugerir la prioridad vía IA.
    """
    data = request.get_json()
    description = data.get('description', '')
    
    # Importación local para evitar dependencias circulares
    from app.services.ai_service import suggest_priority_with_gemini
    
    suggested = suggest_priority_with_gemini(description)
    
    return jsonify({'priority': suggested})

@task_bp.route('/api/generate-description', methods=['POST'])
def api_generate_description():
    """
    Endpoint asíncrono para generar la descripción vía IA.
    """
    data = request.get_json()
    title = data.get('title', '')
    
    from app.services.ai_service import generate_task_description
    generated_desc = generate_task_description(title)
    
    return jsonify({'description': generated_desc})