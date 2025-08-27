#!/usr/bin/env python3
"""
Script para executar a aplicação Nexus Education PDS com Streamlit
"""

import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Nexus Education PDS com Streamlit...")
    print()
    
    # Verifica se o Streamlit está instalado
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} encontrado")
    except ImportError:
        print("❌ Streamlit não encontrado!")
        print("Instale com: pip install streamlit")
        return
    
    # Verifica se o arquivo principal existe
    if not os.path.exists("app_streamlit.py"):
        print("❌ Arquivo app_streamlit.py não encontrado!")
        print("Certifique-se de executar este script da pasta streamlit_version")
        return
    
    print("✅ Arquivo principal encontrado")
    print()
    print("🌐 Abrindo aplicação no navegador...")
    print("📱 A aplicação estará disponível em: http://localhost:8501")
    print()
    print("Para parar a aplicação, pressione Ctrl+C")
    print()
    
    try:
        # Executa o Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_streamlit.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

if __name__ == "__main__":
    main()
