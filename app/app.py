import streamlit as st
import re
from fpdf import FPDF
import tempfile
import pandas as pd
import os

from src.rag import rag_ask_openai
from src.embedding import load_embedding_model
from src.pinecone import get_or_create_index, get_pinecone_client
from src.openai import ask_openai
from src.utils.config import INDEX_NAME, POLICY_PRIORITIES, CANDIDATURA_DESCRIPTIONS
from src.namespace import DISPLAY_NAMES, get_namespace

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

@st.cache_resource
def get_resources():
    model = load_embedding_model()
    pinecone_client = get_pinecone_client()
    index = get_or_create_index(pinecone_client, INDEX_NAME)
    return model, index

model, index = get_resources()

st.title("Asistente Elección Judicial 2025")

st.markdown(f"""
            **Bienvenido al Asistente para la Elección Judicial 2025. 
            Aquí puedes consultar sobre los candidatos a jueces y fiscales, 
            y obtener recomendaciones basadas en tus prioridades o preguntas específicas.**
""")

display_namespace = st.selectbox(
    "Selecciona el tipo de candidatura para tu consulta:",
    DISPLAY_NAMES
)

desc = CANDIDATURA_DESCRIPTIONS.get(display_namespace, "No description available for this type.")
with st.expander("Ver descripción del rol de esta candidatura"):
    st.write(desc)

policy_priorities = st.multiselect(
    "Selecciona tus prioridades o valores para la justicia:",
    POLICY_PRIORITIES
)

st.markdown(f"**Y/O**")

if "history" not in st.session_state:
    st.session_state.history = []

namespace = get_namespace(display_namespace)
user_query = st.text_area("Haz tu pregunta sobre los candidatos:")

send_enabled = (len(policy_priorities) > 0) or (user_query.strip() != "")

if st.button("Enviar", disabled=not send_enabled):
    priorities_text = ""
    if policy_priorities:
        priorities_text = (
            "Mis prioridades o valores para la justicia son: " +
            ", ".join(policy_priorities) + ".\n"
        )
    full_prompt = f"{priorities_text}{user_query or ''}"
    with st.spinner("Buscando respuesta..."):
        answer = rag_ask_openai(full_prompt, index, model, namespace, ask_openai)
    st.session_state.history.append({
        "candidatura": display_namespace,  # <-- Add this line
        "prioridades": policy_priorities.copy(),
        "pregunta": user_query,
        "respuesta": answer
    })
    st.success("Respuesta guardada en el historial.")


def is_all_caps(name):
    # Consider a name as all caps if all letters are uppercase (ignore non-letters)
    letters = [c for c in name if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)

def extract_names_from_response(response):
    # Extract bolded text
    names = re.findall(r"\*\*(.*?)\*\*", response)
    filtered = []
    for n in names:
        n_clean = n.strip()
        if is_all_caps(n_clean):
            filtered.append(n_clean)
    return filtered


# --- Sidebar navigation for history and report ---
with st.sidebar:
    st.markdown("### Historial de Consultas")
    selected = None  # Ensure 'selected' is always defined
    if st.session_state.history:
        options = [
            f"Consulta #{i+1}" for i in range(len(st.session_state.history))
        ]
        selected = st.selectbox(
            "Selecciona una consulta para ver el detalle:",
            options[::-1],  # Most recent first
            key="history_select"
        )
        # Get the index of the selected response
        selected_idx = len(st.session_state.history) - 1 - options[::-1].index(selected)
    else:
        st.markdown("_Sin historial todavía._")
        selected_idx = None

    st.markdown("---")
    st.markdown("### Reporte Finales")
    if st.session_state.history:
        if st.button("Generar Reporte Candidatos (Solo Candidatos)", key="generate_report"):
            # Build the report dictionary
            report = {}
            for entry in st.session_state.history:
                candidatura = entry["candidatura"]
                # Extract names from the response (assuming you have extract_names_from_response)
                names = extract_names_from_response(entry["respuesta"])
                if candidatura not in report:
                    report[candidatura] = set()
                report[candidatura].update(names)
            # Convert sets to sorted lists for consistent output
            for candidatura in report:
                report[candidatura] = sorted(report[candidatura])

            # Group recommendations by candidatura type
            report_lines = ["# Reporte de candidaturas recomendadas\n"]
            for candidatura, names in report.items():
                report_lines.append(f"## {candidatura}")
                if names:
                    for name in names:
                        report_lines.append(f"- {name}")
                else:
                    report_lines.append("- (Sin nombres recomendados detectados)")
                report_lines.append("")  # Blank line

            # Add a summary section
            report_text = "\n".join(report_lines)
            st.markdown(report_text)
            
            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Reporte de candidaturas recomendadas", ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", size=12)
            for candidatura, names in report.items():
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, candidatura, ln=True)
                pdf.set_font("Arial", size=12)
                if names:
                    for name in names:
                        pdf.cell(10)  # Indent
                        pdf.cell(0, 10, f"- {name}", ln=True)
                else:
                    pdf.cell(10)
                    pdf.cell(0, 10, "- (Sin nombres recomendados detectados)", ln=True)
                pdf.ln(2)

            # Save PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile.seek(0)
                pdf_bytes = tmpfile.read()

            # Provide download button for the PDF
            st.download_button(
                label="Descargar Reporte en PDF",
                data=pdf_bytes,
                file_name="reporte_candidaturas.pdf",
                mime="application/pdf",
                key="download_report_pdf"
            )

        if st.button("Generar Reporte Detallado (Con Justificaciones)", key="download_full_report"):

            # Generate detailed report
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(0, 12, "Reporte Detallado de Consultas", ln=True, align="C")
            pdf.ln(6)

            for i, entry in enumerate(st.session_state.history, 1):
                # Section header
                pdf.set_font("Arial", "B", 13)
                pdf.set_text_color(0, 70, 140)
                pdf.cell(0, 10, f"Consulta #{i}", ln=True)
                pdf.set_draw_color(200, 200, 200)
                pdf.set_line_width(0.5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)

                # Content
                pdf.set_font("Arial", "", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 8, f"Candidatura: {entry.get('candidatura', 'No especificada')}")
                if entry["prioridades"]:
                    pdf.set_font("Arial", "I", 11)
                    pdf.multi_cell(0, 8, f"Prioridades: {', '.join(entry['prioridades'])}")
                if entry["pregunta"]:
                    pdf.set_font("Arial", "", 11)
                    pdf.multi_cell(0, 8, f"Pregunta: {entry['pregunta']}")
                pdf.set_font("Arial", "I", 11)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 8, f"Respuesta:\n{entry['respuesta']}")
                pdf.ln(4)

                # Separator between queries
                pdf.set_draw_color(180, 180, 180)
                pdf.set_line_width(0.2)
                y = pdf.get_y()
                pdf.line(10, y, 200, y)
                pdf.ln(4)

            # Save PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile.seek(0)
                pdf_bytes = tmpfile.read()

            # Provide download button for the PDF
            st.download_button(
                label="Descargar Reporte Detallado en PDF",
                data=pdf_bytes,
                file_name="reporte_detallado_candidaturas.pdf",
                mime="application/pdf",
                key="download_full_report_pdf"
            )
 
# --- Main area: show selected response as a "page" ---
if selected_idx is not None and st.session_state.history:
    item = st.session_state.history[selected_idx]
    st.markdown(f"## {selected}")
    st.markdown(f"**Candidatura:** {item.get('candidatura', 'No especificada')}")
    if item["prioridades"]:
        st.markdown(f"**Prioridades:** {', '.join(item['prioridades'])}")
    if item["pregunta"]:
        st.markdown(f"**Pregunta:** {item['pregunta']}")
    st.markdown(f"**Respuesta:** {item['respuesta']}")

# --- Footer with instructions ---
st.markdown("""
---
<sub>
Este sitio es una herramienta informativa desarrollada de manera independiente. 
No pertenece ni representa a ninguna autoridad electoral ni partido político.
Las recomendaciones se generan con base en coincidencias entre los valores proporcionados por la persona usuaria y la información pública disponible sobre las candidaturas.
La decisión final de voto es personal y este sitio no pretende sustituir el juicio propio ni influir de manera politica.
</sub>
""", unsafe_allow_html=True)