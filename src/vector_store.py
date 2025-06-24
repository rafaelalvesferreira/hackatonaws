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

class VectorStore:
    def __init__(self, aws_region: str, embedding_model_id: str, vector_store_path: str):
        self.aws_region = aws_region
        self.embedding_model_id = embedding_model_id
        self.vector_store_path = vector_store_path
        self.vector_store = None
        
        # Inicializa cliente Bedrock
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
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
                logger.info("Vector store carregado com sucesso")
            else:
                logger.info("Criando novo vector store...")
                # Cria um vector store vazio
                dummy_doc = Document(page_content="dummy", metadata={})
                self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
                # Remove o documento dummy
                self.vector_store.delete([0])
                logger.info("Novo vector store criado")
        except Exception as e:
            logger.error(f"Erro ao carregar/criar vector store: {str(e)}")
            # Cria um novo em caso de erro
            dummy_doc = Document(page_content="dummy", metadata={})
            self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
    
    def add_documents(self, documents: List[Document]):
        """Adiciona documentos ao vector store"""
        if not documents:
            logger.warning("Nenhum documento para adicionar")
            return
        
        try:
            logger.info(f"Adicionando {len(documents)} documentos ao vector store...")
            
            if self.vector_store is None:
                # Cria novo vector store se não existir
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                # Adiciona ao vector store existente
                self.vector_store.add_documents(documents)
            
            logger.info("Documentos adicionados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {str(e)}")
            raise
    
    def save_vector_store(self):
        """Salva o vector store no disco"""
        try:
            if self.vector_store is not None:
                os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
                self.vector_store.save_local(self.vector_store_path)
                logger.info(f"Vector store salvo em {self.vector_store_path}")
            else:
                logger.warning("Nenhum vector store para salvar")
        except Exception as e:
            logger.error(f"Erro ao salvar vector store: {str(e)}")
            raise
    
    def search_similar_documents(self, query: str, k: int = 5, score_threshold: float = 0.7) -> List[Tuple[Document, float]]:
        """Busca documentos similares à query"""
        if self.vector_store is None:
            logger.warning("Vector store não inicializado")
            return []
        
        try:
            # Busca com score
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Filtra por threshold de similaridade
            filtered_results = [
                (doc, score) for doc, score in results 
                if score <= (1.0 - score_threshold)  # FAISS usa distância, não similaridade
            ]
            
            logger.info(f"Encontrados {len(filtered_results)} documentos relevantes para a query")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            return []
    
    def get_vector_store_info(self) -> Dict:
        """Retorna informações sobre o vector store"""
        if self.vector_store is None:
            return {"status": "not_initialized", "document_count": 0}
        
        try:
            # FAISS não tem método direto para contar documentos
            # Vamos usar uma aproximação baseada no índice
            index_size = self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') else 0
            
            return {
                "status": "initialized",
                "document_count": index_size,
                "embedding_model": self.embedding_model_id
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações do vector store: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def clear_vector_store(self):
        """Limpa o vector store"""
        try:
            if os.path.exists(self.vector_store_path):
                import shutil
                shutil.rmtree(self.vector_store_path)
                logger.info("Vector store limpo")
            
            # Recria vector store vazio
            self._load_or_create_vector_store()
            
        except Exception as e:
            logger.error(f"Erro ao limpar vector store: {str(e)}")
            raise
