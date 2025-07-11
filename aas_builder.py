import json
def extract_environment_json(text: str) -> dict:
    """
    Intenta extraer un JSON válido desde un texto.
    Parte desde el primer '{' para ignorar encabezados no deseados.
    """
    cleaned = text.strip()

    # Eliminar cualquier texto antes del primer JSON
    start = cleaned.find("{")
    if start == -1:
        raise ValueError("No se encontró un objeto JSON en el texto.")

    cleaned = cleaned[start:].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"El texto no contiene un JSON válido: {e}")
