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
    "Igualdad de género",
    "Derechos humanos",
    "Acceso a la justicia",
    "Transparencia",
    "Imparcialidad",
    "Justicia cercana",
    "Modernización tecnológica",
    "Perspectiva de género",
    "Combate a la impunidad"
]
