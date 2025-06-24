# 🚨 ERRO: "You don't have access" - Bedrock

## 🔍 **PROBLEMA IDENTIFICADO**

**Erro:** `botocore.errorfactory` na linha 50 do `app.py`
**Causa:** Tentativa de acessar Amazon Bedrock sem permissões adequadas

**Local do erro:** Inicialização do `VectorStore` que tenta usar embeddings do Bedrock

## 🎯 **CAUSAS POSSÍVEIS**

### **1. Modelos Bedrock não habilitados**
- ❌ Modelo `amazon.titan-embed-text-v1` não está habilitado na sua conta
- ❌ Região não suporta Bedrock
- ❌ Conta não tem acesso ao Bedrock

### **2. Permissões IAM insuficientes**
- ❌ Usuário/Role não tem permissão `bedrock:InvokeModel`
- ❌ Falta permissão para embeddings
- ❌ Política IAM restritiva

### **3. Credenciais incorretas**
- ❌ SESSION_TOKEN expirado
- ❌ Credenciais de região diferente
- ❌ Conta sem acesso ao Bedrock

## 🛠️ **SOLUÇÕES**

### **SOLUÇÃO 1: Verificar Acesso ao Bedrock**
```bash
# Testar acesso aos modelos
aws bedrock list-foundation-models --region us-east-1

# Se der erro, você não tem acesso ao Bedrock
```

### **SOLUÇÃO 2: Habilitar Modelos no Console AWS**
1. Acesse **AWS Console → Bedrock**
2. Vá em **Model Access**
3. Habilite os modelos:
   - ✅ `Claude 3 Sonnet`
   - ✅ `Titan Embeddings`

### **SOLUÇÃO 3: Usar Modo Demo (Imediato)**
```bash
# Em vez de app.py, use:
python3 run_demo_api.py
```

### **SOLUÇÃO 4: Modificar app.py para Modo Fallback**
Criar versão que funciona sem Bedrock quando há erro de acesso.

## 🚀 **SOLUÇÃO IMEDIATA**

### **Opção A: Modo Demo**
```bash
cd /home/ec2-user/hackatonaws
python3 run_demo_api.py
# ✅ Funciona sem Bedrock
# ✅ Simula todas as funcionalidades
```

### **Opção B: Verificar Permissões**
```bash
# Verificar se tem acesso ao Bedrock
aws bedrock list-foundation-models --region us-east-1 2>&1 | head -5
```

### **Opção C: Testar Credenciais**
```bash
python3 -c "
import boto3
try:
    client = boto3.client('bedrock', region_name='us-east-1')
    models = client.list_foundation_models()
    print('✅ Acesso ao Bedrock OK')
    print(f'Modelos disponíveis: {len(models[\"modelSummaries\"])}')
except Exception as e:
    print(f'❌ Erro de acesso: {e}')
    print('💡 Use: python3 run_demo_api.py')
"
```

## 🔧 **CORREÇÃO NO CÓDIGO**

### **Criar app.py com fallback:**
```python
# Modificar src/app.py para tentar Bedrock, mas usar demo se falhar
try:
    # Tentar inicializar com Bedrock
    vector_store = VectorStore(...)
    bedrock_mode = True
except Exception as e:
    logger.warning(f"Bedrock não disponível: {e}")
    logger.info("Iniciando em modo demo...")
    # Usar modo demo/simulado
    bedrock_mode = False
```

## 📋 **CHECKLIST DE VERIFICAÇÃO**

- [ ] **Conta tem acesso ao Bedrock?**
  ```bash
  aws bedrock list-foundation-models --region us-east-1
  ```

- [ ] **Modelos estão habilitados?**
  - Console AWS → Bedrock → Model Access

- [ ] **Região correta?**
  - Bedrock não está disponível em todas as regiões

- [ ] **Permissões IAM?**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "bedrock:InvokeModel",
          "bedrock:ListFoundationModels"
        ],
        "Resource": "*"
      }
    ]
  }
  ```

## 🎯 **RECOMENDAÇÃO IMEDIATA**

**Para testar agora:**
```bash
python3 run_demo_api.py
```

**Para usar Bedrock real:**
1. Habilite modelos no Console AWS
2. Verifique permissões IAM
3. Teste com: `aws bedrock list-foundation-models`
4. Execute: `python3 run.py`

## 💡 **DICA IMPORTANTE**

O erro "you don't have access" é **muito comum** com Bedrock porque:
- ✅ Bedrock requer habilitação manual dos modelos
- ✅ Não está disponível em todas as regiões
- ✅ Requer permissões específicas

**Use o modo demo enquanto configura o acesso ao Bedrock!**
