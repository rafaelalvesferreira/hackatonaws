#!/usr/bin/env python3
"""
Demo API para o Agente de Documentos Bedrock
Roda sem credenciais AWS válidas para teste da interface
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# Adiciona o diretório raiz ao path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from config.settings import Config

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)

# Variáveis globais para componentes
document_processor = None
vector_store = None
bedrock_agent = None

def print_banner():
    """Imprime banner de inicialização"""
    print("=" * 60)
    print("🤖 AGENTE DE DOCUMENTOS BEDROCK - MODO DEMO")
    print("=" * 60)
    print("⚠️  ATENÇÃO: Rodando em modo demonstração")
    print("📝 Funcionalidades AWS requerem credenciais válidas")
    print("🌐 API disponível em: http://localhost:5000")
    print("=" * 60)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'healthy',
        'mode': 'demo',
        'message': 'API rodando em modo demonstração',
        'timestamp': str(os.times())
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Retorna status do sistema"""
    try:
        # Verificar se diretórios existem
        documents_exist = os.path.exists(Config.DOCUMENTS_PATH)
        vector_store_exist = os.path.exists(Config.VECTOR_STORE_PATH)
        
        # Contar documentos
        doc_count = 0
        if documents_exist:
            doc_count = len([f for f in os.listdir(Config.DOCUMENTS_PATH) 
                           if f.endswith(('.pdf', '.docx', '.txt'))])
        
        return jsonify({
            'status': 'demo_mode',
            'components': {
                'document_processor': 'demo',
                'vector_store': 'demo', 
                'bedrock_agent': 'demo'
            },
            'documents': {
                'path_exists': documents_exist,
                'count': doc_count,
                'path': Config.DOCUMENTS_PATH
            },
            'vector_store': {
                'path_exists': vector_store_exist,
                'path': Config.VECTOR_STORE_PATH
            },
            'config': {
                'aws_region': Config.AWS_REGION,
                'model_id': Config.BEDROCK_MODEL_ID,
                'chunk_size': Config.CHUNK_SIZE,
                'max_results': Config.MAX_SEARCH_RESULTS
            }
        })
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/documents/upload', methods=['POST'])
def process_documents():
    """Simula processamento de documentos"""
    try:
        # Em modo demo, apenas simula o processamento
        documents_path = Config.DOCUMENTS_PATH
        
        if not os.path.exists(documents_path):
            return jsonify({
                'success': False,
                'error': f'Diretório de documentos não encontrado: {documents_path}'
            }), 400
        
        # Listar arquivos disponíveis
        files = []
        for filename in os.listdir(documents_path):
            if filename.endswith(('.pdf', '.docx', '.txt', '.md')):
                filepath = os.path.join(documents_path, filename)
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'type': filename.split('.')[-1].upper()
                })
        
        return jsonify({
            'success': True,
            'mode': 'demo',
            'message': 'Modo demonstração - processamento simulado',
            'documents_found': len(files),
            'files': files,
            'note': 'Para processamento real, configure credenciais AWS válidas'
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar documentos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Simula chat com o agente"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Mensagem é obrigatória'
            }), 400
        
        user_message = data['message']
        
        # Resposta simulada em modo demo
        demo_response = f"""
🤖 **Modo Demonstração Ativo**

Você perguntou: "{user_message}"

Esta é uma resposta simulada. Em modo de produção com credenciais AWS válidas, eu seria capaz de:

✅ Processar seus documentos PDF e Word
✅ Criar embeddings usando Amazon Titan
✅ Realizar busca vetorial com FAISS
✅ Gerar respostas usando Claude 3 Sonnet
✅ Citar fontes específicas dos documentos

**Para ativar funcionalidade completa:**
1. Configure suas credenciais AWS no arquivo .env
2. Verifique acesso aos modelos Bedrock
3. Reinicie a aplicação

**Documentos encontrados:** {len(os.listdir(Config.DOCUMENTS_PATH)) if os.path.exists(Config.DOCUMENTS_PATH) else 0}
        """.strip()
        
        return jsonify({
            'success': True,
            'mode': 'demo',
            'response': demo_response,
            'sources': [
                {
                    'document': 'demo_document.txt',
                    'chunk': 'Exemplo de chunk de documento',
                    'similarity': 0.85
                }
            ],
            'metadata': {
                'model': 'demo_mode',
                'tokens_used': 0,
                'processing_time': '0.1s'
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/documents/list', methods=['GET'])
def list_documents():
    """Lista documentos disponíveis"""
    try:
        documents_path = Config.DOCUMENTS_PATH
        
        if not os.path.exists(documents_path):
            return jsonify({
                'success': False,
                'error': f'Diretório não encontrado: {documents_path}'
            })
        
        files = []
        for filename in os.listdir(documents_path):
            if filename.endswith(('.pdf', '.docx', '.txt', '.md')):
                filepath = os.path.join(documents_path, filename)
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'type': filename.split('.')[-1].upper()
                })
        
        return jsonify({
            'success': True,
            'documents': files,
            'total': len(files),
            'path': documents_path
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar documentos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado',
        'available_endpoints': [
            'GET /health',
            'GET /status', 
            'POST /documents/upload',
            'GET /documents/list',
            'POST /chat'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor',
        'mode': 'demo'
    }), 500

def main():
    """Função principal"""
    print_banner()
    
    try:
        logger.info("Iniciando API em modo demonstração...")
        
        # Verificar configuração básica
        logger.info(f"Diretório de documentos: {Config.DOCUMENTS_PATH}")
        logger.info(f"Porta: {Config.FLASK_PORT}")
        
        # Iniciar servidor
        app.run(
            host=Config.FLASK_HOST,
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
