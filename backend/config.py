import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"
    TEMPERATURE: float = 0.7
    CLASSIFICATION_TEMPERATURE: float = 0.1
    MAX_OUTPUT_TOKENS: int = 256
    MIN_RESPONSE_WORDS: int = 8
    TOP_KEYWORDS: int = 5

    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY)

settings = Settings()

if not settings.is_gemini_configured:
    raise ValueError("GEMINI_API_KEY não definida.")