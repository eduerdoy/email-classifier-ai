import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configurações da aplicação"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Modelos
    GEMINI_MODEL: str = "gemini-2.0-flash"
    SENTIMENT_MODEL: str = "nlptown/bert-base-multilingual-uncased-sentiment"
    
    # Parâmetros de geração
    TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 200
    CLASSIFICATION_TEMPERATURE: float = 0.1
    
    # Validações
    MIN_RESPONSE_WORDS: int = 8
    TOP_KEYWORDS: int = 5
    
    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY)

settings = Settings()

if not settings.is_gemini_configured:
    raise ValueError("❌ GEMINI_API_KEY não encontrada no arquivo .env")