#!/usr/bin/env python3
"""
App principal que usa IAM Role (credenciais automáticas da EC2)
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

from config.settings import Config as config
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
bedrock_available = False

def check_aws_credentials():
    """Verifica credenciais AWS (IAM Role)"""
    logger.info("🔍 Verificando credenciais AWS (IAM Role)...")
    
    try:
        # Usar credenciais padrão (IAM Role da EC2)
        sts_client = boto3.client('sts', region_name=config.AWS_REGION)
        identity = sts_client.get_caller_identity()
        
        logger.info(f"✅ Credenciais válidas via IAM Role")
        logger.info(f"   Account: {identity.get('Account')}")
        logger.info(f"   User: {identity.get('Arn')}")
        logger.info(f"   Region: {config.AWS_REGION}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao validar credenciais: {e}")
        return False

def test_bedrock_access():
    """Testa acesso ao Bedrock"""
    try:
        logger.info("🧪 Testando acesso ao Bedrock...")
        
        # Testar listagem de modelos
        bedrock_client = boto3.client('bedrock', region_name=config.AWS_REGION)
        models = bedrock_client.list_foundation_models()
        
        model_count = len(models['modelSummaries'])
        logger.info(f"✅ Acesso ao Bedrock OK - {model_count} modelos disponíveis")
        
        # Verificar modelos específicos
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        titan_models = [m for m in models['modelSummaries'] if 'titan' in m['modelId'].lower()]
        
        logger.info(f"   🤖 Modelos Claude: {len(claude_models)}")
        logger.info(f"   🔗 Modelos Titan: {len(titan_models)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no Bedrock: {e}")
        if "AccessDenied" in str(e):
            logger.error("💡 IAM Role não tem permissões para Bedrock")
        return False

def initialize_components():
    """Inicializa componentes do sistema"""
    global document_processor, vector_store, bedrock_agent, bedrock_available
    
    try:
        logger.info("Inicializando componentes do sistema...")
        
        # Verificar credenciais AWS
        if not check_aws_credentials():
            logger.error("❌ Credenciais AWS inválidas")
            return False
        
        # Document Processor (sempre funciona)
        document_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        logger.info("✅ Document Processor inicializado")
        
        # Testar acesso ao Bedrock
        if test_bedrock_access():
            try:
                # Vector Store
                logger.info("Inicializando Vector Store...")
                from src.vector_store import VectorStore
                vector_store = VectorStore(
                    aws_region=config.AWS_REGION,
                    embedding_model_id=config.BEDROCK_EMBEDDING_MODEL_ID,
                    vector_store_path=config.VECTOR_STORE_PATH
                )
                logger.info("✅ Vector Store inicializado")
                
                # Bedrock Agent
                logger.info("Inicializando Bedrock Agent...")
                from src.bedrock_agent import BedrockAgent
                agent_instructions_path = os.path.join(
                    config.PROMPTS_PATH, 
                    config.AGENT_INSTRUCTIONS_FILE
                )
                
                bedrock_agent = BedrockAgent(
                    aws_region=config.AWS_REGION,
                    model_id=config.BEDROCK_MODEL_ID,
                    agent_instructions_path=agent_instructions_path
                )
                logger.info("✅ Bedrock Agent inicializado")
                
                bedrock_available = True
                logger.info("🚀 Modo Bedrock ativado - IA real disponível")
                
            except Exception as bedrock_error:
                logger.warning(f"⚠️  Erro ao inicializar Bedrock: {bedrock_error}")
                if "AccessDenied" in str(bedrock_error):
                    logger.warning("💡 Modelos Bedrock não habilitados ou sem permissão")
                elif "ExpiredToken" in str(bedrock_error):
                    logger.warning("💡 Token AWS expirado")
                
                bedrock_available = False
                logger.info("🎭 Continuando em modo demo")
        else:
            bedrock_available = False
            logger.info("🎭 Bedrock não disponível - modo demo ativo")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao inicializar componentes: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'healthy',
        'bedrock_available': bedrock_available,
        'mode': 'bedrock' if bedrock_available else 'demo',
        'components': {
            'document_processor': document_processor is not None,
            'vector_store': vector_store is not None,
            'bedrock_agent': bedrock_agent is not None
        },
        'aws_region': config.AWS_REGION
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Retorna status detalhado do sistema"""
    try:
        # Obter informações da identidade AWS
        try:
            sts_client = boto3.client('sts', region_name=config.AWS_REGION)
            identity = sts_client.get_caller_identity()
            aws_info = {
                'account': identity.get('Account'),
                'user_arn': identity.get('Arn'),
                'region': config.AWS_REGION
            }
        except:
            aws_info = {'error': 'Não foi possível obter informações AWS'}
        
        return jsonify({
            'status': 'running',
            'mode': 'bedrock' if bedrock_available else 'demo',
            'bedrock_available': bedrock_available,
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
            'aws_info': aws_info,
            'message': 'IA real ativa' if bedrock_available else 'Modo demonstração - Bedrock não disponível'
        })
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/documents/upload', methods=['POST'])
def process_documents():
    """Processa documentos"""
    try:
        if not document_processor:
            return jsonify({
                'success': False,
                'error': 'Document processor não inicializado'
            }), 500
        
        # Processar documentos
        documents = document_processor.process_documents_directory(config.DOCUMENTS_PATH)
        
        if bedrock_available and vector_store:
            # Modo Bedrock - processamento real
            vector_store.add_documents(documents)
            message = f"Processados {len(documents)} documentos com embeddings reais"
        else:
            # Modo demo - simulação
            message = f"Simulação: {len(documents)} documentos encontrados (Bedrock não disponível)"
        
        return jsonify({
            'success': True,
            'documents_processed': len(documents),
            'mode': 'bedrock' if bedrock_available else 'demo',
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar documentos: {e}")
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
        
        user_message = data['message']
        max_results = data.get('max_results', config.MAX_SEARCH_RESULTS)
        
        if bedrock_available and bedrock_agent and vector_store:
            # Modo Bedrock - IA real
            try:
                # Buscar documentos relevantes
                relevant_documents = vector_store.similarity_search(
                    user_message, 
                    k=max_results
                )
                
                # Processar com Bedrock
                result = bedrock_agent.process_message(user_message, relevant_documents)
                
                return jsonify({
                    'success': True,
                    'mode': 'bedrock',
                    'response': result['response'],
                    'sources': result.get('sources', []),
                    'metadata': result.get('metadata', {})
                })
                
            except Exception as bedrock_error:
                logger.error(f"Erro no Bedrock: {bedrock_error}")
                # Fallback para modo demo se Bedrock falhar
                pass
        
        # Modo demo - resposta simulada
        demo_response = f"""
🤖 **Modo Demonstração**

Você perguntou: "{user_message}"

Esta é uma resposta simulada. O Bedrock não está disponível devido a:

**Possíveis causas:**
- Modelos não habilitados no Console AWS
- IAM Role sem permissões para Bedrock
- Região não suporta Bedrock

**Para ativar IA real:**
1. Console AWS → Bedrock → Model Access
2. Habilitar Claude 3 Sonnet e Titan Embeddings
3. Verificar permissões IAM da EC2

**Status:** {'Bedrock não disponível' if not bedrock_available else 'Erro temporário do Bedrock'}
        """.strip()
        
        return jsonify({
            'success': True,
            'mode': 'demo',
            'response': demo_response,
            'sources': [
                {
                    'document': 'demo_source.txt',
                    'content': 'Exemplo de fonte de documento',
                    'similarity': 0.85
                }
            ],
            'metadata': {
                'model': 'demo_mode',
                'bedrock_available': bedrock_available
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
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
    logger.info("🚀 Iniciando aplicação com IAM Role...")
    
    # Inicializar componentes
    if not initialize_components():
        logger.error("❌ Falha na inicialização do sistema")
        return False
    
    # Mostrar status
    if bedrock_available:
        logger.info("🚀 Sistema iniciado em modo Bedrock (IA real)")
    else:
        logger.info("🎭 Sistema iniciado em modo demo (Bedrock não disponível)")
        logger.info("💡 Para ativar IA real:")
        logger.info("   1. Console AWS → Bedrock → Model Access")
        logger.info("   2. Habilitar modelos Claude 3 e Titan")
        logger.info("   3. Verificar permissões IAM")
    
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
