from flask import Blueprint, render_template, request
from app.models import Task
from datetime import datetime, timezone

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    now = datetime.now(timezone.utc)
    
    # 1. Métricas Globales (Estas tarjetas siempre mostrarán el estado total de tu proyecto)
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='Pendiente').count()
    completed_tasks = Task.query.filter_by(status='Completada').count()
    overdue_tasks = Task.query.filter(
        Task.status != 'Completada',
        Task.due_date < now
    ).count()
    
    # 2. Capturar los parámetros de búsqueda de la URL
    search_query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    # 3. Construir la consulta dinámica para la lista de tareas
    query = Task.query
    
    if search_query:
        # Busca tanto en el título como en la descripción ignorando mayúsculas/minúsculas
        query = query.filter(
            (Task.title.ilike(f'%{search_query}%')) | 
            (Task.description.ilike(f'%{search_query}%'))
        )
        
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
        
    # Ejecutar la consulta ordenando de la más nueva a la más antigua
    filtered_tasks = query.order_by(Task.created_at.desc()).all()
    
    return render_template(
        'dashboard.html',
        total=total_tasks,
        pending=pending_tasks,
        completed=completed_tasks,
        overdue=overdue_tasks,
        recent_tasks=filtered_tasks,
        # Pasamos las variables actuales a la plantilla para que el formulario no se borre al recargar
        current_q=search_query,
        current_status=status_filter,
        current_priority=priority_filter
    )