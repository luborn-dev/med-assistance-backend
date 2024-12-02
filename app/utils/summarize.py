import logging
import os
import re

from fastapi import HTTPException
from google.generativeai import GenerativeModel, configure

from app.utils.pre_processing_summarize import (
    gerar_prompt_para_historico_medico,
    gerar_prompt_para_sumarizacao,
)

logger = logging.getLogger(__name__)

configure(api_key=os.environ.get("API_KEY"))


async def summarize_transcription(text: str, option: str) -> dict:
    """
    Resumo de transcrições médicas estruturado em um objeto com campos específicos.

    Parâmetros:
    - text (str): Texto da transcrição a ser sumarizado.

    Retorna:
    - dict: Objeto contendo o resumo estruturado.
    """
    try:
        full_text = "\n".join(text)
        if not full_text.strip():
            logger.warning("Empty or whitespace-only text received for summarization.")
            raise ValueError("The input text for summarization cannot be empty.")

        # Gerar o prompt estruturado
        if option == "medical_history":
            prompt = gerar_prompt_para_historico_medico(full_text)
        elif option == "medical_procedure":
            prompt = gerar_prompt_para_sumarizacao(full_text)
        else:
            logger.error(f"Invalid or missing option for summarization: {option}")
            raise ValueError("Invalid or missing option for summarization.")

        # Inicializar o modelo generativo
        model = GenerativeModel("gemini-1.5-flash")
        logger.info("Initialized generative model.")

        # Obter a resposta do modelo
        response = model.generate_content(prompt)
        if not response or not hasattr(response, "text"):
            logger.error("No valid response received from generative model.")
            raise ValueError(
                "Failed to retrieve a valid response from the generative model."
            )

        logger.info("Summarization successful.")

        # Processar a resposta do modelo para criar o objeto estruturado
        if option == "medical_history":
            structured_output = parse_generated_summary(response.text)
        elif option == "medical_procedure":
            structured_output = parse_procedure_summary(response.text)

        return structured_output

    except ValueError as ve:
        logger.error(f"Validation error in summarization service: {ve}")
        raise HTTPException(
            status_code=400, detail=f"Invalid input for summarization: {str(ve)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error in summarization service: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the summarization request.",
        )


def parse_generated_summary(summary_text: str) -> dict:
    """
    Processa o texto gerado pelo modelo para criar um objeto JSON estruturado usando regex.

    Parâmetros:
    - summary_text (str): Resumo gerado pelo modelo.

    Retorna:
    - dict: Objeto JSON estruturado com os campos em padrão REST API.
    """
    sections = {
        "repeated_symptoms_and_complaints": "",
        "aggregated_medical_history": "",
        "frequent_diagnoses": "",
        "most_used_treatments_and_procedures": "",
        "recommendations_and_follow_ups": "",
    }

    # Regex para capturar cada seção e seu conteúdo
    pattern = re.compile(r"\*\*(.+?)\*\*:([\s\S]*?)(?=\*\*|$)")

    # Mapeamento entre os nomes em inglês e os títulos originais
    title_mapping = {
        "Sintomas e Queixas Repetidas": "repeated_symptoms_and_complaints",
        "Histórico Médico Agregado": "aggregated_medical_history",
        "Diagnósticos Frequentes": "frequent_diagnoses",
        "Tratamentos e Procedimentos Mais Utilizados": "most_used_treatments_and_procedures",
        "Recomendações e Acompanhamentos": "recommendations_and_follow_ups",
    }

    # Iterar pelas correspondências e preencher o dicionário
    matches = pattern.findall(summary_text)
    for match in matches:
        section_title = match[0].strip()
        section_content = match[1].strip()
        # Mapear o título ao campo correspondente no dicionário, se existir
        if section_title in title_mapping:
            rest_api_key = title_mapping[section_title]
            sections[rest_api_key] = section_content

    return sections


def parse_procedure_summary(summary_text: str) -> dict:
    """
    Processa o texto gerado pelo modelo para criar um objeto JSON estruturado usando regex.

    Parâmetros:
    - summary_text (str): Resumo gerado pelo modelo.

    Retorna:
    - dict: Objeto JSON estruturado com os campos em padrão REST API.
    """
    sections = {
        "symptoms_and_complaints": "",
        "medical_history": "",
        "diagnosis": "",
        "treatments_and_procedures": "",
        "recommendations": "",
    }

    # Regex para capturar cada seção e seu conteúdo
    pattern = re.compile(r"\*\*(.+?)\*\*:([\s\S]*?)(?=\*\*|$)")

    # Mapeamento entre os nomes em inglês e os títulos originais
    title_mapping = {
        "Sintomas e Queixas": "symptoms_and_complaints",
        "Histórico Médico": "medical_history",
        "Diagnóstico": "diagnosis",
        "Tratamento e Procedimentos": "treatments_and_procedures",
        "Recomendações": "recommendations",
    }

    # Iterar pelas correspondências e preencher o dicionário
    matches = pattern.findall(summary_text)
    for match in matches:
        section_title = match[0].strip()
        section_content = match[1].strip()
        # Mapear o título ao campo correspondente no dicionário, se existir
        if section_title in title_mapping:
            rest_api_key = title_mapping[section_title]
            sections[rest_api_key] = section_content

    return sections
