#!/usr/bin/env python3
"""
Script de demonstração completo do Agente de Documentos Bedrock - VERSÃO CORRIGIDA
Resolve problema de "falha após 20 tentativas"
"""

import os
import sys
import time
import subprocess
import requests
import json
import signal
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
    """Instala dependências se necessário"""
    print_step(2, "Verificando Dependências")
    
    try:
        import flask
        import streamlit
        import boto3
        print("✅ Dependências principais já instaladas")
        return True
    except ImportError as e:
        print(f"⚠️  Instalando dependências faltantes...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_2024_updated.txt"
            ], check=True, capture_output=True)
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False

def create_sample_documents():
    """Cria documentos de exemplo se não existirem"""
    print_step(3, "Verificando Documentos")
    
    docs_dir = "documents"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    sample_doc = os.path.join(docs_dir, "exemplo_demo.txt")
    if not os.path.exists(sample_doc):
        content = """
Documento de Exemplo - Agente Bedrock

Este é um documento de exemplo para demonstrar as capacidades do Agente de Documentos Amazon Bedrock.

Funcionalidades:
- Processamento de documentos PDF e Word
- Busca vetorial usando FAISS
- Integração com Amazon Bedrock
- Interface web com Streamlit
- API REST com Flask

Casos de Uso:
- Suporte ao cliente
- Análise de documentos
- Base de conhecimento
- Assistente de pesquisa

O sistema permite fazer perguntas em linguagem natural sobre o conteúdo dos documentos.
        """.strip()
        
        with open(sample_doc, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Documento de exemplo criado: {sample_doc}")
    else:
        print("✅ Documentos já existem")
    
    return True

def check_port_available(port):
    """Verifica se uma porta está disponível"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return True

def kill_existing_processes():
    """Mata processos existentes que podem conflitar"""
    print("🔧 Limpando processos existentes...")
    
    processes_to_kill = ['flask', 'streamlit', 'run.py', 'run_demo_api']
    
    for proc in processes_to_kill:
        try:
            subprocess.run(['pkill', '-f', proc], capture_output=True, timeout=5)
        except:
            pass
    
    time.sleep(2)  # Aguarda processos terminarem
    print("✅ Processos limpos")

def start_demo_servers():
    """Inicia servidores para demonstração - VERSÃO CORRIGIDA"""
    print_step(4, "Iniciando Servidores")
    
    # Limpar processos existentes primeiro
    kill_existing_processes()
    
    # Verificar se portas estão livres
    if not check_port_available(5000):
        print("⚠️  Porta 5000 em uso, tentando limpar...")
        subprocess.run(['pkill', '-f', ':5000'], capture_output=True)
        time.sleep(2)
    
    if not check_port_available(8501):
        print("⚠️  Porta 8501 em uso, tentando limpar...")
        subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
        time.sleep(2)
    
    # Iniciar API (usando versão demo que funciona)
    print("🚀 Iniciando API Flask...")
    try:
        api_process = subprocess.Popen([
            sys.executable, "run_demo_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aguarda API inicializar - VERSÃO MELHORADA
        print("⏳ Aguardando API inicializar...")
        api_started = False
        
        # Reduzido de 20 para 10 tentativas e melhor lógica
        for i in range(10):
            try:
                response = requests.get("http://localhost:5000/health", timeout=3)
                if response.status_code == 200:
                    print("✅ API Flask iniciada com sucesso!")
                    api_started = True
                    break
            except requests.exceptions.ConnectionError:
                # Esperado enquanto API não inicia
                pass
            except Exception as e:
                print(f"⚠️  Tentativa {i+1}: {e}")
            
            time.sleep(2)  # Aumentado de 1 para 2 segundos
            if i < 9:  # Não mostrar na última tentativa
                print(f"   Aguardando... ({i+1}/10)")
        
        if not api_started:
            print("❌ Falha ao iniciar API após 10 tentativas")
            print("📋 Verificando logs da API...")
            
            # Mostrar logs de erro se houver
            try:
                stdout, stderr = api_process.communicate(timeout=2)
                if stderr:
                    print(f"Erro da API: {stderr[:200]}...")
            except:
                pass
            
            api_process.terminate()
            return None, None
            
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        return None, None
    
    # Iniciar Streamlit
    print("\n🎨 Iniciando Interface Streamlit...")
    try:
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aguardar Streamlit inicializar
        time.sleep(5)
        print("✅ Interface Streamlit iniciada!")
        
    except Exception as e:
        print(f"❌ Erro ao iniciar Streamlit: {e}")
        if api_process:
            api_process.terminate()
        return None, None
    
    return api_process, streamlit_process

def run_api_tests():
    """Executa testes da API - VERSÃO MELHORADA"""
    print_step(5, "Testando API")
    
    tests = [
        ("Health Check", "GET", "/health", None),
        ("Status", "GET", "/status", None),
        ("Listar Documentos", "GET", "/documents/list", None),
        ("Chat Demo", "POST", "/chat", {"message": "Olá! Como você funciona?"})
    ]
    
    results = []
    base_url = "http://localhost:5000"
    
    for test_name, method, endpoint, data in tests:
        print(f"\n🧪 Testando: {test_name}")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", json=data, timeout=10)
            
            success = response.status_code == 200
            results.append((test_name, success))
            
            if success:
                print(f"   ✅ Sucesso ({response.status_code})")
                # Mostrar parte da resposta se for JSON
                try:
                    resp_data = response.json()
                    if 'message' in resp_data:
                        msg = resp_data['message'][:100]
                        print(f"   💬 {msg}...")
                except:
                    pass
            else:
                print(f"   ❌ Falha ({response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results.append((test_name, False))
    
    return results

def show_demo_info():
    """Mostra informações da demonstração"""
    print_step(6, "Informações da Demonstração")
    
    print("🌐 SERVIÇOS DISPONÍVEIS:")
    print("   • API Flask: http://localhost:5000")
    print("   • Interface Web: http://localhost:8501")
    print()
    print("📋 ENDPOINTS DA API:")
    print("   • GET  /health - Status da API")
    print("   • GET  /status - Status do sistema")
    print("   • GET  /documents/list - Lista documentos")
    print("   • POST /chat - Chat com o agente")
    print()
    print("🎯 COMO TESTAR:")
    print("   1. Abra http://localhost:8501 no navegador")
    print("   2. Vá para a aba 'Chat'")
    print("   3. Digite uma pergunta")
    print("   4. Veja a resposta do agente")
    print()
    print("⚠️  MODO DEMONSTRAÇÃO:")
    print("   • Respostas são simuladas")
    print("   • Para IA real, configure credenciais AWS")
    print("   • Documentos são listados mas não processados")

def cleanup_processes(api_process, streamlit_process):
    """Limpa processos ao finalizar"""
    print("\n🛑 Finalizando demonstração...")
    
    if api_process:
        try:
            api_process.terminate()
            api_process.wait(timeout=5)
            print("✅ API finalizada")
        except:
            api_process.kill()
    
    if streamlit_process:
        try:
            streamlit_process.terminate()
            streamlit_process.wait(timeout=5)
            print("✅ Streamlit finalizado")
        except:
            streamlit_process.kill()

def main():
    """Função principal da demonstração"""
    print("🚀 DEMONSTRAÇÃO COMPLETA - AGENTE BEDROCK")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔧 Versão corrigida - sem loops infinitos")
    print("=" * 60)
    
    # Mudar para diretório do projeto
    os.chdir('/home/ec2-user/hackatonaws')
    
    api_process = None
    streamlit_process = None
    
    try:
        # Executar passos da demonstração
        if not check_requirements():
            print("❌ Requisitos não atendidos")
            return False
        
        if not install_dependencies():
            print("❌ Falha ao instalar dependências")
            return False
        
        if not create_sample_documents():
            print("❌ Falha ao criar documentos")
            return False
        
        # Iniciar servidores
        api_process, streamlit_process = start_demo_servers()
        if not api_process:
            print("❌ Falha ao iniciar servidores")
            return False
        
        # Executar testes
        test_results = run_api_tests()
        
        # Mostrar resultados
        print_step(7, "Resultados dos Testes")
        passed = sum(1 for _, success in test_results if success)
        total = len(test_results)
        
        for test_name, success in test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {test_name:20} {status}")
        
        print(f"\n📊 Resultado: {passed}/{total} testes passaram")
        
        # Mostrar informações
        show_demo_info()
        
        # Aguardar interação do usuário
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO ATIVA!")
        print("=" * 60)
        print("⏹️  Pressione Ctrl+C para finalizar")
        
        # Loop de espera (substituindo o loop infinito problemático)
        try:
            while True:
                time.sleep(5)
                # Verificar se processos ainda estão rodando
                if api_process.poll() is not None:
                    print("⚠️  API parou inesperadamente")
                    break
                if streamlit_process.poll() is not None:
                    print("⚠️  Streamlit parou inesperadamente")
                    break
        except KeyboardInterrupt:
            print("\n🛑 Interrompido pelo usuário")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        return False
    
    finally:
        # Sempre limpar processos
        cleanup_processes(api_process, streamlit_process)

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'✅ Demonstração concluída com sucesso!' if success else '❌ Demonstração falhou'}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Demonstração interrompida")
        sys.exit(0)
