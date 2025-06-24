#!/usr/bin/env python3
"""
Debug específico para falha "após 20 tentativas"
"""

import os
import sys
import subprocess
import time
import signal

def find_failing_script():
    """Encontra qual script está falhando"""
    print("🔍 INVESTIGANDO FALHA 'APÓS 20 TENTATIVAS'")
    print("="*50)
    
    # Scripts que podem estar causando o problema
    scripts_to_check = [
        'demo.py',
        'run_streamlit.py', 
        'start_demo.py',
        'start_and_test.py'
    ]
    
    for script in scripts_to_check:
        if os.path.exists(script):
            print(f"\n🔍 Verificando: {script}")
            
            # Ler o script e procurar por loops de tentativas
            try:
                with open(script, 'r') as f:
                    content = f.read()
                    
                # Procurar por padrões que indicam tentativas
                patterns = [
                    'tentativa', 'attempt', 'retry', 'for i in range',
                    'while', 'max_attempts', '20'
                ]
                
                found_patterns = []
                for pattern in patterns:
                    if pattern.lower() in content.lower():
                        found_patterns.append(pattern)
                
                if found_patterns:
                    print(f"⚠️  Padrões encontrados: {found_patterns}")
                    
                    # Mostrar linhas relevantes
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if any(p.lower() in line.lower() for p in patterns):
                            print(f"   Linha {i}: {line.strip()}")
                else:
                    print(f"✅ Nenhum padrão de tentativas encontrado")
                    
            except Exception as e:
                print(f"❌ Erro ao ler {script}: {e}")

def check_running_processes():
    """Verifica processos rodando que podem estar em loop"""
    print(f"\n🔍 PROCESSOS PYTHON RODANDO")
    print("="*50)
    
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        python_processes = []
        for line in lines:
            if 'python' in line and 'hackatonaws' in line:
                python_processes.append(line)
        
        if python_processes:
            print("⚠️  Processos Python relacionados ao projeto:")
            for proc in python_processes:
                print(f"   {proc}")
        else:
            print("✅ Nenhum processo Python do projeto rodando")
            
    except Exception as e:
        print(f"❌ Erro ao verificar processos: {e}")

def check_logs():
    """Verifica se há logs de erro"""
    print(f"\n🔍 VERIFICANDO LOGS")
    print("="*50)
    
    log_files = [
        'flask.log',
        'error.log',
        'debug.log',
        'streamlit.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"📄 Encontrado: {log_file}")
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"   Últimas linhas:")
                        for line in lines[-5:]:
                            print(f"   {line.strip()}")
            except:
                pass
        else:
            print(f"❌ Não encontrado: {log_file}")

def create_safe_starter():
    """Cria um iniciador seguro"""
    print(f"\n🔧 CRIANDO INICIADOR SEGURO")
    print("="*50)
    
    safe_starter = '''#!/usr/bin/env python3
"""
Iniciador seguro - Sem loops infinitos
"""

import os
import sys
import time

def start_single_api():
    """Inicia apenas uma API, sem tentativas múltiplas"""
    print("🚀 Iniciando API única e segura...")
    
    os.chdir('/home/ec2-user/hackatonaws')
    sys.path.insert(0, '.')
    
    try:
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/health')
        def health():
            return jsonify({'status': 'ok', 'message': 'API segura funcionando'})
        
        @app.route('/safe')
        def safe():
            return jsonify({'safe': True, 'message': 'Sem loops infinitos!'})
        
        print("✅ API segura iniciada em http://localhost:5010")
        print("⏹️  Pressione Ctrl+C para parar")
        
        app.run(host='0.0.0.0', port=5010, debug=False)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_single_api()
'''
    
    with open('api_segura.py', 'w') as f:
        f.write(safe_starter)
    
    print("✅ Criado: api_segura.py")
    print("🚀 Execute: python3 api_segura.py")

def kill_all_related():
    """Mata todos os processos relacionados"""
    print(f"\n🛑 MATANDO PROCESSOS RELACIONADOS")
    print("="*50)
    
    processes = [
        'demo.py',
        'run_streamlit.py',
        'start_demo.py', 
        'streamlit',
        'flask',
        'run_demo_api'
    ]
    
    for proc in processes:
        try:
            subprocess.run(['pkill', '-f', proc], capture_output=True)
            print(f"✅ Matou processos: {proc}")
        except:
            pass
    
    time.sleep(2)
    print("✅ Limpeza concluída")

def main():
    """Executa debug completo"""
    os.chdir('/home/ec2-user/hackatonaws')
    
    find_failing_script()
    check_running_processes() 
    check_logs()
    kill_all_related()
    create_safe_starter()
    
    print(f"\n🎯 RESUMO E SOLUÇÕES")
    print("="*50)
    print("1. ✅ Scripts verificados")
    print("2. ✅ Processos limpos") 
    print("3. ✅ API segura criada")
    print()
    print("🚀 PRÓXIMOS PASSOS:")
    print("   python3 api_segura.py      # API sem loops")
    print("   python3 start_flask_robusto.py  # Versão robusta")
    print("   python3 run_demo_api.py    # Original (se funcionar)")

if __name__ == "__main__":
    main()
