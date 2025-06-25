#!/usr/bin/env python3
"""
Script para configurar credenciais AWS CLI no ambiente
"""

import os
import subprocess
import json
import sys

def get_aws_cli_credentials():
    """Obtém credenciais da AWS CLI"""
    print("🔍 Obtendo credenciais da AWS CLI...")
    
    try:
        # Tentar obter credenciais via aws configure
        result = subprocess.run([
            'aws', 'configure', 'list'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ AWS CLI configurado")
            print(result.stdout)
        else:
            print("⚠️  AWS CLI pode não estar configurado")
    
    except Exception as e:
        print(f"❌ Erro ao verificar AWS CLI: {e}")
    
    # Verificar credenciais atuais
    try:
        result = subprocess.run([
            'aws', 'sts', 'get-caller-identity'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            identity = json.loads(result.stdout)
            print(f"✅ Credenciais válidas")
            print(f"   Account: {identity.get('Account')}")
            print(f"   User: {identity.get('Arn')}")
            return True
        else:
            print(f"❌ Credenciais inválidas: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar credenciais: {e}")
        return False

def export_aws_credentials():
    """Exporta credenciais AWS para variáveis de ambiente"""
    print("\n🔧 Configurando variáveis de ambiente...")
    
    # Verificar se já estão configuradas
    env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN', 'AWS_DEFAULT_REGION']
    
    print("📋 Variáveis de ambiente atuais:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'KEY' in var or 'TOKEN' in var:
                print(f"   {var}: {value[:10]}...")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: NOT_SET")
    
    # Se não estão configuradas, tentar obter do AWS CLI
    if not all(os.getenv(var) for var in env_vars[:3]):  # Não incluir região na verificação obrigatória
        print("\n⚠️  Algumas credenciais não estão configuradas")
        print("💡 Para configurar manualmente:")
        print("   export AWS_ACCESS_KEY_ID=sua_access_key")
        print("   export AWS_SECRET_ACCESS_KEY=sua_secret_key")
        print("   export AWS_SESSION_TOKEN=seu_session_token")
        print("   export AWS_DEFAULT_REGION=us-east-1")
        return False
    
    return True

def create_env_file():
    """Cria arquivo .env com credenciais"""
    print("\n📝 Criando arquivo .env...")
    
    env_content = f"""# AWS Credentials from CLI
AWS_REGION={os.getenv('AWS_DEFAULT_REGION', 'us-east-1')}
AWS_ACCESS_KEY_ID={os.getenv('AWS_ACCESS_KEY_ID', '')}
AWS_SECRET_ACCESS_KEY={os.getenv('AWS_SECRET_ACCESS_KEY', '')}
AWS_SESSION_TOKEN={os.getenv('AWS_SESSION_TOKEN', '')}

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def test_bedrock_access():
    """Testa acesso ao Bedrock"""
    print("\n🧪 Testando acesso ao Bedrock...")
    
    try:
        result = subprocess.run([
            'aws', 'bedrock', 'list-foundation-models', '--region', 'us-east-1'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            models = json.loads(result.stdout)
            model_count = len(models.get('modelSummaries', []))
            print(f"✅ Acesso ao Bedrock OK - {model_count} modelos disponíveis")
            return True
        else:
            print(f"❌ Erro no Bedrock: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar Bedrock: {e}")
        return False

def show_next_steps():
    """Mostra próximos passos"""
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("="*50)
    
    print("1. **Testar app com credenciais AWS CLI:**")
    print("   python3 src/app_aws_cli.py")
    print()
    
    print("2. **Se der erro de token expirado:**")
    print("   aws sso login")
    print("   # ou")
    print("   aws configure")
    print()
    
    print("3. **Verificar se modelos Bedrock estão habilitados:**")
    print("   - Console AWS → Bedrock → Model Access")
    print("   - Habilitar: Claude 3 Sonnet e Titan Embeddings")
    print()
    
    print("4. **Testar API:**")
    print("   curl http://localhost:5000/health")

def main():
    """Função principal"""
    print("🔧 CONFIGURAÇÃO DE CREDENCIAIS AWS CLI")
    print("="*50)
    
    os.chdir('/home/ec2-user/hackatonaws')
    
    # Verificar AWS CLI
    if not get_aws_cli_credentials():
        print("\n❌ Configure AWS CLI primeiro:")
        print("   aws configure")
        print("   # ou")
        print("   aws sso login")
        return False
    
    # Verificar variáveis de ambiente
    if not export_aws_credentials():
        print("\n⚠️  Configure as variáveis de ambiente manualmente")
    
    # Criar arquivo .env
    create_env_file()
    
    # Testar Bedrock
    bedrock_ok = test_bedrock_access()
    
    # Mostrar próximos passos
    show_next_steps()
    
    if bedrock_ok:
        print("\n🎉 TUDO CONFIGURADO! Pode usar:")
        print("   python3 src/app_aws_cli.py")
    else:
        print("\n⚠️  Bedrock não acessível. Use modo demo:")
        print("   python3 run_demo_api.py")
    
    return bedrock_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
