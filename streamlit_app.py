import streamlit as st
import requests
import json
import os
import time
from datetime import datetime
import pandas as pd

# Configurações da página
st.set_page_config(
    page_title="🤖 Agente de Documentos Bedrock",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URLs da API
API_BASE_URL = "http://localhost:5000"

# Caminhos dos arquivos
PROMPTS_PATH = "prompts"
AGENT_INSTRUCTIONS_FILE = "agent_instructions.txt"
DOCUMENTS_PATH = "documents"

def load_agent_instructions():
    """Carrega as instruções do agente"""
    try:
        instructions_path = os.path.join(PROMPTS_PATH, AGENT_INSTRUCTIONS_FILE)
        with open(instructions_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        st.error(f"Erro ao carregar instruções: {str(e)}")
        return ""

def save_agent_instructions(content):
    """Salva as instruções do agente"""
    try:
        instructions_path = os.path.join(PROMPTS_PATH, AGENT_INSTRUCTIONS_FILE)
        with open(instructions_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar instruções: {str(e)}")
        return False

def call_api(endpoint, method="GET", data=None):
    """Chama a API do agente"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return None, {"error": "Não foi possível conectar à API. Certifique-se de que o servidor está rodando."}
    except requests.exceptions.Timeout:
        return None, {"error": "Timeout na requisição. Tente novamente."}
    except Exception as e:
        return None, {"error": f"Erro inesperado: {str(e)}"}

def list_documents():
    """Lista documentos no diretório"""
    try:
        if os.path.exists(DOCUMENTS_PATH):
            files = []
            for filename in os.listdir(DOCUMENTS_PATH):
                if filename.lower().endswith(('.pdf', '.docx', '.doc')):
                    filepath = os.path.join(DOCUMENTS_PATH, filename)
                    size = os.path.getsize(filepath)
                    modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    files.append({
                        'Nome': filename,
                        'Tamanho (KB)': round(size / 1024, 2),
                        'Modificado': modified.strftime('%d/%m/%Y %H:%M')
                    })
            return files
        return []
    except Exception as e:
        st.error(f"Erro ao listar documentos: {str(e)}")
        return []

# Interface principal
def main():
    st.title("🤖 Agente de Documentos Bedrock - Interface de Teste")
    st.markdown("---")
    
    # Sidebar para navegação
    st.sidebar.title("🔧 Painel de Controle")
    
    # Verificação de status da API
    with st.sidebar:
        st.subheader("📡 Status da API")
        if st.button("🔄 Verificar Status", use_container_width=True):
            with st.spinner("Verificando..."):
                status_code, response = call_api("/health")
                if status_code == 200:
                    st.success("✅ API Online")
                    st.json(response)
                else:
                    st.error("❌ API Offline")
                    if response:
                        st.error(response.get('error', 'Erro desconhecido'))
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📝 Editor de Prompt", "📄 Documentos", "⚙️ Sistema"])
    
    # Tab 1: Chat
    with tab1:
        st.header("💬 Chat com o Agente")
        
        # Histórico de chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Configurações do chat
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("⚙️ Configurações")
            max_results = st.slider("Máx. Resultados", 1, 10, 5)
            similarity_threshold = st.slider("Limiar Similaridade", 0.1, 1.0, 0.7, 0.1)
            
            if st.button("🗑️ Limpar Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col1:
            # Input da mensagem
            user_message = st.text_area(
                "Digite sua mensagem:",
                height=100,
                placeholder="Ex: Quais são os principais tópicos abordados nos documentos?"
            )
            
            col_send, col_example = st.columns([1, 1])
            
            with col_send:
                send_button = st.button("📤 Enviar", use_container_width=True, type="primary")
            
            with col_example:
                if st.button("💡 Exemplo", use_container_width=True):
                    st.session_state.example_message = "Resuma os principais pontos dos documentos disponíveis"
                    st.rerun()
            
            # Usar mensagem de exemplo se definida
            if 'example_message' in st.session_state:
                user_message = st.session_state.example_message
                del st.session_state.example_message
                send_button = True
            
            # Enviar mensagem
            if send_button and user_message.strip():
                with st.spinner("🤖 Processando..."):
                    # Adiciona mensagem do usuário ao histórico
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_message,
                        "timestamp": datetime.now()
                    })
                    
                    # Chama API
                    status_code, response = call_api("/chat", "POST", {
                        "message": user_message,
                        "max_results": max_results,
                        "similarity_threshold": similarity_threshold
                    })
                    
                    if status_code == 200 and response.get('success'):
                        # Adiciona resposta do agente ao histórico
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response.get('response', ''),
                            "sources": response.get('sources', []),
                            "documents_used": response.get('documents_used', 0),
                            "timestamp": datetime.now()
                        })
                    else:
                        st.error(f"Erro: {response.get('error', 'Erro desconhecido')}")
                
                st.rerun()
        
        # Exibir histórico de chat
        st.subheader("📜 Histórico do Chat")
        
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                if message["role"] == "user":
                    st.markdown(f"**👤 Você** ({message['timestamp'].strftime('%H:%M:%S')})")
                    st.markdown(f"> {message['content']}")
                else:
                    st.markdown(f"**🤖 Agente** ({message['timestamp'].strftime('%H:%M:%S')})")
                    st.markdown(message['content'])
                    
                    if message.get('sources'):
                        st.markdown("**📚 Fontes:**")
                        for source in message['sources']:
                            st.markdown(f"- {source}")
                    
                    if message.get('documents_used'):
                        st.caption(f"📊 {message['documents_used']} documentos utilizados")
                
                st.markdown("---")
    
    # Tab 2: Editor de Prompt
    with tab2:
        st.header("📝 Editor de Instruções do Agente")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("🔧 Ações")
            
            if st.button("📥 Carregar Original", use_container_width=True):
                st.session_state.prompt_content = load_agent_instructions()
                st.success("Instruções carregadas!")
                st.rerun()
            
            if st.button("💾 Salvar Alterações", use_container_width=True, type="primary"):
                if 'prompt_content' in st.session_state:
                    if save_agent_instructions(st.session_state.prompt_content):
                        st.success("✅ Instruções salvas com sucesso!")
                        st.info("ℹ️ Reinicie a API para aplicar as mudanças")
                    else:
                        st.error("❌ Erro ao salvar instruções")
                else:
                    st.warning("Nenhum conteúdo para salvar")
            
            if st.button("🔄 Resetar Padrão", use_container_width=True):
                default_prompt = """Você é um assistente inteligente especializado em análise de documentos.

## COMPORTAMENTO
- Seja preciso e baseie-se apenas nos documentos
- Cite sempre as fontes
- Estruture respostas claramente
- Admita quando não souber algo

## FORMATO DE RESPOSTA
1. Resumo direto
2. Informações detalhadas
3. Citações das fontes
4. Conclusão quando apropriado"""
                
                st.session_state.prompt_content = default_prompt
                st.info("Prompt resetado para o padrão")
                st.rerun()
        
        with col1:
            # Carrega conteúdo se não estiver na sessão
            if 'prompt_content' not in st.session_state:
                st.session_state.prompt_content = load_agent_instructions()
            
            # Editor de texto
            prompt_content = st.text_area(
                "Instruções do Agente:",
                value=st.session_state.prompt_content,
                height=400,
                help="Edite as instruções que definem o comportamento do agente"
            )
            
            # Atualiza sessão quando o conteúdo muda
            if prompt_content != st.session_state.prompt_content:
                st.session_state.prompt_content = prompt_content
            
            # Estatísticas do prompt
            st.caption(f"📊 Caracteres: {len(prompt_content)} | Linhas: {len(prompt_content.splitlines())}")
    
    # Tab 3: Documentos
    with tab3:
        st.header("📄 Gerenciamento de Documentos")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("🔧 Ações")
            
            if st.button("🔄 Reprocessar Documentos", use_container_width=True, type="primary"):
                with st.spinner("Processando documentos..."):
                    status_code, response = call_api("/documents/upload", "POST")
                    
                    if status_code == 200:
                        st.success("✅ Documentos processados com sucesso!")
                        st.json(response)
                    else:
                        st.error("❌ Erro ao processar documentos")
                        if response:
                            st.error(response.get('error', 'Erro desconhecido'))
            
            if st.button("📁 Abrir Pasta Documentos", use_container_width=True):
                st.info(f"📂 Caminho: {os.path.abspath(DOCUMENTS_PATH)}")
            
            st.markdown("### 📋 Formatos Suportados")
            st.markdown("- ✅ PDF (.pdf)")
            st.markdown("- ✅ Word (.docx)")
            st.markdown("- ⚠️ Word antigo (.doc)")
        
        with col1:
            st.subheader("📚 Documentos Disponíveis")
            
            documents = list_documents()
            
            if documents:
                df = pd.DataFrame(documents)
                st.dataframe(df, use_container_width=True)
                
                st.markdown(f"**Total:** {len(documents)} documentos")
            else:
                st.info("📭 Nenhum documento encontrado na pasta 'documents/'")
                st.markdown("**Para adicionar documentos:**")
                st.markdown("1. Coloque arquivos PDF/Word na pasta `documents/`")
                st.markdown("2. Clique em 'Reprocessar Documentos'")
    
    # Tab 4: Sistema
    with tab4:
        st.header("⚙️ Informações do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Status Detalhado")
            
            if st.button("🔍 Obter Status", use_container_width=True):
                with st.spinner("Obtendo informações..."):
                    status_code, response = call_api("/status")
                    
                    if status_code == 200:
                        st.success("✅ Sistema funcionando")
                        
                        # Informações do sistema
                        if 'system' in response:
                            st.markdown("**🖥️ Sistema:**")
                            system_info = response['system']
                            st.json(system_info)
                        
                        # Informações do vector store
                        if 'vector_store' in response:
                            st.markdown("**🔍 Vector Store:**")
                            vs_info = response['vector_store']
                            st.json(vs_info)
                        
                        # Informações do agente
                        if 'agent' in response:
                            st.markdown("**🤖 Agente:**")
                            agent_info = response['agent']
                            st.json(agent_info)
                    else:
                        st.error("❌ Erro ao obter status")
                        if response:
                            st.error(response.get('error', 'Erro desconhecido'))
        
        with col2:
            st.subheader("🛠️ Configurações")
            
            st.markdown("**📍 Endpoints da API:**")
            st.code(f"""
GET  {API_BASE_URL}/health
GET  {API_BASE_URL}/status
POST {API_BASE_URL}/chat
POST {API_BASE_URL}/documents/upload
            """)
            
            st.markdown("**📂 Caminhos:**")
            st.code(f"""
Documentos: {os.path.abspath(DOCUMENTS_PATH)}
Prompts: {os.path.abspath(PROMPTS_PATH)}
            """)
            
            st.markdown("**🔧 Como usar:**")
            st.markdown("1. Inicie a API: `python run.py`")
            st.markdown("2. Adicione documentos na pasta")
            st.markdown("3. Reprocesse os documentos")
            st.markdown("4. Converse com o agente")

if __name__ == "__main__":
    main()
