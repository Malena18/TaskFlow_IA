import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_service import suggest_priority_with_gemini

# Usamos el decorador patch para reemplazar la clase GenerativeModel
@patch('app.services.ai_service.genai.GenerativeModel')
def test_suggest_priority_with_gemini_success(mock_model_class):
    """Prueba que el servicio retorna la prioridad correcta cuando la IA responde bien."""
    
    # 1. Configurar el Mock
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    # Simulamos el objeto respuesta que devuelve el SDK de Google
    mock_response = MagicMock()
    mock_response.text = "Alta"
    mock_model_instance.generate_content.return_value = mock_response
    
    # 2. Ejecutar la función bajo prueba
    # Nota: Aseguramos que exista una variable de entorno para que no entre en el if de error
    import os
    os.environ["GEMINI_API_KEY"] = "fake_key"
    
    priority = suggest_priority_with_gemini("Reparar servidor crítico")
    
    # 3. Validar los resultados
    assert priority == "Alta"
    mock_model_instance.generate_content.assert_called_once()

@patch('app.services.ai_service.genai.GenerativeModel')
def test_suggest_priority_with_gemini_fallback(mock_model_class):
    """Prueba que el servicio retorna 'Media' ante un error en la API."""
    
    # Simulamos que la API falla
    mock_model_class.return_value.generate_content.side_effect = Exception("API Error")
    
    import os
    os.environ["GEMINI_API_KEY"] = "fake_key"
    
    priority = suggest_priority_with_gemini("Cualquier tarea")
    
    assert priority == "Media"