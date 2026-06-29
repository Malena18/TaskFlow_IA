"""
Servicios de integración con Inteligencia Artificial.
"""
import os
import google.generativeai as genai

def suggest_priority_with_gemini(description):
    """
    Evalúa una descripción y devuelve una prioridad (Baja, Media, Alta).
    """
    if not description or len(description.strip()) < 5:
        return "Media"  # Fallback si no hay contexto suficiente

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Advertencia: No se encontró GEMINI_API_KEY.")
        return "Media"

    genai.configure(api_key=api_key)
    # gemini-1.5-flash es ideal porque es extremadamente rápido para texto
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Actúa como un gestor de proyectos experto. 
    Analiza la siguiente descripción de una tarea y determina su nivel de prioridad.
    Debes responder ÚNICAMENTE con una de estas tres palabras: Baja, Media o Alta.
    No añadas explicaciones, puntos, ni texto adicional.
    
    Descripción de la tarea: "{description}"
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text.strip().capitalize()
        
        # Validación de seguridad
        if result in ["Baja", "Media", "Alta"]:
            return result
        return "Media"
        
    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return "Media"
    
def generate_task_description(title):
    """
    Genera una descripción detallada y profesional a partir del título de la tarea.
    """
    if not title or len(title.strip()) < 3:
        return ""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Configura tu API KEY para generar descripciones."

    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Actúa como un asistente de productividad experto. 
    He escrito el siguiente título para una tarea: "{title}"
    
    Escribe una descripción breve, clara y profesional (máximo 3 o 4 líneas) detallando los pasos lógicos, el contexto o el objetivo esperado para completar esta tarea. 
    No incluyas saludos ni frases introductorias, responde directamente con la descripción.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return "Hubo un problema al generar la descripción con IA."