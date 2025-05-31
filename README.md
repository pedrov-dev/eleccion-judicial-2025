# Asistente de Elección Judicial 2025

Asistente de Elección Judicial 2025 es una aplicación interactiva desarrollada en Streamlit que ayuda a la ciudadanía mexicana a tomar decisiones informadas sobre candidaturas judiciales. Utiliza técnicas de RAG (Retrieval-Augmented Generation), modelos de lenguaje y búsqueda semántica para responder preguntas, recomendar candidatas/os según valores y prioridades seleccionados, y generar reportes personalizados de recomendaciones.

### Características
Consulta personalizada: Selecciona el tipo de candidatura y tus prioridades o valores para la justicia.
Preguntas libres: Haz preguntas abiertas sobre los candidatos.
Respuestas inteligentes: El asistente utiliza IA para analizar perfiles y responder de manera imparcial y fundamentada.
Historial de consultas: Guarda y navega tus consultas y respuestas anteriores desde la barra lateral.
Reporte final: Genera y descarga un reporte en PDF con los nombres recomendados agrupados por tipo de candidatura.
Interfaz intuitiva: Todo en una sola página, fácil de usar y navegar.

### ¿Cómo funciona?
Selecciona el tipo de candidatura judicial.
Elige tus prioridades o valores (anticorrupción, igualdad de género, derechos humanos, etc.).
(Opcional) Escribe una pregunta libre sobre los candidatos.
Haz clic en Enviar para recibir recomendaciones y justificaciones.
Consulta tu historial y genera un reporte final en PDF desde la barra lateral.

### Estructura del proyecto
app/
│
├── app.py                  # Aplicación principal de Streamlit
├── src/
│   ├── rag.py
│   ├── embedding.py
│   ├── pinecone.py
│   ├── openai.py
│   ├── namespace.py
│   └── utils/
│       └── config.py

### Licencia
MIT
