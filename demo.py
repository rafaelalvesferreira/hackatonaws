#!/usr/bin/env python3
"""
Script de demonstração completo do Agente de Documentos Bedrock
"""

import os
import sys
import time
import subprocess
import requests
import json
from datetime import datetime

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def print_step(step, description):
    """Imprime passo da demonstração"""
    print(f"\n📋 PASSO {step}: {description}")
    print("-" * 40)

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print_step(1, "Verificando Requisitos")
    
    required_files = [
        "requirements.txt",
        "src/app.py",
        "streamlit_app.py",
        "prompts/agent_instructions.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados")
    return True

def install_dependencies():
    """Instala dependências"""
    print_step(2, "Instalando Dependências")
    
    try:
        print("📦 Instalando pacotes Python...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
            return True
        else:
            print("❌ Erro ao instalar dependências:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def create_sample_documents():
    """Cria documentos de exemplo"""
    print_step(3, "Criando Documentos de Exemplo")
    
    # Documento 1: Manual do Usuário
    doc1_content = """# Manual do Usuário - Sistema de Gestão

## Introdução
Este manual descreve como utilizar o Sistema de Gestão da empresa.

## Funcionalidades Principais
1. **Cadastro de Clientes**: Permite registrar novos clientes
2. **Gestão de Pedidos**: Controla pedidos e entregas
3. **Relatórios**: Gera relatórios financeiros e operacionais

## Como Usar
### Login
1. Acesse o sistema através do navegador
2. Digite seu usuário e senha
3. Clique em "Entrar"

### Cadastrar Cliente
1. Vá para o menu "Clientes"
2. Clique em "Novo Cliente"
3. Preencha os dados obrigatórios
4. Salve as informações

## Suporte
Para suporte técnico, entre em contato:
- Email: suporte@empresa.com
- Telefone: (11) 1234-5678
"""
    
    # Documento 2: Políticas da Empresa
    doc2_content = """# Políticas da Empresa XYZ

## Política de Recursos Humanos

### Horário de Trabalho
- Horário padrão: 8h às 17h
- Intervalo para almoço: 12h às 13h
- Flexibilidade de 30 minutos na entrada

### Benefícios
- Vale alimentação: R$ 500,00/mês
- Vale transporte: Conforme necessidade
- Plano de saúde: Cobertura nacional
- Seguro de vida: Valor equivalente a 12 salários

### Política de Férias
- 30 dias corridos após 12 meses de trabalho
- Possibilidade de venda de 10 dias
- Abono de 1/3 do salário

## Política de Segurança da Informação

### Senhas
- Mínimo de 8 caracteres
- Combinação de letras, números e símbolos
- Troca obrigatória a cada 90 dias

### Acesso aos Sistemas
- Cada funcionário possui login único
- Acesso baseado no cargo e função
- Monitoramento de atividades

### Backup de Dados
- Backup diário automático
- Cópias armazenadas em local seguro
- Teste de restauração mensal
"""
    
    try:
        # Cria documentos de exemplo
        os.makedirs("documents", exist_ok=True)
        
        with open("documents/manual_usuario.txt", "w", encoding="utf-8") as f:
            f.write(doc1_content)
        
        with open("documents/politicas_empresa.txt", "w", encoding="utf-8") as f:
            f.write(doc2_content)
        
        print("✅ Documentos de exemplo criados:")
        print("   - documents/manual_usuario.txt")
        print("   - documents/politicas_empresa.txt")
        
        print("\n💡 Para usar seus próprios documentos:")
        print("   - Coloque arquivos PDF/Word na pasta 'documents/'")
        print("   - Execute o reprocessamento via API ou interface")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar documentos: {e}")
        return False

def check_aws_config():
    """Verifica configuração AWS"""
    print_step(4, "Verificando Configuração AWS")
    
    if os.path.exists(".env"):
        print("✅ Arquivo .env encontrado")
        
        # Lê configurações
        with open(".env", "r") as f:
            content = f.read()
            
        if "AWS_ACCESS_KEY_ID" in content and "AWS_SECRET_ACCESS_KEY" in content:
            print("✅ Credenciais AWS configuradas")
            return True
        else:
            print("⚠️  Credenciais AWS não encontradas no .env")
    else:
        print("⚠️  Arquivo .env não encontrado")
    
    print("\n🔧 Para configurar AWS:")
    print("   1. Copie .env.example para .env")
    print("   2. Edite .env com suas credenciais AWS")
    print("   3. Certifique-se de ter acesso ao Bedrock")
    
    return False

def start_demo_servers():
    """Inicia servidores para demonstração"""
    print_step(5, "Iniciando Servidores")
    
    print("🚀 Iniciando API Flask...")
    api_process = subprocess.Popen([
        sys.executable, "run.py"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Aguarda API inicializar
    print("⏳ Aguardando API inicializar...")
    for i in range(20):
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API Flask iniciada com sucesso!")
                break
        except:
            pass
        time.sleep(1)
        print(f"   Tentativa {i+1}/20...")
    else:
        print("❌ Timeout ao iniciar API")
        api_process.terminate()
        return None, None
    
    print("\n🎨 Iniciando Interface Streamlit...")
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(3)  # Aguarda Streamlit inicializar
    
    return api_process, streamlit_process

def run_api_tests():
    """Executa testes da API"""
    print_step(6, "Testando API")
    
    tests = [
        ("Health Check", "GET", "/health", None),
        ("Status", "GET", "/status", None),
        ("Upload Documentos", "POST", "/documents/upload", None),
    ]
    
    results = []
    
    for test_name, method, endpoint, data in tests:
        try:
            url = f"http://localhost:5000{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=30)
            
            success = response.status_code == 200
            results.append((test_name, success))
            
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"   {test_name}: {status}")
            
            if not success:
                print(f"      Status: {response.status_code}")
                try:
                    error = response.json().get('error', 'Erro desconhecido')
                    print(f"      Erro: {error}")
                except:
                    pass
            
        except Exception as e:
            results.append((test_name, False))
            print(f"   {test_name}: ❌ ERRO - {e}")
    
    # Teste de chat se outros testes passaram
    if all(result for _, result in results):
        print("\n💬 Testando Chat:")
        try:
            chat_data = {
                "message": "Olá! Quais informações você tem disponíveis?",
                "max_results": 3
            }
            
            response = requests.post(
                "http://localhost:5000/chat",
                json=chat_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("   ✅ Chat funcionando!")
                    print(f"   📝 Resposta: {result.get('response', '')[:100]}...")
                else:
                    print(f"   ❌ Erro no chat: {result.get('error', '')}")
            else:
                print(f"   ❌ Erro HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro no teste de chat: {e}")
    
    return results

def show_final_info():
    """Mostra informações finais"""
    print_header("DEMONSTRAÇÃO CONCLUÍDA")
    
    print("🌐 SERVIÇOS DISPONÍVEIS:")
    print("   • API Flask: http://localhost:5000")
    print("   • Interface Streamlit: http://localhost:8501")
    
    print("\n🔧 ENDPOINTS DA API:")
    print("   • GET  /health - Health check")
    print("   • GET  /status - Status detalhado")
    print("   • POST /chat - Chat com agente")
    print("   • POST /documents/upload - Processar documentos")
    
    print("\n🎨 RECURSOS DA INTERFACE:")
    print("   • 💬 Chat interativo com o agente")
    print("   • 📝 Editor de prompts em tempo real")
    print("   • 📄 Gerenciamento de documentos")
    print("   • ⚙️ Monitoramento do sistema")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("   1. Acesse http://localhost:8501 para usar a interface")
    print("   2. Configure suas credenciais AWS no arquivo .env")
    print("   3. Adicione seus documentos na pasta 'documents/'")
    print("   4. Reprocesse os documentos via interface")
    print("   5. Converse com o agente!")
    
    print("\n⚠️  PARA PARAR OS SERVIÇOS:")
    print("   • Pressione Ctrl+C neste terminal")
    print("   • Ou execute: pkill -f 'python.*run.py'")
    print("   • Ou execute: pkill -f 'streamlit'")

def main():
    """Função principal da demonstração"""
    print_header("DEMONSTRAÇÃO - AGENTE DE DOCUMENTOS BEDROCK")
    
    print("🎯 Esta demonstração irá:")
    print("   1. Verificar requisitos")
    print("   2. Instalar dependências")
    print("   3. Criar documentos de exemplo")
    print("   4. Verificar configuração AWS")
    print("   5. Iniciar servidores")
    print("   6. Executar testes")
    print("   7. Mostrar informações finais")
    
    input("\n🚀 Pressione Enter para começar...")
    
    # Executa passos da demonstração
    steps = [
        ("Verificar Requisitos", check_requirements),
        ("Instalar Dependências", install_dependencies),
        ("Criar Documentos de Exemplo", create_sample_documents),
        ("Verificar Configuração AWS", check_aws_config),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Falha em: {step_name}")
            print("🛑 Demonstração interrompida")
            return 1
    
    # Inicia servidores
    api_process, streamlit_process = start_demo_servers()
    
    if not api_process or not streamlit_process:
        print("❌ Falha ao iniciar servidores")
        return 1
    
    try:
        # Executa testes
        results = run_api_tests()
        
        # Mostra informações finais
        show_final_info()
        
        # Aguarda interrupção do usuário
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO ATIVA!")
        print("   Pressione Ctrl+C para encerrar...")
        print("=" * 60)
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando demonstração...")
        
        # Encerra processos
        if api_process:
            api_process.terminate()
            print("✅ API Flask encerrada")
        
        if streamlit_process:
            streamlit_process.terminate()
            print("✅ Interface Streamlit encerrada")
        
        print("🎯 Demonstração concluída com sucesso!")
        return 0
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        
        # Encerra processos em caso de erro
        if api_process:
            api_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
