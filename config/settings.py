import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    BEDROCK_EMBEDDING_MODEL_ID = os.getenv('BEDROCK_EMBEDDING_MODEL_ID', 'amazon.titan-embed-text-v1')
    
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
