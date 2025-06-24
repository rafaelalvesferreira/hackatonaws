import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# Adiciona o diretório raiz ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.settings import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.bedrock_agent import BedrockAgent

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app)

# Configuração
config = Config()

# Inicialização dos componentes
document_processor = None
vector_store = None
bedrock_agent = None

def initialize_components():
    """Inicializa todos os componentes do sistema"""
    global document_processor, vector_store, bedrock_agent
    
    try:
        logger.info("Inicializando componentes do sistema...")
        
        # Document Processor
        document_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        # Vector Store
        vector_store = VectorStore(
            aws_region=config.AWS_REGION,
            embedding_model_id=config.BEDROCK_EMBEDDING_MODEL_ID,
            vector_store_path=config.VECTOR_STORE_PATH
        )
        
        # Bedrock Agent
        agent_instructions_path = os.path.join(
            config.PROMPTS_PATH, 
            config.AGENT_INSTRUCTIONS_FILE
        )
        bedrock_agent = BedrockAgent(
            aws_region=config.AWS_REGION,
            model_id=config.BEDROCK_MODEL_ID,
            agent_instructions_path=agent_instructions_path
        )
        
        logger.info("Componentes inicializados com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao inicializar componentes: {str(e)}")
        logger.error(traceback.format_exc())
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    try:
        # Verifica se os componentes estão inicializados
        components_status = {
            "document_processor": document_processor is not None,
            "vector_store": vector_store is not None,
            "bedrock_agent": bedrock_agent is not None
        }
        
        all_healthy = all(components_status.values())
        
        return jsonify({
            "status": "healthy" if all_healthy else "unhealthy",
            "components": components_status,
            "timestamp": "2025-06-24T17:00:00Z"
        }), 200 if all_healthy else 503
        
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal para chat com o agente"""
    try:
        # Verifica se os componentes estão inicializados
        if not all([document_processor, vector_store, bedrock_agent]):
            return jsonify({
                "success": False,
                "error": "Sistema não inicializado corretamente"
            }), 500
        
        # Obtém dados da requisição
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Campo 'message' é obrigatório"
            }), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Mensagem não pode estar vazia"
            }), 400
        
        # Parâmetros opcionais
        max_results = data.get('max_results', config.MAX_SEARCH_RESULTS)
        similarity_threshold = data.get('similarity_threshold', config.SIMILARITY_THRESHOLD)
        
        logger.info(f"Processando mensagem: {user_message[:100]}...")
        
        # Busca documentos relevantes
        relevant_documents = vector_store.search_similar_documents(
            query=user_message,
            k=max_results,
            score_threshold=similarity_threshold
        )
        
        # Processa mensagem com o agente
        result = bedrock_agent.process_message(user_message, relevant_documents)
        
        # Adiciona informações extras à resposta
        result['search_results_count'] = len(relevant_documents)
        result['timestamp'] = "2025-06-24T17:00:00Z"
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        logger.error(f"Erro no endpoint chat: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@app.route('/documents/upload', methods=['POST'])
def upload_documents():
    """Endpoint para reprocessar documentos"""
    try:
        if not all([document_processor, vector_store]):
            return jsonify({
                "success": False,
                "error": "Sistema não inicializado corretamente"
            }), 500
        
        logger.info("Iniciando reprocessamento de documentos...")
        
        # Processa documentos do diretório
        documents = document_processor.process_documents_directory(config.DOCUMENTS_PATH)
        
        if not documents:
            return jsonify({
                "success": False,
                "error": "Nenhum documento encontrado ou processado",
                "documents_path": config.DOCUMENTS_PATH
            }), 400
        
        # Limpa vector store existente
        vector_store.clear_vector_store()
        
        # Adiciona novos documentos
        vector_store.add_documents(documents)
        
        # Salva vector store
        vector_store.save_vector_store()
        
        logger.info(f"Reprocessamento concluído: {len(documents)} chunks")
        
        return jsonify({
            "success": True,
            "message": "Documentos reprocessados com sucesso",
            "documents_processed": len(documents),
            "documents_path": config.DOCUMENTS_PATH
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no upload de documentos: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Erro ao processar documentos: {str(e)}"
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint para obter status detalhado do sistema"""
    try:
        status = {
            "system": {
                "initialized": all([document_processor, vector_store, bedrock_agent]),
                "documents_path": config.DOCUMENTS_PATH,
                "vector_store_path": config.VECTOR_STORE_PATH
            }
        }
        
        if vector_store:
            status["vector_store"] = vector_store.get_vector_store_info()
        
        if bedrock_agent:
            status["agent"] = bedrock_agent.get_agent_info()
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint não encontrado"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Erro interno do servidor"
    }), 500

if __name__ == '__main__':
    # Inicializa componentes
    if not initialize_components():
        logger.error("Falha na inicialização. Encerrando aplicação.")
        sys.exit(1)
    
    # Inicia servidor Flask
    logger.info(f"Iniciando servidor Flask em {config.FLASK_HOST}:{config.FLASK_PORT}")
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
