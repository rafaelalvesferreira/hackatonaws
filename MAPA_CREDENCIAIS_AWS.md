# 🗺️ MAPA DAS CREDENCIAIS AWS NO CÓDIGO

## 📍 **ONDE AS CREDENCIAIS SÃO DEFINIDAS**

### **1. config/settings.py** (Configuração Central)
```python
class Config:
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')        # ⚠️ AQUI
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') # ⚠️ AQUI
    # ❌ AWS_SESSION_TOKEN = FALTANDO!
```

**🚨 PROBLEMA IDENTIFICADO:** `AWS_SESSION_TOKEN` não está sendo lido!

## 📍 **ONDE AS CREDENCIAIS SÃO USADAS**

### **2. src/bedrock_agent.py** (Linha ~18)
```python
# Inicializa cliente Bedrock
self.bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=aws_region  # ✅ Usa região
    # ❌ Não passa credenciais explicitamente
)
```

### **3. src/vector_store.py** (Linha ~22)
```python
# Inicializa cliente Bedrock
self.bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=aws_region  # ✅ Usa região
    # ❌ Não passa credenciais explicitamente
)
```

## 🔍 **COMO BOTO3 BUSCA CREDENCIAIS**

O boto3 busca credenciais nesta ordem:
1. **Parâmetros explícitos** (não usado no código)
2. **Variáveis de ambiente** (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
3. **Arquivo ~/.aws/credentials**
4. **IAM Roles** (se em EC2)

## 🚨 **PROBLEMAS IDENTIFICADOS**

### **1. AWS_SESSION_TOKEN não está no config/settings.py**
```python
# FALTANDO:
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
```

### **2. Credenciais não são passadas explicitamente**
```python
# ATUAL (implícito):
boto3.client('bedrock-runtime', region_name=region)

# DEVERIA SER (explícito):
boto3.client(
    'bedrock-runtime',
    region_name=region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token  # ⚠️ IMPORTANTE!
)
```

## 🛠️ **CORREÇÕES NECESSÁRIAS**

### **Correção 1: Adicionar SESSION_TOKEN ao config**
```python
# Em config/settings.py
class Config:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # ✅ ADICIONAR
```

### **Correção 2: Passar credenciais explicitamente**
```python
# Em src/bedrock_agent.py e src/vector_store.py
self.bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=aws_region,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    aws_session_token=Config.AWS_SESSION_TOKEN  # ✅ ADICIONAR
)
```

## 📋 **ARQUIVOS QUE PRECISAM SER MODIFICADOS**

1. **config/settings.py** - Adicionar AWS_SESSION_TOKEN
2. **src/bedrock_agent.py** - Passar credenciais explicitamente
3. **src/vector_store.py** - Passar credenciais explicitamente

## 🎯 **SOLUÇÃO RÁPIDA**

### **Opção A: Usar variáveis de ambiente (Atual)**
```bash
# No .env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_SESSION_TOKEN=seu_session_token  # ✅ ADICIONAR ESTA LINHA
```

### **Opção B: Modificar código para passar explicitamente**
Modificar os arquivos para usar as credenciais do Config.

## 🔧 **TESTE ATUAL**

```bash
# Verificar se boto3 consegue acessar as credenciais
python3 -c "
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
print('🔍 Credenciais disponíveis:')
print(f'ACCESS_KEY: {bool(os.getenv(\"AWS_ACCESS_KEY_ID\"))}')
print(f'SECRET_KEY: {bool(os.getenv(\"AWS_SECRET_ACCESS_KEY\"))}')
print(f'SESSION_TOKEN: {bool(os.getenv(\"AWS_SESSION_TOKEN\"))}')

try:
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    print('✅ Cliente criado com sucesso')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

## 💡 **RESUMO**

**O problema é que:**
1. ✅ `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` estão sendo lidos
2. ❌ `AWS_SESSION_TOKEN` **NÃO** está sendo lido no config
3. ❌ As credenciais **NÃO** são passadas explicitamente para boto3

**Solução mais rápida:** Adicionar `AWS_SESSION_TOKEN` ao arquivo `.env` - o boto3 vai pegar automaticamente das variáveis de ambiente.
