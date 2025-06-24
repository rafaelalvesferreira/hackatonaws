# 📋 Qual Requirements.txt Usar?

## 🎯 **RESPOSTA RÁPIDA**

### **✅ MAIS ATUALIZADO E RECOMENDADO:**
```bash
requirements_2024_updated.txt
```
**Por quê:** Versões exatas que estão funcionando no seu sistema agora.

## 📊 **COMPARAÇÃO DOS ARQUIVOS**

| Arquivo | Status | Quando Usar |
|---------|--------|-------------|
| `requirements.txt` | ✅ **ATUALIZADO** | Uso geral (foi corrigido) |
| `requirements_2024_updated.txt` | ✅ **MAIS COMPLETO** | Instalação completa |
| `requirements_minimal_2024.txt` | ✅ **RÁPIDO** | Instalação mínima |
| `requirements_working.txt` | ✅ **FUNCIONAL** | Versões flexíveis |
| `requirements_compatible.txt` | ⚠️ **ANTIGO** | Não usar |
| `requirements_fixed.txt` | ⚠️ **ANTIGO** | Não usar |
| `requirements_minimal.txt` | ⚠️ **ANTIGO** | Não usar |

## 🚀 **RECOMENDAÇÕES POR CENÁRIO**

### **🎯 Para Instalação Nova (Recomendado)**
```bash
pip install -r requirements_2024_updated.txt
```
- ✅ Versões exatas testadas
- ✅ Sem conflitos
- ✅ Comentários explicativos
- ✅ Mais completo

### **⚡ Para Instalação Rápida**
```bash
pip install -r requirements_minimal_2024.txt
```
- ✅ Apenas o essencial
- ✅ Instalação mais rápida
- ✅ Menos dependências

### **🔄 Para Atualizar Sistema Existente**
```bash
pip install -r requirements.txt
```
- ✅ Arquivo principal atualizado
- ✅ Compatível com projeto original

### **🧪 Para Desenvolvimento**
```bash
pip install -r requirements_working.txt
```
- ✅ Versões flexíveis (>=)
- ✅ Permite atualizações automáticas

## 📦 **VERSÕES ATUAIS FUNCIONANDO**

```txt
flask==2.3.3
boto3==1.38.42
langchain==0.3.26
langchain-aws==0.2.27
langchain-community==0.3.26
langchain-core==0.3.66
streamlit==1.46.0
faiss-cpu==1.7.4
```

## 🔧 **COMANDOS DE INSTALAÇÃO**

### **Instalação Limpa (Recomendada)**
```bash
# 1. Limpar cache
pip cache purge

# 2. Instalar versão mais atualizada
pip install -r requirements_2024_updated.txt

# 3. Verificar
python3 test_basic.py
```

### **Instalação Rápida**
```bash
pip install -r requirements_minimal_2024.txt
```

### **Resolução de Conflitos**
```bash
python3 install_clean.py
```

## ⚠️ **ARQUIVOS OBSOLETOS (NÃO USAR)**

- ❌ `requirements_fixed.txt` - Versões antigas
- ❌ `requirements_compatible.txt` - Versões antigas  
- ❌ `requirements_minimal.txt` - Versões antigas

## 🎉 **RESUMO FINAL**

### **🥇 MELHOR OPÇÃO:**
```bash
requirements_2024_updated.txt
```

### **🥈 ALTERNATIVA RÁPIDA:**
```bash
requirements_minimal_2024.txt
```

### **🥉 PADRÃO DO PROJETO:**
```bash
requirements.txt  # (foi atualizado)
```

## 🧪 **TESTE APÓS INSTALAÇÃO**

```bash
# Teste básico
python3 test_basic.py

# Teste da API
python3 run_demo_api.py

# Teste das importações
python3 -c "
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
print('✅ Tudo funcionando!')
"
```

## 💡 **DICA PRO**

**Para nova instalação:**
```bash
cd /home/ec2-user/hackatonaws
pip cache purge
pip install -r requirements_2024_updated.txt
python3 test_basic.py
```

**Para desenvolvimento contínuo:**
```bash
pip install -r requirements_working.txt
```

---

**🎯 Use `requirements_2024_updated.txt` - é o mais completo e atualizado!**
