#!/usr/bin/env python3
"""
Script de instalação limpa para resolver conflitos de dependências
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            return True
        else:
            print(f"❌ {description} - Erro:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def main():
    """Instalação limpa das dependências"""
    print("🚀 INSTALAÇÃO LIMPA - BEDROCK DOCUMENT AGENT")
    print("=" * 60)
    print("Resolvendo conflitos de dependências...")
    
    # Mudar para diretório do projeto
    os.chdir('/home/ec2-user/hackatonaws')
    
    steps = [
        # 1. Limpeza
        ("python3 -m pip cache purge", "Limpando cache do pip"),
        
        # 2. Dependências básicas
        ("python3 -m pip install flask==2.3.3 flask-cors==4.0.0", "Instalando Flask"),
        ("python3 -m pip install boto3 python-dotenv requests", "Instalando AWS SDK e utilitários"),
        
        # 3. Processamento de documentos
        ("python3 -m pip install PyPDF2==3.0.1 python-docx==0.8.11", "Instalando processadores de documento"),
        
        # 4. LangChain (sem versões específicas para evitar conflitos)
        ("python3 -m pip install langchain-core", "Instalando LangChain Core"),
        ("python3 -m pip install langchain-aws", "Instalando LangChain AWS"),
        ("python3 -m pip install langchain-community", "Instalando LangChain Community"),
        ("python3 -m pip install langchain", "Instalando LangChain principal"),
        
        # 5. Vector store
        ("python3 -m pip install faiss-cpu==1.7.4", "Instalando FAISS"),
        
        # 6. Interface web (opcional)
        ("python3 -m pip install streamlit pandas", "Instalando Streamlit"),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for cmd, description in steps:
        if run_command(cmd, description):
            success_count += 1
        time.sleep(1)  # Pequena pausa entre instalações
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DA INSTALAÇÃO")
    print("=" * 60)
    print(f"Passos concluídos: {success_count}/{total_steps}")
    
    if success_count == total_steps:
        print("\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        
        # Teste das importações
        print("\n🧪 Testando importações críticas...")
        test_imports()
        
        print("\n✅ PRÓXIMOS PASSOS:")
        print("1. Execute: python3 test_basic.py")
        print("2. Para modo demo: python3 run_demo_api.py")
        print("3. Configure AWS no .env para modo completo")
        
    else:
        print(f"\n⚠️  {total_steps - success_count} passos falharam")
        print("Verifique os erros acima e tente novamente")
    
    return success_count == total_steps

def test_imports():
    """Testa as importações principais"""
    imports_to_test = [
        ("flask", "Flask"),
        ("boto3", "AWS SDK"),
        ("PyPDF2", "PDF processor"),
        ("docx", "Word processor"),
        ("langchain_community.vectorstores", "FAISS"),
        ("langchain_aws", "BedrockEmbeddings"),
        ("langchain_core.documents", "Document"),
        ("langchain_text_splitters", "RecursiveCharacterTextSplitter"),
    ]
    
    success = 0
    for module, name in imports_to_test:
        try:
            __import__(module)
            print(f"  ✅ {name}")
            success += 1
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
    
    print(f"\nImportações: {success}/{len(imports_to_test)} funcionando")
    return success == len(imports_to_test)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
