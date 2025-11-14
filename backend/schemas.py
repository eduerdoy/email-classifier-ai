from pydantic import BaseModel, Field, validator
from typing import Optional, List

class MessageRequest(BaseModel):
    """Schema para requisição de classificação via texto"""
    sender: str = Field(..., description="Email do remetente")
    subject: str = Field(..., description="Assunto do email")
    body: str = Field(..., description="Corpo do email")
    
    @validator('sender')
    def validate_sender(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v

class MessageResponse(BaseModel):
    """Schema para resposta da classificação"""
    category: str = Field(..., description="Categoria: Produtivo ou Improdutivo")
    confidence: float = Field(..., description="Confiança da classificação (0-1)")
    suggested_reply: str = Field(..., description="Resposta sugerida")
    keywords: List[str] = Field(default=[], description="Palavras-chave extraídas")
    processed_text: Optional[str] = Field(None, description="Texto pré-processado")

class FileUploadResponse(BaseModel):
    """Schema para resposta de upload de arquivo"""
    filename: str = Field(..., description="Nome do arquivo enviado")
    file_type: str = Field(..., description="Tipo do arquivo (.txt ou .pdf)")
    extracted_text_preview: str = Field(..., description="Preview do texto extraído")
    category: str = Field(..., description="Categoria: Produtivo ou Improdutivo")
    confidence: float = Field(..., description="Confiança da classificação")
    suggested_reply: str = Field(..., description="Resposta sugerida")
    keywords: List[str] = Field(default=[], description="Palavras-chave extraídas")