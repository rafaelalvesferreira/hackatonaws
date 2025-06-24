#!/usr/bin/env python3
"""
Script para testar a API do Agente de Documentos
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:5000"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_status():
    """Testa o endpoint de status"""
    print("\n📊 Testando Status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_upload_documents():
    """Testa o upload/processamento de documentos"""
    print("\n📄 Testando Upload de Documentos...")
    try:
        response = requests.post(f"{BASE_URL}/documents/upload")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_chat(message):
    """Testa o endpoint de chat"""
    print(f"\n💬 Testando Chat: '{message}'")
    try:
        payload = {
            "message": message,
            "max_results": 3,
            "similarity_threshold": 0.7
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print("✅ Resposta do Agente:")
            print(f"   {result.get('response', 'Sem resposta')}")
            print(f"   Fontes: {result.get('sources', [])}")
            print(f"   Documentos usados: {result.get('documents_used', 0)}")
        else:
            print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DA API - AGENTE DE DOCUMENTOS BEDROCK")
    print("=" * 60)
    
    # Lista de testes
    tests = [
        ("Health Check", test_health),
        ("Status", test_status),
        ("Upload Documentos", test_upload_documents),
    ]
    
    # Executa testes básicos
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Pausa entre testes
    
    # Testes de chat (apenas se os testes básicos passaram)
    if all(result for _, result in results):
        print("\n" + "=" * 60)
        print("🤖 TESTANDO CHAT COM O AGENTE")
        print("=" * 60)
        
        chat_messages = [
            "Olá! Como você pode me ajudar?",
            "Quais documentos você tem acesso?",
            "Me fale sobre o conteúdo dos documentos disponíveis",
            "Resuma as principais informações que você encontrou"
        ]
        
        for message in chat_messages:
            test_chat(message)
            time.sleep(2)  # Pausa entre mensagens
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    total_passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {total_passed}/{len(results)} testes passaram")
    
    if total_passed == len(results):
        print("🎉 Todos os testes passaram! API funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração.")

if __name__ == '__main__':
    main()
