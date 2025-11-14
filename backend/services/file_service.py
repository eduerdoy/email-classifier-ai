import PyPDF2
from typing import Optional
from io import BytesIO

class FileService:
    """Serviço para extrair texto de arquivos"""
    
    SUPPORTED_FORMATS = ['.txt', '.pdf']
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    def extract_text_from_file(
        self, 
        file_content: bytes, 
        filename: str
    ) -> str:
       
        # Valida tamanho
        if len(file_content) > self.MAX_FILE_SIZE:
            raise ValueError(f"Arquivo muito grande. Tamanho máximo: {self.MAX_FILE_SIZE / 1024 / 1024}MB")
        
        # Determina tipo de arquivo
        file_ext = self._get_file_extension(filename)
        
        if file_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Formato '{file_ext}' não suportado. "
                f"Formatos aceitos: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        # Extrai texto baseado no tipo
        if file_ext == '.txt':
            return self._extract_from_txt(file_content)
        elif file_ext == '.pdf':
            return self._extract_from_pdf(file_content)
        
        raise ValueError(f"Erro ao processar arquivo {filename}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Retorna extensão do arquivo em lowercase"""
        return '.' + filename.split('.')[-1].lower() if '.' in filename else ''
    
    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extrai texto de arquivo TXT"""
        try:
            # Tenta decodificar em UTF-8
            text = file_content.decode('utf-8')
            
            if not text.strip():
                raise ValueError("Arquivo TXT está vazio")
            
            return text
            
        except UnicodeDecodeError:
            # Fallback para latin-1
            try:
                text = file_content.decode('latin-1')
                if not text.strip():
                    raise ValueError("Arquivo TXT está vazio")
                return text
            except:
                raise ValueError("Não foi possível decodificar o arquivo TXT")
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            # Cria objeto BytesIO
            pdf_file = BytesIO(file_content)
            
            # Lê PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Valida número de páginas
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                raise ValueError("PDF não contém páginas")
            
            # Extrai texto de todas as páginas
            text_parts = []
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text_parts.append(page_text)
            
            # Junta todo o texto
            full_text = '\n'.join(text_parts)
            
            if not full_text.strip():
                raise ValueError("PDF não contém texto extraível (pode ser imagem)")
            
            return full_text
            
        except PyPDF2.errors.PdfReadError as e:
            raise ValueError(f"Erro ao ler PDF: {str(e)}")
        except Exception as e:
            raise ValueError(f"Erro ao processar PDF: {str(e)}")

# Instância singleton
file_service = FileService()