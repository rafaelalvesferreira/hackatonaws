#!/usr/bin/env python3
"""
Teste da API em modo demonstração
"""

import requests
import json
import time
import sys

def test_api_endpoint(url, method='GET', data=None):
    """Testa um endpoint da API"""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Conexão recusada - API não está rodando'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Testa todos os endpoints da API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testando API em Modo Demonstração")
    print("=" * 50)
    
    # Lista de testes
    tests = [
        {
            'name': 'Health Check',
            'url': f'{base_url}/health',
            'method': 'GET'
        },
        {
            'name': 'Status do Sistema',
            'url': f'{base_url}/status',
            'method': 'GET'
        },
        {
            'name': 'Listar Documentos',
            'url': f'{base_url}/documents/list',
            'method': 'GET'
        },
        {
            'name': 'Processar Documentos',
            'url': f'{base_url}/documents/upload',
            'method': 'POST'
        },
        {
            'name': 'Chat com Agente',
            'url': f'{base_url}/chat',
            'method': 'POST',
            'data': {
                'message': 'Olá! Como você pode me ajudar?',
                'max_results': 5
            }
        }
    ]
    
    # Executar testes
    results = []
    for test in tests:
        print(f"\n🔍 Testando: {test['name']}")
        print(f"   URL: {test['url']}")
        
        result = test_api_endpoint(
            test['url'], 
            test['method'], 
            test.get('data')
        )
        
        if result['success']:
            if result['status_code'] == 200:
                print(f"   ✅ Sucesso (200)")
                if isinstance(result['data'], dict):
                    if 'mode' in result['data']:
                        print(f"   📋 Modo: {result['data']['mode']}")
                    if 'message' in result['data']:
                        print(f"   💬 Mensagem: {result['data']['message']}")
            else:
                print(f"   ⚠️  Status: {result['status_code']}")
        else:
            print(f"   ❌ Erro: {result['error']}")
        
        results.append({
            'test': test['name'],
            'success': result['success'],
            'details': result
        })
        
        time.sleep(0.5)  # Pequena pausa entre testes
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{result['test']:20} {status}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        print("✅ A API está funcionando corretamente em modo demo")
        print("\n💡 Próximos passos:")
        print("   1. Configure credenciais AWS no .env")
        print("   2. Execute: python3 run.py")
        print("   3. Teste com credenciais reais")
    else:
        print(f"\n⚠️  {total - passed} testes falharam")
        print("🔧 Verifique se a API está rodando: python3 run_demo_api.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
