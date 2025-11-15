from config import settings
from services.nlp_service import nlp_service
from services.gemini_service import gemini_service
from typing import Dict, Tuple
from nltk.sentiment import SentimentIntensityAnalyzer
import os, nltk, pathlib

_NOREPLY_PATTERNS = ("noreply", "no-reply", "donotreply", "do-not-reply", "automat", "auto-mail")

def ensure_nltk_ready():
    nltk_dir = os.getenv("NLTK_DATA", "/tmp/nltk_data")
    pathlib.Path(nltk_dir).mkdir(parents=True, exist_ok=True)
    if nltk_dir not in nltk.data.path:
        nltk.data.path.append(nltk_dir)
    for path, pkg in [("sentiment/vader_lexicon","vader_lexicon")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, download_dir=nltk_dir)

class ClassifierService:
    def __init__(self):
        self.nlp = nlp_service
        self.gemini = gemini_service
        ensure_nltk_ready()
        self.sentiment = SentimentIntensityAnalyzer()

    def classify_and_respond(self, sender: str, subject: str, body: str) -> Dict[str, any]:
        sender_lower = sender.lower()
        if any(p in sender_lower for p in _NOREPLY_PATTERNS):
            return {
                "category": "Improdutivo",
                "confidence": 0.95,
                "suggested_reply": "Este é um email automático; não é necessário responder.",
                "keywords": [],
                "processed_text": "",
            }

        texto_original = f"{subject}. {body}"
        texto_processado = self.nlp.preprocess_text(texto_original)
        keywords = self.nlp.extract_keywords(texto_original, settings.TOP_KEYWORDS)

        try:
            category, confidence = self.gemini.classify_email(subject, body)
        except Exception:
            category, confidence = self._fallback_classify(texto_original)

        sender_name = self._extract_sender_name(sender)
        try:
            resposta = self.gemini.generate_response(category, sender_name, subject, body, keywords)
            resposta = self._clean_response(resposta)
        except Exception:
            resposta = self._fallback_response(category, subject)

        return {
            "category": category,
            "confidence": confidence,
            "suggested_reply": resposta,
            "keywords": keywords,
            "processed_text": texto_processado[:200],
        }

    def _extract_sender_name(self, sender: str) -> str:
        try:
            return sender.split('@')[0].replace('.', ' ').title()
        except:
            return "Colega"

    def _fallback_classify(self, text: str) -> Tuple[str, float]:
        t = text.lower()
        produtivo = [
            "reunião","projeto","prazo","entrega","urgente","aprovação","orçamento",
            "contrato","proposta","documento","relatório","vaga","entrevista",
            "solicitação","pendência","ação","tarefa","cliente","processo","suporte",
            "solicito","confirmação","agendar","discussão","imediato","urgência"
        ]
        improdutivo = [
            "parabéns","feliz","aniversário","natal","ano novo","obrigado",
            "bom dia","nada","férias","feriado","festa","casamento","abraço","não responder",
            "email automático","noreply","no-reply","teste"
        ]
        p = sum(k in t for k in produtivo)
        i = sum(k in t for k in improdutivo)
        if p > i:
            return "Produtivo", min(0.6 + p*0.05, 0.85)
        if i > p:
            return "Improdutivo", min(0.6 + i*0.05, 0.85)
        comp = self.sentiment.polarity_scores(text)["compound"]
        if comp < -0.2:
            return "Improdutivo", 0.55
        return "Produtivo", 0.55

    def _clean_response(self, resposta: str) -> str:
        for marker in ["Atenciosamente", "Abraços", "Cordialmente"]:
            resposta = resposta.split(marker)[0]
        resposta = resposta.strip()
        if resposta and not resposta.endswith(('.', '!', '?')):
            resposta += '.'
        return resposta

    def _fallback_response(self, category: str, subject: str) -> str:
        if category == "Improdutivo":
            return "Obrigado pela mensagem! Agradecemos o contato."
        return f"Recebemos sua mensagem sobre '{subject}'. Retornaremos em breve."

classifier_service = ClassifierService()