NAMESPACE_MAP = {
    "Magistraturas de Tribunales Colegiados de Circuito": "Magistraturas_de_Tribunales_Colegiados_de_Circuito_texts",
    "Juezas/es de Distrito": "Juezas_es_de_Distrito_texts",
    "Magistratura Salas Regionales del TE del PJF": "Magistratura_Salas_Regionales_del_TE_del_PJF_texts",
    "Ministra/o Suprema Corte de Justicia de la Nación": "Ministra_o_Suprema_Corte_de_Justicia_de_la_Nacin_texts",
    "Magistratura Tribunal de Disciplina Judicial": "Magistratura_Tribunal_de_Disciplina_Judicial_texts",
    "Magistratura Sala Superior del TE del PJF": "Magistratura_Sala_Superior_del_TE_del_PJF_texts"
}

DISPLAY_NAMES = list(NAMESPACE_MAP.keys())

def get_namespace(display_name):
    return NAMESPACE_MAP[display_name]