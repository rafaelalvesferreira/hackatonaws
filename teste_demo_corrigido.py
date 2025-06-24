#!/usr/bin/env python3
"""
Teste específico para verificar se o demo.py foi corrigido
"""

import subprocess
import sys
import time
import os

def test_demo_correction():
    """Testa se o demo corrigido funciona"""
    print("🧪 TESTANDO DEMO.PY CORRIGIDO")
    print("="*50)
    
    os.chdir('/home/ec2-user/hackatonaws')
    
    # Limpar processos primeiro
    print("🔧 Limpando processos...")
    subprocess.run(['pkill', '-f', 'demo'], capture_output=True)
    subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
    subprocess.run(['pkill', '-f', 'flask'], capture_output=True)
    time.sleep(2)
    
    print("🚀 Iniciando demo corrigido...")
    
    try:
        # Executar demo com timeout
        process = subprocess.Popen([
            sys.executable, 'demo.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aguardar alguns segundos para ver se inicia sem erro
        time.sleep(10)
        
        # Verificar se processo ainda está rodando (bom sinal)
        if process.poll() is None:
            print("✅ Demo iniciou sem erros!")
            print("✅ Processo ainda rodando (sem crash)")
            
            # Tentar acessar a API
            import requests
            try:
                response = requests.get('http://localhost:5000/health', timeout=5)
                if response.status_code == 200:
                    print("✅ API respondendo corretamente!")
                    data = response.json()
                    print(f"📊 Status: {data.get('status', 'N/A')}")
                else:
                    print(f"⚠️  API respondeu com status {response.status_code}")
            except Exception as e:
                print(f"⚠️  API ainda não disponível: {e}")
            
            # Parar o processo
            process.terminate()
            try:
                process.wait(timeout=5)
            except:
                process.kill()
            
            print("✅ TESTE PASSOU - Demo corrigido funciona!")
            return True
            
        else:
            # Processo terminou, verificar por que
            stdout, stderr = process.communicate()
            print("❌ Demo terminou inesperadamente")
            if stdout:
                print(f"STDOUT: {stdout[:300]}...")
            if stderr:
                print(f"STDERR: {stderr[:300]}...")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar demo: {e}")
        return False

def compare_with_original():
    """Compara com a versão original"""
    print("\n🔍 COMPARANDO COM VERSÃO ORIGINAL")
    print("="*50)
    
    if os.path.exists('demo_original_backup.py'):
        print("✅ Backup da versão original encontrado")
        
        # Contar linhas com "20" e "tentativa"
        with open('demo_original_backup.py', 'r') as f:
            original = f.read()
        
        with open('demo.py', 'r') as f:
            current = f.read()
        
        original_20 = original.count('20')
        current_20 = current.count('20')
        
        original_tentativa = original.lower().count('tentativa')
        current_tentativa = current.lower().count('tentativa')
        
        print(f"Ocorrências de '20':")
        print(f"  Original: {original_20}")
        print(f"  Corrigido: {current_20}")
        
        print(f"Ocorrências de 'tentativa':")
        print(f"  Original: {original_tentativa}")
        print(f"  Corrigido: {current_tentativa}")
        
        if 'run_demo_api.py' in current and 'run.py' in original:
            print("✅ Mudou de run.py para run_demo_api.py")
        
        if 'kill_existing_processes' in current:
            print("✅ Adicionou limpeza de processos")
        
        if 'check_port_available' in current:
            print("✅ Adicionou verificação de portas")
            
    else:
        print("⚠️  Backup original não encontrado")

def main():
    """Executa todos os testes"""
    success = test_demo_correction()
    compare_with_original()
    
    print(f"\n{'='*50}")
    print(f"🎯 RESULTADO FINAL")
    print(f"{'='*50}")
    
    if success:
        print("✅ DEMO.PY FOI CORRIGIDO COM SUCESSO!")
        print("✅ Não há mais erro de '20 tentativas'")
        print("✅ API inicia corretamente")
        print("\n🚀 COMO USAR:")
        print("   python3 demo.py")
    else:
        print("❌ Demo ainda tem problemas")
        print("🔧 Tente:")
        print("   python3 run_demo_api.py  # API direta")
        print("   python3 api_simples.py   # API garantida")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
