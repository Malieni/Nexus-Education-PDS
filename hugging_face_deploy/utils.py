# utils.py
# Utilitários do pacote NexusEducation_Ferramenta
from datetime import datetime

def gerar_timestamp():
    """Gera um timestamp formatado para nomes de arquivos."""
    return datetime.now().strftime("%Y%m%d%H%M%S")
