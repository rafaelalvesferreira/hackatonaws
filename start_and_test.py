#!/usr/bin/env python3
"""
Script para iniciar API demo e testar automaticamente
"""

import subprocess
import time
import requests
import json
import signal
import sys
import os

def start_api():
    """Inicia a API em background"""
    print("🚀 Iniciando API em modo demo...")
    
    # Mudar para diretório do projeto
    os.chdir('/home/ec2-user/hackatonaws')
    
    # Iniciar API
    process = subprocess.Popen(
        [sys.executable, 'run_demo_api.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

def wait_for_api(max_attempts=10):
    """Aguarda a API ficar disponível"""
    print("⏳ Aguardando API ficar disponível...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://localhost:5000/health', timeout=2)
            if response.status_code == 200:
                print("✅ API está rodando!")
                return True
        except:
            pass
        
        print(f"   Tentativa {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    return False

def test_endpoints():
    """Testa os endpoints da API"""
    print("\n🧪 Testando endpoints...")
    
    tests = [
        ('Health Check', 'GET', '/health', None),
        ('Status', 'GET', '/status', None),
        ('Listar Documentos', 'GET', '/documents/list', None),
        ('Processar Documentos', 'POST', '/documents/upload', {}),
        ('Chat', 'POST', '/chat', {'message': 'Olá, como você pode me ajudar?'})
    ]
    
    results = []
    base_url = 'http://localhost:5000'
    
    for name, method, endpoint, data in tests:
        print(f"\n🔍 Testando: {name}")
        
        try:
            if method == 'GET':
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", json=data, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Sucesso (200)")
                result_data = response.json()
                
                if 'mode' in result_data:
                    print(f"   📋 Modo: {result_data['mode']}")
                if 'message' in result_data:
                    print(f"   💬 {result_data['message'][:100]}...")
                
                results.append((name, True))
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                results.append((name, False))
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results.append((name, False))
    
    return results

def print_summary(results):
    """Imprime resumo dos testes"""
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        print("✅ A API está funcionando corretamente")
    else:
        print(f"\n⚠️  {total - passed} testes falharam")

def main():
    """Função principal"""
    print("🤖 TESTE AUTOMÁTICO DA API DEMO")
    print("="*40)
    
    # Iniciar API
    api_process = start_api()
    
    try:
        # Aguardar API ficar disponível
        if not wait_for_api():
            print("❌ API não ficou disponível")
            return False
        
        # Testar endpoints
        results = test_endpoints()
        
        # Mostrar resumo
        print_summary(results)
        
        # Manter API rodando por um tempo para testes manuais
        print("\n🌐 API rodando em: http://localhost:5000")
        print("📝 Você pode testar manualmente agora")
        print("⏹️  Pressione Ctrl+C para parar")
        
        # Aguardar interrupção do usuário
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando API...")
        
        return all(success for _, success in results)
        
    finally:
        # Parar API
        api_process.terminate()
        api_process.wait()
        print("✅ API parada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
