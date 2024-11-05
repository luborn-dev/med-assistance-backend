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
