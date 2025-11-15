# Email Classifier AI

> Sistema inteligente de classificação e resposta automática de emails usando IA Generativa

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.0_Flash-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Sobre o Projeto

Sistema desenvolvido para **automatizar a classificação de emails corporativos** em **Produtivo** ou **Improdutivo** e **sugerir respostas automáticas contextualizadas**, liberando tempo da equipe para atividades estratégicas.

**Case técnico desenvolvido para:** AutoU  
**Autor:** Eduardo Augusto Pinto Correa  

---

## ✨ Funcionalidades

- ✅ **Classificação inteligente** em Produtivo/Improdutivo usando Google Gemini 2.0 Flash
- ✅ **Processamento NLP avançado** com remoção de stop words, stemming (RSLP) e extração de keywords
- ✅ **Múltiplos formatos de entrada**: Texto direto, upload de TXT e PDF
- ✅ **Geração automática de respostas** contextualizadas por categoria
- ✅ **Interface web moderna** e responsiva (desktop + mobile)
- ✅ **API REST completa** com documentação interativa (Swagger)
- ✅ **Sistema de fallback** com análise de sentimento (transformers)

---

## 🏗️ Arquitetura

```
email-classifier-ai/
├── backend/
│   ├── services/
│   │   ├── nlp_service.py          # Processamento NLP (stop words, stemming)
│   │   ├── gemini_service.py       # Integração Gemini AI
│   │   ├── classifier_service.py   # Lógica de classificação
│   │   └── file_service.py         # Extração de texto (TXT/PDF)
│   ├── config.py                   # Configurações centralizadas
│   ├── main.py                     # API FastAPI
|   ├── Procfile                    # Para deploy
|   ├── Runtime.txt                 # Para deploy
│   ├── schemas.py                  # Modelos Pydantic
│   ├── requirements.txt            # Dependências Python
│   └── runtime.txt                 # Versão do Python (deploy)
├── frontend/
│   ├── index.html                  # Interface web
│   ├── style.css                   # Estilos responsivos
│   ├── script.js                   # Lógica cliente
│   └── vercel.json                 # Configuração Vercel
├── .gitignore                      # Arquivos ignorados
└── README.md                       # Este arquivo
```

---

## 🚀 Como Executar Localmente

### **Pré-requisitos**

- Python 3.11 ou superior
- Chave de API do Google Gemini ([obter aqui](https://aistudio.google.com/app/apikey))

### **1. Clonar o repositório**

```bash
git clone https://github.com/eduerdoy/email-classifier-ai.git
cd email-classifier-ai
```

### **2. Configurar Backend**

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### **3. Configurar variáveis de ambiente**

Crie o arquivo `.env` na pasta `backend/`:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### **4. Iniciar servidor backend**

```bash
uvicorn main:app --reload
```

A API estará rodando em: **http://localhost:8000**

### **5. Abrir Frontend**


**Opção A:** Use um servidor local (recomendado):
```bash
# Com Python
cd frontend
python -m http.server 5500

# Acesse: http://localhost:5500
```

**Opção B:** Use a extensão **Live Server** do VS Code

---

## 🌐 Deploy em Produção

### **URLs da aplicação:**


| **Vercel** | https://email-classifier-ai-ten.vercel.app |



### **💡 Dica:**
> Se ao acessar pela primeira vez o backend demorar, **aguarde ~30 segundos**. O servidor gratuito está iniciando. As próximas requisições serão rápidas!

---

## 🧠 Tecnologias Utilizadas

### **Backend**
- **FastAPI** - Framework web moderno e de alta performance
- **Google Gemini AI**  - LLM para classificação e geração de respostas
- **NLTK** - Processamento de linguagem natural (stop words, stemming)
- **PyPDF2** - Extração de texto de arquivos PDF
- **Pydantic** 2.5.0 - Validação de dados e schemas

### **Frontend**
- **HTML5/CSS3/JavaScript** - Interface web responsiva
- **Fetch API** - Comunicação assíncrona com backend
- **CSS Grid/Flexbox** - Layout responsivo (2 colunas desktop / empilhado mobile)

### **Deploy**
- **Railway** - Hospedagem do backend (Python/FastAPI)
- **Vercel** - Hospedagem do frontend (SPA estático)
- **GitHub** - Controle de versão e CI/CD automático

---

## 🔬 Pipeline de Processamento NLP

### **Etapas do pré-processamento:**

```python
1. Lowercasing          → "REUNIÃO" → "reunião"
2. Remoção de URLs      → "http://site.com" → ""
3. Remoção de emails    → "contato@email.com" → ""
4. Remoção de números   → "123 456" → ""
5. Remoção de pontuação → "Olá!" → "Olá"
6. Tokenização          → "Olá mundo" → ["olá", "mundo"]
7. Stop words (PT-BR)   → ["o", "a", "de"] → [] (removidos)
8. Stemming (RSLP)      → ["reunião", "reuniões"] → ["reuni"]
9. Extração keywords    → Top 5 palavras por frequência
```

### **Classificação via IA:**

```
Texto processado → Gemini AI → Categoria + Confiança
                              → Resposta contextualizada
```

### **Sistema de fallback:**

```
Gemini AI falha? → Classificador de sentimento
                 → POSITIVE/NEGATIVE/NEUTRAL
                 → Categoria baseada em sentimento
```

---

## 📊 Categorias de Classificação

### **✅ Produtivo**
Emails que exigem ação profissional ou resposta formal:

- 📋 Solicitações de trabalho, reuniões, documentos
- 💼 Processos seletivos, entrevistas, vagas
- 📈 Status de projetos, relatórios, prazos
- 💰 Propostas comerciais, orçamentos, contratos
- ✔️ Aprovações, pendências e ações necessárias

**Exemplo de resposta gerada:**
> "Olá! Recebemos sua mensagem sobre [assunto]. Nossa equipe está analisando e retornará em breve com as informações solicitadas. Agradecemos o contato!"

---

### **🔕 Improdutivo**
Emails sociais, de cortesia ou sem ação necessária:

- 🎂 Felicitações (aniversário, natal, ano novo)
- 👋 Cumprimentos diários (bom dia, boa tarde)
- 🙏 Agradecimentos simples
- 💬 Mensagens pessoais sem contexto de negócios
- ❤️ Votos de felicidade, saúde, etc.

**Exemplo de resposta gerada:**
> "Olá! Muito obrigado pela sua mensagem. É sempre um prazer receber notícias suas!"

---

## 🎨 Interface

### **Funcionalidades da Interface:**

#### **Desktop (≥ 1200px):**
- ✅ **Layout em 2 colunas:** Formulário à esquerda (sticky) + Resultado à direita
- ✅ **Placeholder elegante:** "Aguardando classificação..." quando vazio
- ✅ **Sem scroll desnecessário:** Tudo visível simultaneamente

#### **Mobile (< 1200px):**
- ✅ **Layout empilhado:** Formulário acima + Resultado abaixo
- ✅ **Scroll automático:** Desce para o resultado ao processar
- ✅ **Abas otimizadas:** Digitar Email / Upload de Arquivo

#### **Recursos gerais:**
- ✅ **Spinner centralizado** durante processamento
- ✅ **Copiar resposta** com um clique
- ✅ **Badges coloridos** para categorias (verde/vermelho)
- ✅ **Animações suaves** (fade in, slide in)

---

## 🔧 Configurações Avançadas

### **Ajustar temperatura do modelo:**

```python
# backend/config.py

TEMPERATURE = 0.7  # Criatividade das respostas (0.0 a 1.0)
# 0.0 = Muito previsível, conservador
# 0.7 = Balanceado (padrão)
# 1.0 = Muito criativo, variado

CLASSIFICATION_TEMPERATURE = 0.1  # Precisão da classificação (use baixo)
MAX_OUTPUT_TOKENS = 200  # Tamanho máximo da resposta
```

### **Alterar modelo Gemini:**

```python
# backend/config.py

GEMINI_MODEL = "gemini-2.0-flash-exp"  # Padrão (rápido + barato)

# Alternativas:
# "gemini-pro"           → Mais preciso, mais caro
# "gemini-1.5-flash"     → Versão anterior, estável
# "gemini-1.5-pro"       → Máxima qualidade, custo alto
```


## 🧪 Exemplos de Uso

### **Exemplo 1: Email Produtivo**

**Input:**
```
Remetente: recrutamento@empresa.com
Assunto: Processo Seletivo - Dúvidas
Corpo: Olá! Gostaria de saber quais serão as próximas etapas do PS.
```

**Output:**
```json
{
  "category": "Produtivo",
  "confidence": 0.95,
  "suggested_reply": "Olá! Recebemos sua mensagem sobre o processo seletivo. Nossa equipe está analisando e retornará em breve com as próximas etapas. Agradecemos o contato!",
  "keywords": ["processo", "seletivo", "gostaria", "etapas"],
  "sentiment": "POSITIVE"
}
```

---

### **Exemplo 2: Email Improdutivo**

**Input:**
```
Remetente: amigo@email.com
Assunto: Feliz Aniversário!
Corpo: Olá! Desejo um feliz aniversário e muitas realizações neste 
       novo ciclo. Que você alcance todos os seus objetivos!
```

**Output:**
```json
{
  "category": "Improdutivo",
  "confidence": 0.91,
  "suggested_reply": "Olá! Muito obrigado pela sua mensagem. É um prazer receber as suas felicitações!",
  "keywords": ["feliz", "aniversário", "realizações", "objetivos"],
  "sentiment": "POSITIVE"
}
```

---

## 📈 Melhorias Futuras

- [ ] **Autenticação de usuários** (OAuth2/JWT)
- [ ] **Histórico de classificações** com persistência (PostgreSQL/MongoDB)
- [ ] **Integração com Gmail API** (classificação automática)
- [ ] **Exportar relatórios** em CSV/PDF
- [ ] **Dashboard de analytics** (gráficos de uso)
- [ ] **Suporte a múltiplos idiomas** (EN, ES, FR)
- [ ] **Fine-tuning do modelo** com dataset customizado
- [ ] **Rate limiting inteligente** (Redis + cache)
- [ ] **Webhook para notificações** (Slack/Discord)
- [ ] **Modo offline** com Service Workers (PWA)

---

## ⚠️ Limitações Conhecidas

### **API Gemini (Free Tier):**
- ⚠️ **10 requisições/minuto** - Adequado para testes, não para produção em escala
- ⚠️ **1.500 requisições/dia** - ~200 emails classificados (considerando retries)
- ⚠️ **Rate limit 429** pode ocorrer em uso intenso


### **Processamento de PDFs:**
- ⚠️ **Limite de 5MB** por arquivo
- ⚠️ **PDFs escaneados** (imagem) não são suportados (OCR necessário)
- ⚠️ **Formatação complexa** pode afetar extração de texto

### **Classificação:**
- ⚠️ **Contexto limitado** a ~8.000 tokens (emails muito longos são truncados)
- ⚠️ **Falsos positivos** podem ocorrer em emails ambíguos
- ⚠️ **Depende da qualidade** do prompt e do modelo Gemini

---


## 📄 Licença

Este projeto foi desenvolvido como **case técnico** para a **AutoU**.

**Uso:** Educacional e demonstrativo  
**Autor:** Eduardo Augusto Pinto Correa  

---

## 👤 Autor

**Eduardo Augusto Pinto Correa**

- 🌐 **GitHub:** [@eduerdoy](https://github.com/seu-usuario)
- 💼 **LinkedIn:** [Eduardo Correa](https://linkedin.com/in/seu-perfil)
- 📧 **Email:** eduardo.correap17@gmail.com

---

## 🙏 Agradecimentos

- **AutoU** pela oportunidade do desafio técnico
- **Google Gemini AI** pela API de IA generativa gratuita
- **FastAPI** pela documentação excelente
- **NLTK** pelos recursos de NLP em português
- Comunidade open-source pelas bibliotecas utilizadas

---

## 📞 Suporte


### **Quer contribuir?**
Pull requests são bem-vindos! 🚀

---

<div align="center">


⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!

</div>
