import google.generativeai as genai
from config import settings
from typing import Tuple

# Configura Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    """Serviço de integração com Google Gemini"""
    
    CLASSIFICATION_INSTRUCTION = """Você é um classificador especializado de emails corporativos.

Sua tarefa é classificar emails em APENAS duas categorias:

**PRODUTIVO**: Emails relacionados a trabalho, negócios e assuntos profissionais, incluindo:
- Solicitações de trabalho, reuniões, documentos
- Processos seletivos, entrevistas, vagas de emprego
- Status de projetos, relatórios, prazos
- Propostas comerciais, orçamentos, contratos
- Aprovações, pendências profissionais
- Questões técnicas ou administrativas
- Qualquer assunto que exija ação profissional


**IMPRODUTIVO**: Emails sociais, pessoais ou de cortesia, incluindo:
- Felicitações (aniversário, natal, ano novo, casamento)
- Cumprimentos diários sem contexto profissional
- Mensagens de agradecimento simples
- Conversas pessoais sem objetivo de trabalho
- Emails sobre aviso que confirme o pagamento de fatura
- Emails ou propagandas SPAM
- Avisos sobre alterações de senha

IMPORTANTE:
- Se o email mencionar aprovação em "processo seletivo", "vaga", "entrevista", "aprovado", "candidatura" → É PRODUTIVO
- Se tiver "parabéns" mas for sobre trabalho/aprovação profissional → É PRODUTIVO  
- Se for só felicitação social sem contexto de negócios → É IMPRODUTIVO

Responda APENAS com uma destas opções exatas:
- "Produtivo" 
- "Improdutivo"

Não adicione explicações, apenas a categoria."""

    RESPONSE_INSTRUCTIONS = {
        "Improdutivo": """Você é um assistente de email amigável em português brasileiro.

Sua tarefa é escrever respostas calorosas, naturais e pessoais para emails sociais.

Regras:
- Seja cordial, empático e humano
- Use tom informal mas respeitoso
- Mantenha a resposta em 2-3 frases
- Retribua o sentimento do remetente
- Não use jargões corporativos
- Se em alguma parte do email estiver dizendo que é uma resposta automática, não respota e considere improdutivo
- Não mencione que você é uma IA""",

        "Produtivo": """Você é um assistente de email profissional em português brasileiro.

Sua tarefa é escrever respostas objetivas, informativas e profissionais.

Regras:
- Seja formal mas cordial
- Confirme o recebimento do email
- Indique próximos passos quando relevante
- Se a respostas estiver em inglês, responda em pt-br
- Use tom profissional
- Não mencione que você é uma IA"""
    }
    
    def classify_email(self, subject: str, body: str) -> Tuple[str, float]:
        """
        Classifica email usando Gemini
        
        Returns:
            tuple: (category, confidence)
        """
        try:
            print(f"Chamando Gemini para classificação...")
            
            model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                system_instruction=self.CLASSIFICATION_INSTRUCTION
            )
            
            prompt = f"""Classifique este email:

**Assunto:** {subject}

**Corpo do email:**
{body}

**Categoria:**"""
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.CLASSIFICATION_TEMPERATURE,
                    max_output_tokens=10,
                )
            )
            
            category_raw = response.text.strip().lower()
            print(f"Resposta do Gemini: '{category_raw}'")
            
            # Normaliza a resposta
            if "produtivo" in category_raw and "improdutivo" not in category_raw:
                return "Produtivo", 0.90
            elif "improdutivo" in category_raw:
                return "Improdutivo", 0.90
            else:
                # Fallback
                print(f"Resposta inesperada, usando fallback")
                return "Produtivo", 0.50
                
        except Exception as e:
            print(f"Erro na classificação: {e}")
            raise
    
    def generate_response(
        self, 
        category: str, 
        sender_name: str, 
        subject: str, 
        body: str, 
        keywords: list
    ) -> str:
        """
        Gera resposta usando Gemini
        
        Args:
            category: Categoria do email (Produtivo/Improdutivo)
            sender_name: Nome do remetente
            subject: Assunto do email
            body: Corpo do email
            keywords: Palavras-chave extraídas
            
        Returns:
            str: Resposta gerada
        """
        try:
            print(f"Gerando resposta com Gemini...")
            
            system_instruction = self.RESPONSE_INSTRUCTIONS[category]
            
            if category == "Improdutivo":
                prompt = f"""Responda este email social de forma amigável:

**De:** {sender_name}
**Assunto:** {subject}
**Mensagem:** {body}

**Palavras-chave identificadas:** {', '.join(keywords)}

Seja caloroso e natural."""
            else:
                prompt = f"""Responda este email profissional:

**De:** {sender_name}
**Assunto:** {subject}
**Mensagem:** {body}

**Palavras-chave identificadas:** {', '.join(keywords)}

Confirme o recebimento de forma profissional."""
            
            model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                system_instruction=system_instruction
            )
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_OUTPUT_TOKENS,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Erro na geração de resposta: {e}")
            raise

# Instância singleton
gemini_service = GeminiService()