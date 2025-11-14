import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from collections import Counter
from typing import List

# Download de recursos NLTK
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')
    nltk.download('rslp')

class NLPService:
    """Serviço de processamento de linguagem natural"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = RSLPStemmer()
    
    def preprocess_text(self, text: str) -> str:
       
        # Lowercasing
        text = text.lower()
        
        # Remove emails e URLs
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove números
        text = re.sub(r'\d+', '', text)
        
        # Remove pontuação
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenização
        tokens = text.split()
        
        # Remove stop words
        tokens = [word for word in tokens if word not in self.stop_words]
        
        # Stemming
        tokens = [self.stemmer.stem(word) for word in tokens]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extrai as palavras-chave mais importantes do texto"""
        processed = self.preprocess_text(text)
        word_freq = Counter(processed.split())
        return [word for word, _ in word_freq.most_common(top_n)]

# Instância singleton
nlp_service = NLPService()