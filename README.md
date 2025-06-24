# 🤖 Agente de Documentos Amazon Bedrock

Um agente inteligente que utiliza Amazon Bedrock para análise e busca em documentos PDF e Word, estruturado como uma API Flask com interface Streamlit.

## 🚀 Características

- **Processamento de Documentos**: Suporte para PDF e Word (.docx)
- **Busca Vetorial**: Utiliza FAISS para busca semântica eficiente
- **Amazon Bedrock**: Integração com modelos Claude 3 Sonnet
- **API REST**: Interface Flask para integração fácil
- **Interface Web**: Frontend Streamlit interativo
- **Editor de Prompts**: Modificação em tempo real das instruções do agente
- **Embeddings**: Utiliza Amazon Titan para vetorização
- **Instruções Personalizáveis**: Prompt do agente configurável

## 📁 Estrutura do Projeto

```
bedrock-document-agent/
├── documents/              # Coloque seus PDFs e Word aqui
├── prompts/
│   └── agent_instructions.txt  # Instruções do agente
├── config/
│   └── settings.py         # Configurações
├── src/
│   ├── app.py             # API Flask principal
│   ├── document_processor.py  # Processamento de documentos
│   ├── vector_store.py    # Sistema de busca vetorial
│   └── bedrock_agent.py   # Agente Bedrock
├── vector_store/          # Índice vetorial (criado automaticamente)
├── streamlit_app.py       # Interface web Streamlit
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore            # Arquivos ignorados pelo Git
├── run.py                # Script principal da API
├── run_streamlit.py      # Script para interface web
├── demo.py               # Demonstração completa
└── test_api.py           # Script de teste da API
```

## ⚙️ Configuração

### 1. Instalar Dependências

```bash
cd bedrock-document-agent
pip install -r requirements.txt
```

### 2. Configurar Credenciais AWS

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas credenciais
nano .env
```

Configure no arquivo `.env`:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### 3. Verificar Permissões Bedrock

Certifique-se de que sua conta AWS tem acesso aos modelos:
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `amazon.titan-embed-text-v1`

## 📄 Adicionando Documentos

1. Coloque seus arquivos PDF e Word na pasta `documents/`
2. Execute o processamento via API ou interface web

## 🚀 Executando o Sistema

### Método 1: Demonstração Completa (Recomendado)
```bash
python demo.py
```
Este script irá:
- Verificar requisitos
- Instalar dependências
- Criar documentos de exemplo
- Iniciar API e interface web
- Executar testes automatizados

### Método 2: Interface Web + API
```bash
python run_streamlit.py
```
Inicia automaticamente a API Flask e a interface Streamlit.

### Método 3: Apenas API
```bash
python run.py
```
Inicia apenas a API Flask em `http://localhost:5000`

### Método 4: Apenas Interface Web
```bash
streamlit run streamlit_app.py
```
Inicia apenas a interface em `http://localhost:8501` (API deve estar rodando)

## 🎨 Interface Web Streamlit

A interface web oferece:

### 💬 **Chat Interativo**
- Conversa em tempo real com o agente
- Histórico de mensagens
- Configuração de parâmetros de busca
- Visualização de fontes utilizadas

### 📝 **Editor de Prompts**
- Modificação em tempo real das instruções do agente
- Preview das alterações
- Salvamento automático
- Templates predefinidos

### 📄 **Gerenciamento de Documentos**
- Lista de documentos disponíveis
- Informações de tamanho e data
- Reprocessamento com um clique
- Status do processamento

### ⚙️ **Monitoramento do Sistema**
- Status da API em tempo real
- Informações do vector store
- Configurações do agente
- Logs e métricas

## 🔌 Endpoints da API

### 1. Health Check
```bash
GET /health
```

### 2. Status do Sistema
```bash
GET /status
```

### 3. Processar Documentos
```bash
POST /documents/upload
```

### 4. Chat com o Agente
```bash
POST /chat
Content-Type: application/json

{
  "message": "Sua pergunta aqui",
  "max_results": 5,
  "similarity_threshold": 0.7
}
```

## 🧪 Testando o Sistema

### Teste Automatizado
```bash
python test_api.py
```

### Teste Manual via Interface
1. Acesse `http://localhost:8501`
2. Vá para a aba "Documentos"
3. Clique em "Reprocessar Documentos"
4. Vá para a aba "Chat"
5. Digite uma pergunta e teste

## 💬 Exemplo de Uso

### Via API
```python
import requests

# Chat com o agente
response = requests.post('http://localhost:5000/chat', json={
    "message": "Quais são os principais tópicos abordados nos documentos?"
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Fontes: {result['sources']}")
```

### Via Interface Web
1. Acesse `http://localhost:8501`
2. Vá para a aba "Chat"
3. Digite sua pergunta
4. Veja a resposta com fontes citadas

## ⚙️ Configurações Avançadas

### Modelos Bedrock Suportados
- Claude 3 Sonnet (padrão)
- Claude 3 Haiku
- Outros modelos compatíveis

### Parâmetros de Busca
- `CHUNK_SIZE`: Tamanho dos chunks (padrão: 1000)
- `CHUNK_OVERLAP`: Sobreposição entre chunks (padrão: 200)
- `MAX_SEARCH_RESULTS`: Máximo de documentos retornados (padrão: 5)
- `SIMILARITY_THRESHOLD`: Limiar de similaridade (padrão: 0.7)

## 🔧 Personalização

### Modificar Instruções do Agente
1. **Via Interface Web**: Use o editor na aba "Editor de Prompt"
2. **Via Arquivo**: Edite `prompts/agent_instructions.txt`

### Adicionar Novos Tipos de Documento
Modifique `src/document_processor.py` para suportar outros formatos.

### Customizar Interface
Modifique `streamlit_app.py` para personalizar a interface web.

## 🐛 Solução de Problemas

### Erro de Credenciais AWS
- Verifique se as credenciais estão corretas no `.env`
- Confirme se a região está correta
- Teste com AWS CLI: `aws sts get-caller-identity`

### Erro de Acesso ao Bedrock
- Verifique se os modelos estão habilitados na sua conta
- Confirme as permissões IAM para Bedrock

### Interface não Carrega
- Verifique se a API está rodando em `localhost:5000`
- Confirme se o Streamlit está na porta `8501`
- Veja os logs para erros específicos

### Documentos Não Processados
- Verifique se os arquivos estão na pasta `documents/`
- Confirme se são PDFs ou Word válidos
- Use a interface para reprocessar

## 📊 Monitoramento

O sistema fornece logs detalhados sobre:
- Processamento de documentos
- Buscas realizadas
- Chamadas para Bedrock
- Erros e exceções
- Atividade da interface web

## 🔒 Segurança

- Nunca commite credenciais AWS no código
- Use IAM roles quando possível
- Mantenha as dependências atualizadas
- Configure CORS adequadamente para produção
- O `.gitignore` protege arquivos sensíveis

## 📈 Performance

Para melhor performance:
- Use instâncias EC2 com mais memória para documentos grandes
- Configure cache para embeddings frequentes
- Otimize o tamanho dos chunks baseado no seu caso de uso
- Use SSD para armazenamento do vector store

## 🎯 Casos de Uso

- **Suporte ao Cliente**: Base de conhecimento inteligente
- **Análise de Contratos**: Busca em documentos legais
- **Manuais Técnicos**: Assistente para documentação
- **Pesquisa Acadêmica**: Análise de papers e artigos
- **Compliance**: Consulta a políticas e procedimentos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ usando Amazon Bedrock, Flask e Streamlit**
