# 🔍 Diferenças entre demo.py e run_demo_api.py

## 📋 RESUMO RÁPIDO

| Aspecto | `demo.py` | `run_demo_api.py` |
|---------|-----------|-------------------|
| **Tipo** | Script de automação completa | Servidor API Flask |
| **Função** | Configura e testa todo o sistema | Apenas roda a API em modo demo |
| **Interação** | Automático, executa e para | Fica rodando até ser parado |
| **Escopo** | Setup completo + testes | Apenas API backend |
| **Interface** | Terminal/console | HTTP endpoints |

## 🎯 demo.py - Script de Demonstração Completa

### **O que faz:**
- 🔧 **Verifica requisitos** do sistema
- 📦 **Instala dependências** automaticamente
- 📄 **Cria documentos de exemplo**
- 🚀 **Inicia API e Streamlit** juntos
- 🧪 **Executa testes automatizados**
- 📊 **Mostra relatório completo**
- ⏹️ **Para tudo automaticamente**

### **Quando usar:**
- ✅ Primeira vez configurando o sistema
- ✅ Demonstração completa para alguém
- ✅ Teste automatizado de tudo
- ✅ Setup inicial do projeto

### **Como executar:**
```bash
python3 demo.py
```

### **O que acontece:**
1. Verifica se tudo está instalado
2. Instala o que estiver faltando
3. Cria documentos de exemplo
4. Inicia API (porta 5000)
5. Inicia Streamlit (porta 8501)
6. Testa todos os endpoints
7. Mostra relatório
8. Para os serviços

---

## 🌐 run_demo_api.py - Servidor API Demo

### **O que faz:**
- 🌐 **Inicia apenas a API Flask**
- 🔄 **Fica rodando continuamente**
- 📡 **Responde a requisições HTTP**
- 🎭 **Simula funcionalidades** (sem AWS)
- 📝 **Logs de atividade**

### **Quando usar:**
- ✅ Testar apenas a API
- ✅ Desenvolvimento frontend
- ✅ Integração com outras aplicações
- ✅ Testes manuais de endpoints
- ✅ Deixar API rodando por tempo prolongado

### **Como executar:**
```bash
python3 run_demo_api.py
```

### **O que acontece:**
1. Inicia servidor Flask
2. Fica rodando em http://localhost:5000
3. Responde a requisições
4. Roda até você parar (Ctrl+C)

---

## 🔗 Endpoints da API Demo

Quando você executa `run_demo_api.py`, estes endpoints ficam disponíveis:

```bash
GET  /health              # Status da API
GET  /status              # Status do sistema
GET  /documents/list      # Lista documentos
POST /documents/upload    # Simula processamento
POST /chat               # Chat simulado
```

## 🧪 Exemplos Práticos

### **Cenário 1: Primeira vez usando o sistema**
```bash
python3 demo.py
```
- ✅ Configura tudo automaticamente
- ✅ Mostra se está funcionando
- ✅ Para quando termina

### **Cenário 2: Desenvolvendo frontend**
```bash
python3 run_demo_api.py
```
- ✅ API fica disponível
- ✅ Você pode fazer requisições
- ✅ Testa integração

### **Cenário 3: Demonstração para cliente**
```bash
python3 demo.py
```
- ✅ Setup automático
- ✅ Testes completos
- ✅ Relatório profissional

### **Cenário 4: Desenvolvimento contínuo**
```bash
python3 run_demo_api.py &  # Roda em background
# Desenvolve frontend
# API fica disponível
```

## 🔄 Fluxo de Uso Recomendado

### **1ª vez:**
```bash
python3 demo.py           # Setup completo
```

### **Desenvolvimento:**
```bash
python3 run_demo_api.py   # Apenas API
```

### **Produção (com AWS):**
```bash
python3 run.py            # API completa
python3 run_streamlit.py  # Interface completa
```

## 🎯 Qual Usar Quando?

### **Use `demo.py` quando:**
- 🆕 É sua primeira vez
- 🎪 Quer demonstração completa
- 🧪 Quer testar tudo automaticamente
- 📊 Precisa de relatório de status

### **Use `run_demo_api.py` quando:**
- 🔧 Está desenvolvendo
- 🌐 Só precisa da API
- ⏰ Quer deixar rodando por tempo
- 🔗 Está integrando com outro sistema

## 💡 Dica Pro

**Para desenvolvimento:**
```bash
# Terminal 1: API
python3 run_demo_api.py

# Terminal 2: Frontend
python3 start_demo.py

# Agora você tem API + Interface rodando separadamente
```

**Para demonstração rápida:**
```bash
python3 demo.py  # Faz tudo automaticamente
```
