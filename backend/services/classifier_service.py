from transformers import pipeline
from config import settings
from services.nlp_service import nlp_service
from services.gemini_service import gemini_service
from typing import Dict
import re

# Classificador de sentimento (fallback)
sentiment_classifier = pipeline(
    "text-classification",
    model=settings.SENTIMENT_MODEL
)

class ClassifierService:
    """Serviço principal de classificação de emails"""
    
    def __init__(self):
        self.nlp = nlp_service
        self.gemini = gemini_service
    
    def classify_and_respond(
        self, 
        sender: str, 
        subject: str, 
        body: str
    ) -> Dict[str, any]:
       
        
        print(f"\n{'='*60}")
        print(f"📧 PROCESSANDO EMAIL")
        print(f"{'='*60}")
        print(f"📝 Assunto: {subject[:80]}...")
        print(f"👤 Remetente: {sender}")
        
        # 1. Pré-processamento NLP
        texto_original = f"{subject}. {body}"
        texto_processado = self.nlp.preprocess_text(texto_original)
        keywords = self.nlp.extract_keywords(texto_original, settings.TOP_KEYWORDS)
        
        print(f"🔧 Texto processado: {texto_processado[:100]}...")
        print(f"🔑 Keywords: {keywords}")
        
        # 2. Classificação
        try:
            category, confidence = self.gemini.classify_email(subject, body)
        except Exception as e:
            print(f"Erro no Gemini, usando fallback de sentimento...")
            category, confidence = self._classify_with_sentiment(texto_original)
        
        print(f"Classificado: {category} (confiança: {confidence})")
        
        # 3. Geração de resposta
        sender_name = self._extract_sender_name(sender)
        
        try:
            resposta = self.gemini.generate_response(
                category, sender_name, subject, body, keywords
            )
            resposta = self._clean_response(resposta, sender_name)
            
        except Exception as e:
            print(f"Erro na geração, usando resposta padrão...")
            resposta = self._fallback_response(category, sender_name, subject)
        
        print(f"Resposta: {resposta[:100]}...")
        print(f"{'='*60}\n")
        
        return {
            "category": category,
            "confidence": confidence,
            "suggested_reply": resposta,
            "keywords": keywords,
            "processed_text": texto_processado[:200]
        }
    
    def _extract_sender_name(self, sender: str) -> str:
        """Extrai nome do remetente do email"""
        try:
            return sender.split('@')[0].replace('.', ' ').title()
        except:
            return "Colega"
    
    def _classify_with_sentiment(self, text: str) -> tuple:
        """Classificação de fallback usando sentimento"""
        result = sentiment_classifier(text)[0]
        label = result.get("label", "")
        confidence = round(result.get("score", 0.0), 3)
        category = "Produtivo" if label in ["4 stars", "5 stars"] else "Improdutivo"
        return category, confidence
    
    def _clean_response(self, resposta: str, sender_name: str) -> str:
        """Limpa e formata a resposta gerada"""
        # Remove assinaturas
        resposta = resposta.split("Atenciosamente")[0]
        resposta = resposta.split("Abraços")[0]
        resposta = resposta.split("Cordialmente")[0]
        resposta = resposta.strip()
        
        # # Garante saudação inicial
        # if not resposta.lower().startswith(f"olá"):
        #     resposta = f"Olá! {resposta}"
        
        # Garante pontuação final
        if not resposta.endswith(('.', '!', '?')):
            resposta += '.'
        
        return resposta
    
    def _fallback_response(self, category: str, sender_name: str, subject: str) -> str:
        """Resposta padrão em caso de erro"""
        if category == "Improdutivo":
            return f"Muito obrigado pela sua mensagem. É sempre um prazer receber notícias suas!"
        else:
            return f"Recebemos sua mensagem sobre '{subject}'. Nossa equipe está analisando e retornará em breve."

# Instância singleton
classifier_service = ClassifierService()