def gerar_prompt_para_sumarizacao(texto):
    prompt_inicial = (
        "Atue como um sumarizador expert de assuntos médicos, "
        "tentando resumir em tópicos apenas os pontos importantes discutidos em um procedimento. "
        "Abaixo vou enviar a transcrição do procedimento (não adicione nenhum comentário conversacional comigo, "
        "apenas me entregue o resultado da sumarização, pois vou usá-lo desta forma no meu app).\n\n"
    )
    return prompt_inicial + texto
