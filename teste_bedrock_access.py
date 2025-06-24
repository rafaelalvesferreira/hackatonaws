#!/usr/bin/env python3
"""
Teste de acesso ao Amazon Bedrock
"""

import boto3
import os
import sys
from dotenv import load_dotenv

def test_bedrock_access():
    """Testa acesso ao Bedrock"""
    print("🔍 TESTANDO ACESSO AO AMAZON BEDROCK")
    print("="*50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar credenciais
    print("📋 Verificando credenciais...")
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    session_token = os.getenv('AWS_SESSION_TOKEN')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print(f"   ACCESS_KEY: {'✅ SET' if access_key else '❌ MISSING'}")
    print(f"   SECRET_KEY: {'✅ SET' if secret_key else '❌ MISSING'}")
    print(f"   SESSION_TOKEN: {'✅ SET' if session_token else '❌ MISSING'}")
    print(f"   REGION: {region}")
    
    if not access_key or not secret_key:
        print("\n❌ Credenciais básicas faltando!")
        return False
    
    # Teste 1: STS (verificar se credenciais funcionam)
    print(f"\n🧪 Teste 1: Verificando credenciais com STS...")
    try:
        sts_client = boto3.client('sts', region_name=region)
        identity = sts_client.get_caller_identity()
        print(f"   ✅ Credenciais válidas")
        print(f"   👤 User ARN: {identity.get('Arn', 'N/A')}")
        print(f"   🆔 Account: {identity.get('Account', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Erro nas credenciais: {e}")
        return False
    
    # Teste 2: Bedrock - Listar modelos
    print(f"\n🧪 Teste 2: Listando modelos Bedrock...")
    try:
        bedrock_client = boto3.client('bedrock', region_name=region)
        models = bedrock_client.list_foundation_models()
        model_count = len(models['modelSummaries'])
        print(f"   ✅ Acesso ao Bedrock OK")
        print(f"   📊 Modelos disponíveis: {model_count}")
        
        # Verificar modelos específicos
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        titan_models = [m for m in models['modelSummaries'] if 'titan' in m['modelId'].lower()]
        
        print(f"   🤖 Modelos Claude: {len(claude_models)}")
        print(f"   🔗 Modelos Titan: {len(titan_models)}")
        
    except Exception as e:
        print(f"   ❌ Erro ao acessar Bedrock: {e}")
        if "AccessDenied" in str(e):
            print("   💡 Possível causa: Modelos não habilitados no Console AWS")
        elif "UnauthorizedOperation" in str(e):
            print("   💡 Possível causa: Permissões IAM insuficientes")
        return False
    
    # Teste 3: Bedrock Runtime - Embeddings
    print(f"\n🧪 Teste 3: Testando embeddings...")
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # Testar embedding com Titan
        response = bedrock_runtime.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body='{"inputText": "teste"}'
        )
        print(f"   ✅ Embeddings funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro nos embeddings: {e}")
        if "AccessDenied" in str(e):
            print("   💡 Modelo Titan não habilitado")
        return False
    
    # Teste 4: Claude 3
    print(f"\n🧪 Teste 4: Testando Claude 3...")
    try:
        import json
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Olá, você está funcionando?"
                }
            ]
        })
        
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        print(f"   ✅ Claude 3 funcionando")
        
    except Exception as e:
        print(f"   ❌ Erro no Claude 3: {e}")
        if "AccessDenied" in str(e):
            print("   💡 Modelo Claude 3 não habilitado")
        return False
    
    print(f"\n🎉 TODOS OS TESTES PASSARAM!")
    print(f"✅ Bedrock está totalmente funcional")
    return True

def show_solutions():
    """Mostra soluções para problemas comuns"""
    print(f"\n🛠️  SOLUÇÕES PARA PROBLEMAS COMUNS")
    print("="*50)
    
    print("1. **Modelos não habilitados:**")
    print("   - Acesse AWS Console → Bedrock → Model Access")
    print("   - Habilite: Claude 3 Sonnet e Titan Embeddings")
    print()
    
    print("2. **Permissões IAM:**")
    print("   - Adicione política com bedrock:InvokeModel")
    print("   - Adicione bedrock:ListFoundationModels")
    print()
    
    print("3. **Região não suportada:**")
    print("   - Use: us-east-1, us-west-2, ou eu-west-1")
    print()
    
    print("4. **Credenciais temporárias:**")
    print("   - Verifique se AWS_SESSION_TOKEN está configurado")
    print("   - Renove credenciais se expiradas")

def main():
    """Função principal"""
    os.chdir('/home/ec2-user/hackatonaws')
    
    success = test_bedrock_access()
    
    if not success:
        show_solutions()
        print(f"\n💡 ENQUANTO ISSO, USE MODO DEMO:")
        print(f"   python3 run_demo_api.py")
        print(f"   python3 src/app_com_fallback.py")
    else:
        print(f"\n🚀 PODE USAR BEDROCK REAL:")
        print(f"   python3 run.py")
        print(f"   python3 src/app.py")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
