import os
from dotenv import load_dotenv

# Carregar .env primeiro (fallback)
load_dotenv()

class Config:
    # AWS Configuration - Prioriza variáveis de ambiente da AWS CLI
    AWS_REGION = (
        os.getenv('AWS_DEFAULT_REGION') or  # AWS CLI padrão
        os.getenv('AWS_REGION') or          # Variável comum
        'us-east-1'                         # Fallback
    )
    
    # Credenciais AWS - Prioriza variáveis de ambiente da CLI
    AWS_ACCESS_KEY_ID = (
        os.getenv('AWS_ACCESS_KEY_ID') or   # Variável padrão AWS
        os.getenv('ACCESS_KEY_ID')          # Fallback
    )
    
    AWS_SECRET_ACCESS_KEY = (
        os.getenv('AWS_SECRET_ACCESS_KEY') or  # Variável padrão AWS
        os.getenv('SECRET_ACCESS_KEY')         # Fallback
    )
    
    AWS_SESSION_TOKEN = (
        os.getenv('AWS_SESSION_TOKEN') or   # Variável padrão AWS
        os.getenv('SESSION_TOKEN')          # Fallback
    )
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    # BEDROCK_EMBEDDING_MODEL_ID = os.getenv('BEDROCK_EMBEDDING_MODEL_ID', 'amazon.titan-embed-text-v2')
    BEDROCK_EMBEDDING_MODEL_ID = os.getenv('BEDROCK_EMBEDDING_MODEL_ID', 'amazon.titan-embed-text-v2:0')
    
    # Flask Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Document Processing
    DOCUMENTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'documents')
    VECTOR_STORE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vector_store')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    
    # Search Configuration
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 5))
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))
    
    # Prompt Configuration
    PROMPTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
    AGENT_INSTRUCTIONS_FILE = 'agent_instructions.txt'
    
    @classmethod
    def get_aws_credentials(cls):
        """Retorna credenciais AWS formatadas para debug"""
        return {
            'region': cls.AWS_REGION,
            'access_key_set': bool(cls.AWS_ACCESS_KEY_ID),
            'secret_key_set': bool(cls.AWS_SECRET_ACCESS_KEY),
            'session_token_set': bool(cls.AWS_SESSION_TOKEN),
            'access_key_preview': cls.AWS_ACCESS_KEY_ID[:10] + '...' if cls.AWS_ACCESS_KEY_ID else 'NOT_SET'
        }
    
    @classmethod
    def validate_aws_credentials(cls):
        """Valida se as credenciais AWS estão completas"""
        missing = []
        
        if not cls.AWS_ACCESS_KEY_ID:
            missing.append('AWS_ACCESS_KEY_ID')
        if not cls.AWS_SECRET_ACCESS_KEY:
            missing.append('AWS_SECRET_ACCESS_KEY')
        if not cls.AWS_SESSION_TOKEN:
            missing.append('AWS_SESSION_TOKEN')
            
        return len(missing) == 0, missing
