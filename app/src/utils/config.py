from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = "ine-candidates"

NAMESPACE_OPTIONS = [
    "Magistraturas_de_Tribunales_Colegiados_de_Circuito_texts",
    "Juezas_es_de_Distrito_texts",
    "Magistratura_Salas_Regionales_del_TE_del_PJF_texts",
    "Ministra_o_Suprema_Corte_de_Justicia_de_la_Nacin_texts",
    "Magistratura_Tribunal_de_Disciplina_Judicial_texts",
    "Magistratura_Sala_Superior_del_TE_del_PJF_texts"
]

POLICY_PRIORITIES = [
    "Anticorrupción",
    "Combate a la impunidad",
    "Transparencia",
    "Acceso a la justicia",
    "Derechos humanos",
    "Perspectiva de género e igualdad",
    "Imparcialidad",
    "Justicia accesible",
    "Independencia judicial",
    "Profesionalismo y trayectoria" 
]

CANDIDATURA_DESCRIPTIONS = {
    "Magistraturas de Tribunales Colegiados de Circuito": "Resuelven apelaciones y asuntos importantes en materias como civil, penal o administrativa dentro de un circuito judicial. Son órganos colegiados que revisan decisiones de jueces de distrito.",
    "Juezas/es de Distrito": "Son jueces federales que atienden casos en primera instancia, como amparos, delitos federales, y asuntos civiles o administrativos contra autoridades federales.",
    "Magistratura Salas Regionales del TE del PJF": "Resuelven impugnaciones electorales a nivel regional, como conflictos en elecciones locales o decisiones de institutos electorales estatales. Son parte del Tribunal Electoral.",
    "Ministra/o Suprema Corte de Justicia de la Nación": "Integran el máximo tribunal del país. Deciden sobre la constitucionalidad de leyes, conflictos entre poderes y estados, y temas de gran importancia nacional.",
    "Magistratura Tribunal de Disciplina Judicial": "Evalúan y sancionan la conducta de jueces y magistrados del Poder Judicial. Aseguran que se mantenga la ética y profesionalismo en el sistema de justicia.",
    "Magistratura Sala Superior del TE del PJF": "Es la instancia máxima del Tribunal Electoral. Resuelve las impugnaciones más importantes, como la validez de elecciones federales, y establece criterios en materia electoral."
}
