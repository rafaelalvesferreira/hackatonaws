import os
import json
import logging
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockAgent:
    def __init__(self, aws_region: str, model_id: str, agent_instructions_path: str):
        self.aws_region = aws_region
        self.model_id = model_id
        self.agent_instructions_path = agent_instructions_path
        
        # Inicializa cliente Bedrock
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )
        
        # Carrega instruções do agente
        self.agent_instructions = self._load_agent_instructions()
    
    def _load_agent_instructions(self) -> str:
        """Carrega as instruções do agente do arquivo"""
        try:
            with open(self.agent_instructions_path, 'r', encoding='utf-8') as file:
                instructions = file.read()
                logger.info("Instruções do agente carregadas com sucesso")
                return instructions
        except Exception as e:
            logger.error(f"Erro ao carregar instruções do agente: {str(e)}")
            return "Você é um assistente útil especializado em análise de documentos."
    
    def _format_context_from_documents(self, documents_with_scores: List[tuple]) -> str:
        """Formata o contexto a partir dos documentos encontrados"""
        if not documents_with_scores:
            return "Nenhum documento relevante encontrado."
        
        context_parts = []
        context_parts.append("=== CONTEXTO DOS DOCUMENTOS ===\n")
        
        for i, (doc, score) in enumerate(documents_with_scores, 1):
            source = doc.metadata.get('source', 'Documento desconhecido')
            chunk_id = doc.metadata.get('chunk_id', 'N/A')
            
            context_parts.append(f"[DOCUMENTO {i}]")
            context_parts.append(f"Fonte: {source}")
            context_parts.append(f"Chunk: {chunk_id}")
            context_parts.append(f"Relevância: {1-score:.2f}")
            context_parts.append(f"Conteúdo:\n{doc.page_content}")
            context_parts.append("-" * 50)
        
        return "\n".join(context_parts)
    
    def _build_prompt(self, user_message: str, context: str) -> str:
        """Constrói o prompt completo para o modelo"""
        prompt = f"""
{self.agent_instructions}

{context}

=== PERGUNTA DO USUÁRIO ===
{user_message}

=== INSTRUÇÕES ESPECÍFICAS ===
- Base sua resposta exclusivamente nas informações fornecidas no contexto dos documentos
- Cite sempre as fontes (nome dos arquivos) quando referenciar informações
- Se não encontrar informações relevantes no contexto, seja transparente sobre isso
- Estruture sua resposta de forma clara e organizada
- Mantenha um tom profissional e prestativo

Resposta:"""
        
        return prompt
    
    def _call_bedrock_model(self, prompt: str) -> str:
        """Chama o modelo Bedrock com o prompt"""
        try:
            # Configuração específica para Claude
            if "claude" in self.model_id.lower():
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            else:
                # Configuração genérica para outros modelos
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 4000,
                        "temperature": 0.1,
                        "topP": 0.9
                    }
                }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extrai resposta baseada no modelo
            if "claude" in self.model_id.lower():
                return response_body['content'][0]['text']
            else:
                return response_body.get('results', [{}])[0].get('outputText', '')
                
        except ClientError as e:
            logger.error(f"Erro do cliente AWS: {str(e)}")
            return f"Erro ao processar sua solicitação: {str(e)}"
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return f"Erro inesperado: {str(e)}"
    
    def process_message(self, user_message: str, relevant_documents: List[tuple]) -> Dict[str, Any]:
        """Processa uma mensagem do usuário com contexto de documentos"""
        try:
            # Formata contexto dos documentos
            context = self._format_context_from_documents(relevant_documents)
            
            # Constrói prompt completo
            prompt = self._build_prompt(user_message, context)
            
            # Chama modelo Bedrock
            response = self._call_bedrock_model(prompt)
            
            # Prepara metadados da resposta
            sources = list(set([
                doc.metadata.get('source', 'Desconhecido') 
                for doc, _ in relevant_documents
            ]))
            
            return {
                "success": True,
                "response": response,
                "sources": sources,
                "documents_used": len(relevant_documents),
                "model_id": self.model_id
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": "Desculpe, ocorreu um erro ao processar sua solicitação."
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o agente"""
        return {
            "model_id": self.model_id,
            "aws_region": self.aws_region,
            "instructions_loaded": bool(self.agent_instructions),
            "instructions_length": len(self.agent_instructions) if self.agent_instructions else 0
        }
