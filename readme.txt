Notas de instalación

1. Dependencias y requisitos de instalación

VisualStudio Code
Python 3.11.9
pip 25.1.1


2.	Crear y activar un entorno virtual
python -m venv .venv 
.\.venv\Scripts\activate        # Windows

3.	Dependencias
 Archivos que la aplicación necesita para funcionar correctamente:
app.timestamp.py – punto de entrada Streamlit, orquesta todos los pasos de la app app.timestamp
llm_client.py – funciones interpret_structure y generate_aas para interactuar con el LLM app.timestamp
llm_examples.py – define los few-shot examples usados por llm_client.py llm_examples
aas_builder.py – extract_environment_json para parsear el JSON generado app.timestamp
validator.py – validate_environment que aplica el esquema JSON de AAS validator
summary.py – summarize_environment para generar el texto resumen del AAS app.timestamp
utils.py – sanitize_aas_json y normalize_booleans para limpiar el JSON app.timestamp
fix_degree_symbols.py – corrige símbolos de grado mal codificados en qualifiers fix_degree_symbols
basyx_exporter.py – export_aasx_from_json para generar el paquete AASX via Eclipse BaSyx SDK basyx_exporter
requirements.txt – lista de dependencias:

streamlit
requests
jsonschema
basyx-python-sdk==1.2.1


Para instalar dependencias:

(ya debe haberse ejecutado python -m venv .venv 
.\.venv\Scripts\activate        # Windows)

pip install --upgrade pip (python.exe -m pip install --upgrade pip)
pip install -r requirements.txt



4.	Backend de LLM local
Descargar modelo meta-llama-3.1-8b-instruct. (dede Hugging face)
LM Studio (llm_client) 
POST a http://localhost:1234/v1/chat/completions, se debe tener corriendo el servidor LLM en ese puerto.

5.	Arranque de la aplicación
streamlit run app.timestamp.py



