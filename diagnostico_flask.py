#!/usr/bin/env python3
"""
Diagnóstico de problemas com Flask
"""

import os
import sys
import socket
import subprocess
import time
import requests

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_port(port):
    """Verifica se uma porta está disponível"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # True se porta está livre
    except:
        return True

def check_imports():
    """Verifica se as importações necessárias funcionam"""
    print_header("VERIFICANDO IMPORTAÇÕES")
    
    imports = [
        ('flask', 'Flask'),
        ('flask_cors', 'CORS'),
        ('config.settings', 'Config'),
        ('src.app', 'App principal')
    ]
    
    success = 0
    for module, name in imports:
        try:
            __import__(module)
            print(f"✅ {name}")
            success += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    return success == len(imports)

def check_ports():
    """Verifica disponibilidade das portas"""
    print_header("VERIFICANDO PORTAS")
    
    ports = [5000, 8501, 8502]
    available = []
    
    for port in ports:
        if check_port(port):
            print(f"✅ Porta {port}: Livre")
            available.append(port)
        else:
            print(f"❌ Porta {port}: Em uso")
    
    return available

def check_config():
    """Verifica configuração"""
    print_header("VERIFICANDO CONFIGURAÇÃO")
    
    try:
        sys.path.insert(0, '/home/ec2-user/hackatonaws')
        from config.settings import Config
        
        print(f"✅ Flask Host: {Config.FLASK_HOST}")
        print(f"✅ Flask Port: {Config.FLASK_PORT}")
        print(f"✅ Debug Mode: {Config.FLASK_DEBUG}")
        print(f"✅ Documents Path: {Config.DOCUMENTS_PATH}")
        
        # Verificar se diretórios existem
        if os.path.exists(Config.DOCUMENTS_PATH):
            print(f"✅ Diretório de documentos existe")
        else:
            print(f"❌ Diretório de documentos não existe: {Config.DOCUMENTS_PATH}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def test_simple_flask():
    """Testa Flask simples"""
    print_header("TESTANDO FLASK SIMPLES")
    
    try:
        # Criar app Flask mínimo
        test_code = '''
import sys
sys.path.insert(0, "/home/ec2-user/hackatonaws")
from flask import Flask
app = Flask(__name__)

@app.route("/test")
def test():
    return {"status": "ok", "message": "Flask funcionando"}

if __name__ == "__main__":
    print("Iniciando Flask de teste...")
    app.run(host="0.0.0.0", port=5001, debug=False)
'''
        
        # Salvar código de teste
        with open('/tmp/test_flask.py', 'w') as f:
            f.write(test_code)
        
        # Executar em background
        process = subprocess.Popen([
            sys.executable, '/tmp/test_flask.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguardar um pouco
        time.sleep(3)
        
        # Testar se responde
        try:
            response = requests.get('http://localhost:5001/test', timeout=5)
            if response.status_code == 200:
                print("✅ Flask básico funcionando")
                result = True
            else:
                print(f"❌ Flask respondeu com status {response.status_code}")
                result = False
        except Exception as e:
            print(f"❌ Erro ao testar Flask: {e}")
            result = False
        
        # Parar processo
        process.terminate()
        process.wait()
        
        return result
        
    except Exception as e:
        print(f"❌ Erro no teste Flask: {e}")
        return False

def check_system_resources():
    """Verifica recursos do sistema"""
    print_header("VERIFICANDO RECURSOS DO SISTEMA")
    
    try:
        # Memória
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemAvailable' in line:
                    mem_kb = int(line.split()[1])
                    mem_mb = mem_kb // 1024
                    print(f"✅ Memória disponível: {mem_mb} MB")
                    break
        
        # Espaço em disco
        import shutil
        total, used, free = shutil.disk_usage('/')
        free_gb = free // (1024**3)
        print(f"✅ Espaço livre: {free_gb} GB")
        
        # Load average
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()[0]
            print(f"✅ Load average: {load}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar recursos: {e}")
        return False

def suggest_solutions():
    """Sugere soluções baseadas no diagnóstico"""
    print_header("SOLUÇÕES SUGERIDAS")
    
    print("🔧 SOLUÇÕES POSSÍVEIS:")
    print()
    print("1. **Usar porta diferente:**")
    print("   export FLASK_PORT=5001")
    print("   python3 run_demo_api.py")
    print()
    print("2. **Matar processos conflitantes:**")
    print("   pkill -f flask")
    print("   pkill -f streamlit")
    print()
    print("3. **Reiniciar com configuração limpa:**")
    print("   cd /home/ec2-user/hackatonaws")
    print("   python3 -c \"")
    print("   from flask import Flask")
    print("   app = Flask(__name__)")
    print("   app.run(host='0.0.0.0', port=5002)\"")
    print()
    print("4. **Usar script simplificado:**")
    print("   python3 diagnostico_flask.py --fix")
    print()
    print("5. **Verificar logs detalhados:**")
    print("   python3 run_demo_api.py 2>&1 | tee flask.log")

def create_simple_api():
    """Cria uma API Flask simples que funciona"""
    print_header("CRIANDO API SIMPLES")
    
    simple_api = '''#!/usr/bin/env python3
"""
API Flask Simples - Garantida para funcionar
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API Flask simples funcionando',
        'port': 5002
    })

@app.route('/test')
def test():
    return jsonify({
        'message': 'Teste bem-sucedido!',
        'working': True
    })

if __name__ == '__main__':
    print("🚀 Iniciando API Flask Simples...")
    print("🌐 Disponível em: http://localhost:5002")
    print("📋 Endpoints: /health, /test")
    print("⏹️  Pressione Ctrl+C para parar")
    
    app.run(
        host='0.0.0.0',
        port=5002,
        debug=False
    )
'''
    
    with open('/home/ec2-user/hackatonaws/api_simples.py', 'w') as f:
        f.write(simple_api)
    
    print("✅ API simples criada: api_simples.py")
    print("🚀 Execute: python3 api_simples.py")

def main():
    """Executa diagnóstico completo"""
    print("🔍 DIAGNÓSTICO COMPLETO DO FLASK")
    print("="*60)
    
    os.chdir('/home/ec2-user/hackatonaws')
    
    results = []
    
    # Executar testes
    tests = [
        ("Importações", check_imports),
        ("Portas", lambda: len(check_ports()) > 0),
        ("Configuração", check_config),
        ("Recursos do Sistema", check_system_resources),
        ("Flask Simples", test_simple_flask)
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro no teste {name}: {e}")
            results.append((name, False))
    
    # Resumo
    print_header("RESUMO DO DIAGNÓSTICO")
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nTestes passaram: {passed}/{len(results)}")
    
    # Sugestões
    suggest_solutions()
    
    # Criar API simples
    create_simple_api()
    
    return passed == len(results)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        create_simple_api()
        print("\n🚀 Execute agora: python3 api_simples.py")
    else:
        main()
