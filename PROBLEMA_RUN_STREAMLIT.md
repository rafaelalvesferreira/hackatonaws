# 🚨 PROBLEMA: PDF não usado quando rodado via run_streamlit.py

## 🔍 **DIAGNÓSTICO ESPECÍFICO:**

### **O que acontece quando você roda `run_streamlit.py`:**

1. **Script tenta iniciar API** usando `run.py` (linha 21)
2. **`run.py` importa** `src.app_aws_cli` que precisa de credenciais explícitas
3. **API falha ao inicializar** por problemas com Bedrock/credenciais
4. **Streamlit inicia** mas sem API funcionando
5. **Interface não consegue** processar documentos ou fazer chat
6. **PDF é ignorado** porque não há backend funcionando

## ❌ **PROBLEMAS IDENTIFICADOS:**

### **1. run_streamlit.py usa API errada:**
```python
# Linha 21 em run_streamlit.py
subprocess.Popen([sys.executable, "run.py"])  # ❌ Esta API falha
```

### **2. run.py importa app_aws_cli:**
```python
# run.py linha 11
from src.app_aws_cli import app, initialize_components, config  # ❌ Precisa credenciais explícitas
```

### **3. Cadeia de falhas:**
```
run_streamlit.py → run.py → app_aws_cli → Bedrock → AccessDenied → API não inicia → Streamlit sem backend
```

## 🛠️ **SOLUÇÕES:**

### **Solução 1: Usar run_streamlit.py corrigido**
Modificar `run_streamlit.py` para usar a API que funciona:

```python
# Em vez de:
subprocess.Popen([sys.executable, "run.py"])

# Usar:
subprocess.Popen([sys.executable, "src/app_iam_role.py"])
```

### **Solução 2: Iniciar manualmente (Recomendado)**
```bash
# Terminal 1: API que funciona
python3 src/app_iam_role.py

# Terminal 2: Streamlit
streamlit run streamlit_app.py --server.port 8501
```

### **Solução 3: Usar demo completo**
```bash
python3 demo.py  # Inicia API + Streamlit automaticamente
```

## 🎯 **POR QUE O PDF NÃO É USADO:**

1. **API não inicia** (falha com Bedrock)
2. **Streamlit fica sem backend** para processar documentos
3. **Interface não consegue** fazer upload/processamento
4. **Chat não funciona** (sem API)
5. **PDF nunca é processado** ou adicionado ao vector store

## ✅ **TESTE PARA CONFIRMAR:**

### **1. Verificar se API está rodando:**
```bash
curl http://localhost:5000/health
# Se der "Connection refused" = API não está rodando
```

### **2. Verificar logs do Streamlit:**
- Interface mostra erros de conexão com API
- Botões de upload/chat não funcionam
- Mensagens de erro sobre backend

### **3. Verificar se documentos foram processados:**
```bash
curl -X POST http://localhost:5000/documents/upload
# Se API não responder = documentos não foram processados
```

## 🚀 **SOLUÇÃO IMEDIATA:**

### **Opção A: Corrigir run_streamlit.py**
```bash
# Editar run_streamlit.py linha 21:
# Trocar "run.py" por "src/app_iam_role.py"
```

### **Opção B: Iniciar manualmente**
```bash
# Terminal 1
python3 src/app_iam_role.py

# Terminal 2 (aguardar API iniciar)
streamlit run streamlit_app.py --server.port 8501
```

### **Opção C: Usar demo funcionando**
```bash
python3 run_demo_api.py &
streamlit run streamlit_app.py --server.port 8501
```

## 💡 **RESUMO:**

**Problema:** `run_streamlit.py` tenta usar API que falha com Bedrock
**Resultado:** Streamlit sem backend → PDF não é processado
**Solução:** Usar API que funciona (`app_iam_role.py`) ou modo demo

---

**🎯 O PDF não está sendo usado porque a API backend não conseguiu inicializar devido aos problemas com Bedrock que já identificamos.**
