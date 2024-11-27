def gerar_prompt_para_sumarizacao(texto, contexto: str = "procedimentos médicos"):
    """
    Gera um prompt estruturado para sumarização de transcrições médicas.

    Parâmetros:
    - texto (str): A transcrição do procedimento a ser sumarizada.
    - contexto (str): O contexto de atuação da IA (ex.: "procedimentos médicos").

    Retorna:
    - str: O prompt formatado para sumarização.
    """
    if not texto:
        raise ValueError("O texto de entrada não pode estar vazio.")

    prompt_inicial = (
        f"Atue como um sumarizador especializado em {contexto}. "
        "Abaixo está a transcrição de um procedimento médico. Sua tarefa é gerar um resumo estruturado, "
        "organizando as informações nas seções especificadas. Não inclua nenhum tipo de interação, comentário, "
        "ou perguntas direcionadas ao usuário. Apenas forneça o resumo formatado conforme solicitado.\n\n"
        "Estruture o resumo nas seguintes seções:\n\n"
        "- **Sintomas e Queixas**: Descreva os principais sintomas relatados pelo paciente.\n"
        "- **Histórico Médico**: Inclua detalhes relevantes sobre o histórico médico e condições crônicas.\n"
        "- **Diagnóstico**: Resuma qualquer diagnóstico discutido durante o procedimento.\n"
        "- **Tratamento e Procedimentos**: Descreva os tratamentos ou procedimentos realizados.\n"
        "- **Recomendações**: Liste as principais recomendações e próximos passos sugeridos.\n\n"
        "Abaixo está a transcrição completa do procedimento médico:\n\n"
    )
    return prompt_inicial + texto


def gerar_prompt_para_historico_medico(texto, contexto: str = "procedimentos médicos"):
    prompt_inicial = (
        f"Atue como um sumarizador especializado em {contexto} com foco em análise abrangente de múltiplos procedimentos médicos. "
        "Abaixo está a transcrição de diversas consultas e procedimentos realizados. Sua tarefa é gerar um resumo estruturado, "
        "integrando informações recorrentes e destacando padrões importantes. Não inclua nenhum tipo de interação, comentário, "
        "ou perguntas direcionadas ao usuário. Apenas forneça o resumo formatado conforme solicitado.\n\n"
        "Estruture o resumo nas seguintes seções:\n\n"
        "- **Sintomas e Queixas Repetidas**: Destaque os sintomas e queixas mais frequentemente relatados.\n"
        "- **Histórico Médico Agregado**: Resuma o histórico médico e as condições crônicas mencionadas ao longo das consultas.\n"
        "- **Diagnósticos Frequentes**: Liste e descreva os diagnósticos mais comuns e recorrentes entre as transcrições.\n"
        "- **Tratamentos e Procedimentos Mais Utilizados**: Resuma os principais tratamentos e procedimentos realizados com mais frequência.\n"
        "- **Recomendações e Acompanhamentos**: Inclua as recomendações gerais, os acompanhamentos sugeridos, e próximos passos comuns.\n\n"
        "Abaixo estão as transcrições completas de múltiplos procedimentos médicos:\n\n"
    )

    return prompt_inicial + texto
