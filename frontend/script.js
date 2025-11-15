const API_URL = 'https://email-classifier-ai-production.up.railway.app';

// const API_URL = 'http://127.0.0.1:8000';

// Gerenciamento de abas
function showTab(tabName) {
    // Remove active de todas as abas
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Adiciona active na aba selecionada
    event.target.classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');
    
    // Esconde resultado ao trocar de aba
    document.getElementById('resultado').style.display = 'none';
}

// Form de texto
document.getElementById('emailForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        sender: document.getElementById('sender').value,
        subject: document.getElementById('subject').value,
        body: document.getElementById('body').value
    };
    
    await classifyEmail(formData, 'text');
});

// Form de upload
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('sender', document.getElementById('sender-upload').value);
    formData.append('subject', document.getElementById('subject-upload').value || 'Email importado');
    formData.append('file', document.getElementById('file').files[0]);
    
    await classifyEmail(formData, 'upload');
});

// Função principal de classificação
async function classifyEmail(data, type) {
    const loading = document.getElementById('loading');
    const resultado = document.getElementById('resultado');
    
    // Mostra loading
    loading.style.display = 'block';
    resultado.style.display = 'none';
    
    try {
        let response;
        
        if (type === 'text') {
            response = await fetch(`${API_URL}/classify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch(`${API_URL}/classify/upload`, {
                method: 'POST',
                body: data // FormData já tem o Content-Type correto
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao processar email');
        }
        
        const result = await response.json();
        displayResult(result, type);
        
    } catch (error) {
        alert(`Erro: ${error.message}`);
        console.error(error);
    } finally {
        loading.style.display = 'none';
    }
}

// Exibe resultado
function displayResult(data, type) {
    const resultado = document.getElementById('resultado');
    const fileInfo = document.getElementById('file-info');
    
    // Categoria
    const categoryBadge = document.getElementById('category');
    categoryBadge.textContent = data.category;
    categoryBadge.className = `badge ${data.category.toLowerCase()}`;
    
    // // Confiança
    // document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
    
    // // Keywords
    // document.getElementById('keywords').textContent = data.keywords.join(', ');
    
    // Resposta sugerida
    document.getElementById('suggested-reply').textContent = data.suggested_reply;
    
    // Informações do arquivo (só para upload)
    // if (type === 'upload') {
    //     document.getElementById('filename').textContent = data.filename;
    //     document.getElementById('filetype').textContent = data.file_type;
    //     document.getElementById('extracted-text').textContent = data.extracted_text_preview;
    //     fileInfo.style.display = 'block';
    // } else {
    //     fileInfo.style.display = 'none';
    // }

    if (window.innerWidth < 1200) {
        // Pequeno delay para garantir que o DOM foi atualizado
        setTimeout(() => {
            resultado.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }
    
    resultado.style.display = 'block';
    resultado.scrollIntoView({ behavior: 'smooth' });
}

// Copiar resposta
function copyResponse() {
    const reply = document.getElementById('suggested-reply').textContent;
    navigator.clipboard.writeText(reply).then(() => {
        alert('Resposta copiada para a área de transferência!');
    });
}
