"""
Definición de los modelos de base de datos para TaskFlow IA.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pendiente')   # Pendiente, En Progreso, Completada
    priority = db.Column(db.String(15), default='Media')     # Baja, Media, Alta
    due_date = db.Column(db.DateTime, nullable=True)         # Fecha límite para el cálculo de vencimiento
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id} - {self.title}>'