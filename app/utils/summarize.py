import logging
import os

from fastapi import HTTPException
from google.generativeai import GenerativeModel, configure

logger = logging.getLogger(__name__)

configure(api_key=os.environ.get("API_KEY"))


async def summarize_transcription(text: str) -> str:
    try:
        if not text.strip():
            logger.warning("Empty or whitespace-only text received for summarization.")
            raise ValueError("The input text for summarization cannot be empty.")

        model = GenerativeModel("gemini-1.5-flash")
        logger.info("Initialized generative model.")

        response = model.generate_content(text)
        if not response or not hasattr(response, "text"):
            logger.error("No valid response received from generative model.")
            raise ValueError(
                "Failed to retrieve a valid response from the generative model."
            )

        logger.info("Summarization successful.")
        return response.text

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
