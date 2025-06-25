#!/usr/bin/env python3
"""
App principal que usa credenciais das variáveis de ambiente da AWS CLI - VERSÃO CORRIGIDA
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import boto3

# Adiciona o diretório raiz ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Usar configuração que pega credenciais da AWS CLI
from config.settings_aws_cli import Config as config
from src.document_processor import DocumentProcessor

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

def check_aws_credentials():
    """Verifica e exibe credenciais AWS"""
    logger.info("🔍 Verificando credenciais AWS...")
    
    # Verificar credenciais
    creds = config.get_aws_credentials()
    logger.info(f"   Região: {creds['region']}")
    logger.info(f"   Access Key: {creds['access_key_preview']}")
    logger.info(f"   Secret Key: {'SET' if creds['secret_key_set'] else 'NOT_SET'}")
    logger.info(f"   Session Token: {'SET' if creds['session_token_set'] else 'NOT_SET'}")
    
    # Validar credenciais
    valid, missing = config.validate_aws_credentials()
    if not valid:
        logger.error(f"❌ Credenciais faltando: {missing}")
        logger.error("💡 Execute: aws configure ou aws sso login")
        return False
    
    # Testar credenciais com STS
    try:
        sts_client = boto3.client(
            'sts',
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN
        )
        
        identity = sts_client.get_caller_identity()
        logger.info(f"✅ Credenciais válidas - User: {identity.get('Arn', 'N/A')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao validar credenciais: {e}")
        if "ExpiredToken" in str(e):
            logger.error("💡 Token expirado - Execute: aws sso login")
        return False

def create_boto3_client(service_name, region=None):
    """Cria cliente boto3 com credenciais explícitas"""
    return boto3.client(
        service_name,
        region_name=region or config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=config.AWS_SESSION_TOKEN
    )

def initialize_components():
    """Inicializa componentes do sistema"""
    global document_processor, vector_store, bedrock_agent
    
    try:
        logger.info("Inicializando componentes do sistema...")
        
        # Verificar credenciais AWS primeiro
        if not check_aws_credentials():
            logger.error("❌ Credenciais AWS inválidas")
            return False
        
        # Document Processor
        document_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        logger.info("✅ Document Processor inicializado")
        
        # Vector Store com credenciais explícitas
        logger.info("Inicializando Vector Store...")
        from src.vector_store_aws_cli import VectorStoreAWSCLI
        vector_store = VectorStoreAWSCLI(
            aws_region=config.AWS_REGION,
            embedding_model_id=config.BEDROCK_EMBEDDING_MODEL_ID,
            vector_store_path=config.VECTOR_STORE_PATH,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN
        )
        logger.info("✅ Vector Store inicializado")
        
        # Bedrock Agent com credenciais explícitas
        logger.info("Inicializando Bedrock Agent...")
        from src.bedrock_agent_aws_cli import BedrockAgentAWSCLI
        agent_instructions_path = os.path.join(
            config.PROMPTS_PATH, 
            config.AGENT_INSTRUCTIONS_FILE
        )
        
        bedrock_agent = BedrockAgentAWSCLI(
            aws_region=config.AWS_REGION,
            model_id=config.BEDROCK_MODEL_ID,
            agent_instructions_path=agent_instructions_path,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            aws_session_token=config.AWS_SESSION_TOKEN
        )
        logger.info("✅ Bedrock Agent inicializado")
        
        logger.info("🚀 Todos os componentes inicializados com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao inicializar componentes: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        if "ExpiredToken" in str(e):
            logger.error("💡 Token AWS expirado - Execute: aws sso login")
        elif "AccessDenied" in str(e):
            logger.error("💡 Sem acesso ao Bedrock - Habilite modelos no Console AWS")
        
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    creds = config.get_aws_credentials()
    return jsonify({
        'status': 'healthy',
        'components': {
            'document_processor': document_processor is not None,
            'vector_store': vector_store is not None,
            'bedrock_agent': bedrock_agent is not None
        },
        'aws_credentials': {
            'region': creds['region'],
            'access_key_set': creds['access_key_set'],
            'secret_key_set': creds['secret_key_set'],
            'session_token_set': creds['session_token_set']
        }
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Retorna status detalhado do sistema"""
    try:
        creds = config.get_aws_credentials()
        
        return jsonify({
            'status': 'running',
            'components': {
                'document_processor': document_processor is not None,
                'vector_store': vector_store is not None,
                'bedrock_agent': bedrock_agent is not None
            },
            'config': {
                'aws_region': config.AWS_REGION,
                'model_id': config.BEDROCK_MODEL_ID,
                'embedding_model': config.BEDROCK_EMBEDDING_MODEL_ID,
                'documents_path': config.DOCUMENTS_PATH,
                'vector_store_path': config.VECTOR_STORE_PATH
            },
            'aws_credentials': creds,
            'initialized': all([document_processor, vector_store, bedrock_agent])
        })
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/documents/upload', methods=['POST'])
def process_documents():
    """Processa documentos - MÉTODO CORRIGIDO"""
    try:
        if not all([document_processor, vector_store]):
            return jsonify({
                'success': False,
                'error': 'Componentes não inicializados'
            }), 500
        
        # Processar documentos - CORREÇÃO AQUI
        logger.info(f"Processando documentos do diretório: {config.DOCUMENTS_PATH}")
        documents = document_processor.process_documents_directory(config.DOCUMENTS_PATH)  # ✅ CORRIGIDO
        
        logger.info(f"Documentos processados: {len(documents)}")
        for i, doc in enumerate(documents):
            logger.info(f"  {i+1}. {doc.metadata.get('source', 'N/A')} - {len(doc.page_content)} chars")
        
        # Adicionar ao vector store
        vector_store.add_documents(documents)
        
        return jsonify({
            'success': True,
            'documents_processed': len(documents),
            'message': f'Processados {len(documents)} documentos com embeddings reais',
            'documents': [
                {
                    'source': doc.metadata.get('source', 'N/A'),
                    'chunks': 1,
                    'content_preview': doc.page_content[:100] + '...' if len(doc.page_content) > 100 else doc.page_content
                } for doc in documents[:5]  # Mostrar apenas os primeiros 5
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar documentos: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Chat com o agente"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Mensagem é obrigatória'
            }), 400
        
        if not all([bedrock_agent, vector_store]):
            return jsonify({
                'success': False,
                'error': 'Componentes não inicializados'
            }), 500
        
        user_message = data['message']
        max_results = data.get('max_results', config.MAX_SEARCH_RESULTS)
        
        logger.info(f"Chat request: {user_message}")
        
        # Buscar documentos relevantes
        relevant_documents = vector_store.similarity_search(
            user_message, 
            k=max_results
        )
        
        logger.info(f"Documentos relevantes encontrados: {len(relevant_documents)}")
        for i, doc in enumerate(relevant_documents):
            logger.info(f"  {i+1}. {doc.get('metadata', {}).get('source', 'N/A')} - Similaridade: {doc.get('similarity', 0):.3f}")
        
        # Processar com Bedrock
        result = bedrock_agent.process_message(user_message, relevant_documents)
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'sources': result.get('sources', []),
            'metadata': result.get('metadata', {}),
            'relevant_documents_count': len(relevant_documents)
        })
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint não encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500

def main():
    """Função principal"""
    logger.info("🚀 Iniciando aplicação com credenciais AWS CLI...")
    
    # Inicializar componentes
    if not initialize_components():
        logger.error("❌ Falha na inicialização do sistema")
        logger.error("💡 Verifique credenciais AWS e acesso ao Bedrock")
        return False
    
    # Iniciar servidor
    try:
        logger.info(f"🌐 Servidor iniciando em http://{config.FLASK_HOST}:{config.FLASK_PORT}")
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )
        return True
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
