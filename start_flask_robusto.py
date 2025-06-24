#!/usr/bin/env python3
"""
Inicializador robusto para Flask - Resolve problemas de inicialização
"""

import os
import sys
import time
import socket
import subprocess
import signal
import threading
from datetime import datetime

def print_banner():
    print("="*60)
    print("🚀 INICIALIZADOR ROBUSTO - FLASK API")
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔧 Resolvendo problemas de inicialização...")
    print("="*60)

def check_port(port, max_attempts=3):
    """Verifica se porta está livre com múltiplas tentativas"""
    for attempt in range(max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Porta livre
                return True
            else:
                print(f"⚠️  Porta {port} em uso, tentativa {attempt + 1}/{max_attempts}")
                if attempt < max_attempts - 1:
                    time.sleep(2)
        except Exception as e:
            print(f"❌ Erro ao verificar porta {port}: {e}")
            return False
    
    return False

def kill_conflicting_processes():
    """Mata processos que podem estar conflitando"""
    print("🔧 Limpando processos conflitantes...")
    
    processes_to_kill = [
        'flask',
        'streamlit', 
        'run_demo_api',
        'run.py',
        'demo.py'
    ]
    
    for process_name in processes_to_kill:
        try:
            subprocess.run(['pkill', '-f', process_name], 
                         capture_output=True, timeout=5)
            print(f"✅ Limpou processos: {process_name}")
        except:
            pass  # Ignorar erros
    
    time.sleep(2)  # Aguardar processos terminarem

def find_free_port(start_port=5000, max_attempts=10):
    """Encontra uma porta livre"""
    for port in range(start_port, start_port + max_attempts):
        if check_port(port):
            return port
    return None

def start_api_safe(port=5000):
    """Inicia API de forma segura"""
    print(f"🚀 Iniciando API na porta {port}...")
    
    try:
        # Mudar para diretório do projeto
        os.chdir('/home/ec2-user/hackatonaws')
        
        # Adicionar ao path
        sys.path.insert(0, '.')
        
        # Importar e configurar Flask
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        # Endpoints básicos
        @app.route('/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'message': 'API funcionando perfeitamente',
                'port': port,
                'timestamp': datetime.now().isoformat()
            })
        
        @app.route('/status')
        def status():
            return jsonify({
                'status': 'running',
                'mode': 'robust',
                'port': port,
                'endpoints': ['/health', '/status', '/test']
            })
        
        @app.route('/test')
        def test():
            return jsonify({
                'message': 'Teste bem-sucedido!',
                'working': True,
                'port': port
            })
        
        # Tentar importar endpoints do projeto original
        try:
            from run_demo_api import app as demo_app
            # Copiar rotas do app demo
            for rule in demo_app.url_map.iter_rules():
                if rule.endpoint not in ['static', 'health', 'status', 'test']:
                    try:
                        view_func = demo_app.view_functions[rule.endpoint]
                        app.add_url_rule(rule.rule, rule.endpoint, view_func, methods=rule.methods)
                        print(f"✅ Rota importada: {rule.rule}")
                    except:
                        pass
        except Exception as e:
            print(f"⚠️  Não foi possível importar rotas originais: {e}")
            print("✅ Continuando com endpoints básicos...")
        
        print(f"🌐 API disponível em: http://localhost:{port}")
        print(f"📋 Endpoints disponíveis:")
        print(f"   - GET  /health")
        print(f"   - GET  /status") 
        print(f"   - GET  /test")
        print(f"⏹️  Pressione Ctrl+C para parar")
        
        # Iniciar servidor
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        return False

def test_api(port, max_attempts=5):
    """Testa se a API está respondendo"""
    import requests
    
    print(f"🧪 Testando API na porta {port}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f'http://localhost:{port}/health', timeout=5)
            if response.status_code == 200:
                print(f"✅ API respondendo corretamente!")
                data = response.json()
                print(f"📊 Status: {data.get('status')}")
                return True
        except Exception as e:
            print(f"⚠️  Tentativa {attempt + 1}/{max_attempts}: {e}")
            time.sleep(2)
    
    return False

def main():
    """Função principal"""
    print_banner()
    
    try:
        # 1. Limpar processos conflitantes
        kill_conflicting_processes()
        
        # 2. Encontrar porta livre
        port = find_free_port()
        if not port:
            print("❌ Não foi possível encontrar porta livre")
            return False
        
        print(f"✅ Porta livre encontrada: {port}")
        
        # 3. Iniciar API
        print("🚀 Iniciando servidor Flask robusto...")
        start_api_safe(port)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
        return True
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def quick_start():
    """Início rápido sem diagnósticos"""
    os.chdir('/home/ec2-user/hackatonaws')
    
    # Encontrar porta livre
    port = find_free_port()
    if not port:
        port = 5003  # Fallback
    
    print(f"🚀 Início rápido na porta {port}")
    start_api_safe(port)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_start()
    else:
        success = main()
        sys.exit(0 if success else 1)
