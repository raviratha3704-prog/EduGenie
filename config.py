import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:

    # Gemini
    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    # Explanation provider
    explanation_provider: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "local"
    ).lower()

    # Local Hugging Face model
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    # Maximum user input
    max_input_chars: int = int(
        os.getenv(
            "MAX_INPUT_CHARS",
            "30000"
        )
    )

    # Environment
    app_env: str = os.getenv(
        "APP_ENV",
        "development"
    )


settings = Settings()