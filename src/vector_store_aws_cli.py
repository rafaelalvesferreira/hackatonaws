import os
import pickle
import logging
from typing import List, Dict, Tuple
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStoreAWSCLI:
    def __init__(self, aws_region: str, embedding_model_id: str, vector_store_path: str,
                 aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str):
        self.aws_region = aws_region
        self.embedding_model_id = embedding_model_id
        self.vector_store_path = vector_store_path
        self.vector_store = None
        
        # Inicializa cliente Bedrock com credenciais explícitas
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )
        
        # Inicializa embeddings
        self.embeddings = BedrockEmbeddings(
            client=self.bedrock_client,
            model_id=embedding_model_id
        )
        
        # Carrega ou cria vector store
        self._load_or_create_vector_store()
    
    def _load_or_create_vector_store(self):
        """Carrega vector store existente ou cria um novo"""
        try:
            if os.path.exists(self.vector_store_path):
                logger.info("Carregando vector store existente...")
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("✅ Vector store carregado com sucesso")
            else:
                logger.info("Criando novo vector store...")
                # Criar documento dummy para inicializar
                dummy_doc = Document(
                    page_content="Documento inicial para inicialização do vector store.",
                    metadata={"source": "init", "type": "dummy"}
                )
                
                

                self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
                
                # Criar diretório se não existir
                os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
                
                # Salvar vector store
                self.vector_store.save_local(self.vector_store_path)
                logger.info("✅ Novo vector store criado e salvo")
                
        except Exception as e:
            logger.error(f"Erro ao carregar/criar vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]):
        """Adiciona documentos ao vector store"""
        try:
            if not documents:
                logger.warning("Nenhum documento para adicionar")
                return
            
            logger.info(f"Adicionando {len(documents)} documentos ao vector store...")
            
            # Adicionar documentos
            self.vector_store.add_documents(documents)
            
            # Salvar vector store atualizado
            self.vector_store.save_local(self.vector_store_path)
            
            logger.info(f"✅ {len(documents)} documentos adicionados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 5, similarity_threshold: float = 0.7) -> List[Dict]:
        """Busca documentos similares"""
        try:
            if not self.vector_store:
                logger.error("Vector store não inicializado")
                return []
            
            # Buscar documentos similares com scores
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Filtrar por threshold e formatar resultado
            results = []
            for doc, score in docs_with_scores:
                # FAISS retorna distância (menor = mais similar)
                # Converter para similaridade (maior = mais similar)
                similarity = 1 / (1 + score)
                
                if similarity >= similarity_threshold:
                    results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'similarity': similarity
                    })
            
            logger.info(f"Encontrados {len(results)} documentos relevantes")
            return results
            
        except Exception as e:
            logger.error(f"Erro na busca por similaridade: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do vector store"""
        try:
            if not self.vector_store:
                return {'error': 'Vector store não inicializado'}
            
            # Obter número de documentos
            index_size = self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') else 0
            
            return {
                'documents_count': index_size,
                'embedding_model': self.embedding_model_id,
                'vector_store_path': self.vector_store_path,
                'aws_region': self.aws_region
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {'error': str(e)}
