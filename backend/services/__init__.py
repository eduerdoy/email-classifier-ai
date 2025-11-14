"""Serviços de processamento de emails"""

from .nlp_service import nlp_service
from .gemini_service import gemini_service
from .classifier_service import classifier_service
from .file_service import file_service

__all__ = [
    'nlp_service', 
    'gemini_service', 
    'classifier_service',
    'file_service'
]