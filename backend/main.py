from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from schemas import MessageRequest, MessageResponse, FileUploadResponse
from services.classifier_service import classifier_service
from services.file_service import file_service

app = FastAPI(
    title="Email Classifier AI",
    description="API de classificação e resposta automática de emails",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500", 
        "https://seu-frontend.vercel.app",  
        "*"  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Download de recursos NLTK
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Incluir rotas
app.include_router(email_routes.router)

@app.post("/classify", response_model=MessageResponse)
async def classify_email(data: MessageRequest):
    
    try:
        resultado = classifier_service.classify_and_respond(
            sender=data.sender,
            subject=data.subject,
            body=data.body
        )
        return MessageResponse(**resultado)
    
    except Exception as e:
        print(f"Erro no processamento: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar email: {str(e)}"
        )

@app.post("/classify/upload", response_model=FileUploadResponse)
async def classify_email_from_file(
    file: UploadFile = File(..., description="Arquivo TXT ou PDF com o email"),
    sender: str = Form(..., description="Email do remetente"),
    subject: str = Form(default="Email importado", description="Assunto do email (opcional)")
):
    
    try:
        # Valida email do remetente
        if '@' not in sender:
            raise HTTPException(
                status_code=400,
                detail="Email do remetente inválido"
            )
        
        # Lê conteúdo do arquivo
        file_content = await file.read()
        
        print(f"📁 Arquivo recebido: {file.filename} ({len(file_content)} bytes)")
        
        # Extrai texto do arquivo
        try:
            extracted_text = file_service.extract_text_from_file(
                file_content=file_content,
                filename=file.filename
            )
            
            print(f"✅ Texto extraído: {len(extracted_text)} caracteres")
            
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        # Classifica o email extraído
        resultado = classifier_service.classify_and_respond(
            sender=sender,
            subject=subject,
            body=extracted_text
        )
        
        # Prepara resposta com informações do arquivo
        return FileUploadResponse(
            filename=file.filename,
            file_type=file_service._get_file_extension(file.filename),
            extracted_text_preview=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            category=resultado["category"],
            confidence=resultado["confidence"],
            suggested_reply=resultado["suggested_reply"],
            keywords=resultado["keywords"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no processamento do arquivo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "Email Classifier AI está funcionando!"}

@app.get("/health")
async def health_check():
    """Verifica status da API"""
    return {
        "status": "ok", 
        "message": "Email Classifier AI está funcionando",
        "supported_formats": file_service.SUPPORTED_FORMATS,
        "max_file_size_mb": file_service.MAX_FILE_SIZE / 1024 / 1024
    }