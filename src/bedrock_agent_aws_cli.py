import os
import json
import logging
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockAgentAWSCLI:
    def __init__(self, aws_region: str, model_id: str, agent_instructions_path: str,
                 aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
        self.aws_region = aws_region
        self.model_id = model_id
        self.agent_instructions_path = agent_instructions_path
        
        # Inicializa cliente Bedrock com credenciais explícitas
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        
        # Carrega instruções do agente
        self.agent_instructions = self._load_agent_instructions()
    
    def _load_agent_instructions(self) -> str:
        """Carrega instruções do agente"""
        try:
            if os.path.exists(self.agent_instructions_path):
                with open(self.agent_instructions_path, 'r', encoding='utf-8') as f:
                    instructions = f.read().strip()
                logger.info("✅ Instruções do agente carregadas")
                return instructions
            else:
                # Instruções padrão se arquivo não existir
                default_instructions = """
Você é um assistente especializado em análise de documentos. 

Suas responsabilidades:
1. Analisar documentos fornecidos pelo usuário
2. Responder perguntas baseadas no conteúdo dos documentos
3. Citar fontes específicas quando possível
4. Ser preciso e objetivo nas respostas

Sempre baseie suas respostas no conteúdo dos documentos fornecidos.
                """.strip()
                
                logger.warning(f"Arquivo de instruções não encontrado: {self.agent_instructions_path}")
                logger.info("Usando instruções padrão")
                return default_instructions
                
        except Exception as e:
            logger.error(f"Erro ao carregar instruções: {e}")
            return "Você é um assistente de análise de documentos."
    
    def _call_bedrock_model(self, prompt: str) -> str:
        """Chama o modelo Bedrock"""
        try:
            # Preparar body para Claude 3
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            # Chamar modelo
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType='application/json',
                accept='application/json'
            )
            
            # Processar resposta
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                logger.error("Resposta do modelo não contém conteúdo esperado")
                return "Erro: Resposta inválida do modelo"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Erro do Bedrock ({error_code}): {error_message}")
            
            if error_code == 'AccessDeniedException':
                return "Erro: Sem acesso ao modelo Bedrock. Verifique permissões."
            elif error_code == 'ValidationException':
                return "Erro: Parâmetros inválidos para o modelo."
            else:
                return f"Erro do Bedrock: {error_message}"
                
        except Exception as e:
            logger.error(f"Erro inesperado ao chamar Bedrock: {e}")
            return f"Erro inesperado: {str(e)}"
    
    def process_message(self, user_message: str, relevant_documents: List[Dict]) -> Dict[str, Any]:
        """Processa mensagem do usuário com documentos relevantes"""
        try:
            # Construir contexto dos documentos
            context = ""
            sources = []
            
            if relevant_documents:
                context = "\n\nDocumentos relevantes:\n"
                for i, doc in enumerate(relevant_documents, 1):
                    context += f"\n--- Documento {i} ---\n"
                    context += doc['content']
                    context += f"\n(Fonte: {doc['metadata'].get('source', 'Desconhecida')})\n"
                    
                    # Adicionar à lista de fontes
                    sources.append({
                        'document': doc['metadata'].get('source', 'Desconhecida'),
                        'content': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
                        'similarity': doc.get('similarity', 0.0)
                    })
            
            # Construir prompt completo
            prompt = f"""
{self.agent_instructions}

{context}

Pergunta do usuário: {user_message}

Por favor, responda baseado nos documentos fornecidos. Se não houver documentos relevantes, informe que não há informações suficientes.
            """.strip()
            
            # Chamar modelo
            response = self._call_bedrock_model(prompt)
            
            return {
                'response': response,
                'sources': sources,
                'metadata': {
                    'model': self.model_id,
                    'documents_used': len(relevant_documents),
                    'prompt_length': len(prompt)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return {
                'response': f"Erro ao processar mensagem: {str(e)}",
                'sources': [],
                'metadata': {'error': str(e)}
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Retorna informações do agente"""
        return {
            'model_id': self.model_id,
            'aws_region': self.aws_region,
            'instructions_loaded': bool(self.agent_instructions),
            'instructions_length': len(self.agent_instructions) if self.agent_instructions else 0
        }
