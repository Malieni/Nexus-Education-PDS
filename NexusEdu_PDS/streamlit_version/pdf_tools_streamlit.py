from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from fpdf import FPDF
from datetime import datetime
import streamlit as st
import json
import tempfile
import os

def analisar_documentos(arquivo):
    """Analisa um documento PDF usando IA"""
    if not arquivo:
        return "Nenhum arquivo enviado."
    
    try:
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(arquivo.getvalue())
            tmp_path = tmp_file.name
        
        converter = DocumentConverter()
        res = converter.convert(tmp_path)
        doc = res.document
        texto = doc.export_to_markdown()
        
        # Remove o arquivo temporário
        os.unlink(tmp_path)
        
        # Prompt para a IA
        prompt = (
            "Analise o seguinte conteúdo extraído de um PDF de ementa de disciplina. "
            "Resuma o conteúdo, destaque pontos importantes e faça uma análise semântica do conteúdo programático. "
            "Se não houver conteúdo programático, apenas faça o resumo.\n\n"
            f"Conteúdo extraído:\n{texto}"
        )
        resposta = Settings.llm.complete(prompt)
        return resposta.text
    except Exception as e:
        return f"Erro ao processar o PDF: {e}"

def add_historico(resposta, historico_estado):
    """Adiciona uma resposta ao histórico"""
    if resposta:
        historico_estado.append(resposta)
        return historico_estado
    return historico_estado

def gerar_pdf(historico_estado):
    """Gera um PDF com o histórico de análises"""
    if not historico_estado:
        st.error("Nenhum dado para adicionar ao PDF.")
        return None
    
    try:
        timestamp = gerar_timestamp()
        caminho_pdf = f"relatorio_perguntas_respostas_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Adiciona título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Relatório de Análises de Ementas", ln=True, align='C')
        pdf.ln(10)
        
        # Adiciona cada análise
        for i, resposta in enumerate(historico_estado, 1):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, txt=f"Análise {i}", ln=True)
            pdf.set_font("Arial", '', 10)
            
            # Quebra o texto em linhas para caber na página
            linhas = resposta.split('\n')
            for linha in linhas:
                if len(linha) > 80:  # Se a linha for muito longa
                    palavras = linha.split()
                    linha_atual = ""
                    for palavra in palavras:
                        if len(linha_atual + palavra) < 80:
                            linha_atual += palavra + " "
                        else:
                            pdf.multi_cell(0, 5, txt=linha_atual.strip())
                            linha_atual = palavra + " "
                    if linha_atual:
                        pdf.multi_cell(0, 5, txt=linha_atual.strip())
                else:
                    pdf.multi_cell(0, 5, txt=linha)
            
            pdf.ln(5)
        
        pdf.output(caminho_pdf)
        return caminho_pdf
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return None

def resetar_aplicacao():
    """Reseta a aplicação"""
    return "A aplicação foi resetada. Por favor, faça upload de um novo arquivo."
