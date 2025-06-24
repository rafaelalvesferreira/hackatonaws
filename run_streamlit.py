#!/usr/bin/env python3
"""
Script para executar a interface Streamlit do Agente de Documentos Bedrock
"""

import os
import sys
import subprocess
import time
import requests
from threading import Thread

def check_api_status():
    """Verifica se a API está rodando"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_api():
    """Inicia a API em background"""
    print("🚀 Iniciando API Flask...")
    subprocess.Popen([
        sys.executable, "run.py"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Aguarda API inicializar
    print("⏳ Aguardando API inicializar...")
    for i in range(30):  # Aguarda até 30 segundos
        if check_api_status():
            print("✅ API iniciada com sucesso!")
            return True
        time.sleep(1)
        print(f"   Tentativa {i+1}/30...")
    
    print("❌ Timeout ao iniciar API")
    return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🎨 INTERFACE STREAMLIT - AGENTE DE DOCUMENTOS BEDROCK")
    print("=" * 60)
    
    # Verifica se está no diretório correto
    if not os.path.exists("streamlit_app.py"):
        print("❌ Erro: Execute este script no diretório do projeto")
        return 1
    
    # Verifica se a API já está rodando
    if not check_api_status():
        print("🔍 API não encontrada. Tentando iniciar...")
        
        if not start_api():
            print("❌ Não foi possível iniciar a API automaticamente")
            print("💡 Inicie manualmente com: python run.py")
            print("   Em seguida execute: streamlit run streamlit_app.py")
            return 1
    else:
        print("✅ API já está rodando!")
    
    print("\n📋 INFORMAÇÕES:")
    print("   • API Flask: http://localhost:5000")
    print("   • Interface Streamlit: http://localhost:8501")
    print("   • Para parar: Ctrl+C")
    
    print("\n🎨 Iniciando interface Streamlit...")
    print("=" * 60)
    
    try:
        # Inicia Streamlit
        subprocess.run([
            "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada pelo usuário")
        return 0
    except FileNotFoundError:
        print("❌ Streamlit não encontrado. Instale com: pip install streamlit")
        return 1
    except Exception as e:
        print(f"❌ Erro ao iniciar Streamlit: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
