from config import settings
from services.nlp_service import nlp_service
from services.gemini_service import gemini_service
from typing import Dict, Tuple
from nltk.sentiment import SentimentIntensityAnalyzer
import os, nltk, pathlib
from datetime import datetime

_NOREPLY_PATTERNS = ("noreply", "no-reply", "donotreply", "do-not-reply", "automat", "auto-mail")

def ensure_nltk_ready():
    nltk_dir = os.getenv("NLTK_DATA", "/tmp/nltk_data")
    pathlib.Path(nltk_dir).mkdir(parents=True, exist_ok=True)
    if nltk_dir not in nltk.data.path:
        nltk.data.path.append(nltk_dir)
    for path, pkg in [("sentiment/vader_lexicon","vader_lexicon")]:
        try:
            nltk.data.find(path)
            print(f"✅ NLTK resource {pkg} encontrado")
        except LookupError:
            print(f"⬇️ Baixando NLTK resource {pkg}...")
            nltk.download(pkg, download_dir=nltk_dir)

class ClassifierService:
    def __init__(self):
        print("🚀 INICIALIZANDO ClassifierService...")
        self.nlp = nlp_service
        self.gemini = gemini_service
        ensure_nltk_ready()
        self.sentiment = SentimentIntensityAnalyzer()
        print("✅ ClassifierService PRONTO!")

    def classify_and_respond(self, sender: str, subject: str, body: str) -> Dict[str, any]:
        start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"📧 PROCESSANDO EMAIL")
        print(f"De: {sender}")
        print(f"Assunto: {subject}")
        print(f"Corpo: {body[:100]}...")
        print(f"{'='*60}")

        # Verificar noreply
        sender_lower = sender.lower()
        if any(p in sender_lower for p in _NOREPLY_PATTERNS):
            print(f"🚫 EMAIL NOREPLY DETECTADO - IGNORANDO")
            return {
                "category": "Improdutivo",
                "confidence": 0.95,
                "suggested_reply": "Este é um email automático, não é necessário responder.",
                "keywords": [],
                "processed_text": "",
            }

        # Processar texto
        print("🔄 PROCESSANDO TEXTO...")
        texto_original = f"{subject}. {body}"
        texto_processado = self.nlp.preprocess_text(texto_original)
        keywords = self.nlp.extract_keywords(texto_original, settings.TOP_KEYWORDS)
        print(f"🔑 Keywords: {keywords}")

        # CLASSIFICAÇÃO COM GEMINI
        print("🤖 === TENTANDO CLASSIFICAR COM GEMINI ===")
        try:
            category, confidence = self.gemini.classify_email(subject, body)
            print(f"✅ GEMINI SUCESSO: {category} (conf: {confidence})")
        except Exception as e:
            print(f"❌ GEMINI FALHOU!")
            print(f"   Erro: {type(e).__name__}: {str(e)}")
            print(f"   🔄 Usando fallback...")
            category, confidence = self._fallback_classify(texto_original)
            print(f"   ✅ Fallback resultado: {category} (conf: {confidence})")

        # RESPOSTA COM GEMINI
        sender_name = self._extract_sender_name(sender)
        print(f"👤 Sender name: {sender_name}")
        print("💬 === TENTANDO GERAR RESPOSTA COM GEMINI ===")
        try:
            resposta = self.gemini.generate_response(category, sender_name, subject, body, keywords)
            resposta = self._clean_response(resposta)
            print(f"✅ GEMINI RESPOSTA SUCESSO: {len(resposta)} chars")
        except Exception as e:
            print(f"❌ GEMINI RESPOSTA FALHOU!")
            print(f"   Erro: {type(e).__name__}: {str(e)}")
            print(f"   🔄 Usando resposta fallback...")
            resposta = self._fallback_response(category, subject)
            print(f"   ✅ Fallback resposta: {resposta[:50]}...")

        # Resultado
        processing_time = (datetime.now() - start_time).total_seconds()
        result = {
            "category": category,
            "confidence": confidence,
            "suggested_reply": resposta,
            "keywords": keywords,
            "processed_text": texto_processado[:200],
        }
        
        print(f"🎯 PROCESSAMENTO CONCLUÍDO em {processing_time:.2f}s")
        print(f"📊 Resultado: {category} | Confiança: {confidence}")
        print(f"{'='*60}\n")
        
        return result

    def _extract_sender_name(self, sender: str) -> str:
        try:
            return sender.split('@')[0].replace('.', ' ').title()
        except:
            return "Colega"

    def _fallback_classify(self, text: str) -> Tuple[str, float]:
        print("🔄 EXECUTANDO FALLBACK CLASSIFICATION...")
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
            
        p_matches = [k for k in produtivo if k in t]
        i_matches = [k for k in improdutivo if k in t]
        p = len(p_matches)
        i = len(i_matches)
        
        print(f"   Produtivo matches ({p}): {p_matches}")
        print(f"   Improdutivo matches ({i}): {i_matches}")
        
        if p > i:
            conf = min(0.6 + p*0.05, 0.85)
            print(f"   → PRODUTIVO (score {p})")
            return "Produtivo", conf
        if i > p:
            conf = min(0.6 + i*0.05, 0.85)
            print(f"   → IMPRODUTIVO (score {i})")
            return "Improdutivo", conf
            
        # Empate: análise de sentimento
        comp = self.sentiment.polarity_scores(text)["compound"]
        print(f"   Empate! Sentimento: {comp}")
        if comp < -0.2:
            print("   → IMPRODUTIVO (sentimento negativo)")
            return "Improdutivo", 0.55
        print("   → PRODUTIVO (padrão)")
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