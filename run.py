#!/usr/bin/env python3
"""
Script principal para executar o Agente de Documentos Bedrock
"""

import os
import sys
import logging

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app_aws_cli import app, initialize_components, config

def main():
    """Função principal"""
    print("=" * 60)
    print("🤖 AGENTE DE DOCUMENTOS BEDROCK")
    print("=" * 60)
    
    # Configuração de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Verifica se o arquivo .env existe
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(env_file):
            logger.warning("Arquivo .env não encontrado. Usando configurações padrão.")
            logger.info("Copie .env.example para .env e configure suas credenciais AWS.")
        
        # Inicializa componentes
        logger.info("Inicializando sistema...")
        if not initialize_components():
            logger.error("❌ Falha na inicialização do sistema")
            return 1
        
        logger.info("✅ Sistema inicializado com sucesso")
        
        # Informações do sistema
        print(f"\n📊 CONFIGURAÇÕES:")
        print(f"   • Região AWS: {config.AWS_REGION}")
        print(f"   • Modelo Bedrock: {config.BEDROCK_MODEL_ID}")
        print(f"   • Modelo Embedding: {config.BEDROCK_EMBEDDING_MODEL_ID}")
        print(f"   • Diretório de Documentos: {config.DOCUMENTS_PATH}")
        print(f"   • Host: {config.FLASK_HOST}:{config.FLASK_PORT}")
        
        print(f"\n🚀 ENDPOINTS DISPONÍVEIS:")
        print(f"   • POST /chat - Chat com o agente")
        print(f"   • POST /documents/upload - Reprocessar documentos")
        print(f"   • GET /status - Status do sistema")
        print(f"   • GET /health - Health check")
        
        print(f"\n📁 Para usar o sistema:")
        print(f"   1. Coloque seus documentos PDF/Word em: {config.DOCUMENTS_PATH}")
        print(f"   2. Faça POST para /documents/upload para processar")
        print(f"   3. Use POST para /chat para conversar com o agente")
        
        print(f"\n🌐 Servidor iniciando em http://{config.FLASK_HOST}:{config.FLASK_PORT}")
        print("=" * 60)
        
        # Inicia servidor
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n👋 Servidor interrompido pelo usuário")
        return 0
    except Exception as e:
        logger.error(f"❌ Erro fatal: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
