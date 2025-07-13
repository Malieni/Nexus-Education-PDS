# pdf_tools.py
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from fpdf import FPDF
from datetime import datetime
import gradio as gr
from utils import gerar_timestamp
import json

def analisar_documentos(arquivo):
    if not arquivo:
        return "Nenhum arquivo enviado."
    try:
        converter = DocumentConverter()
        res = converter.convert(arquivo.name)
        doc = res.document
        texto = doc.export_to_markdown()
        
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
    if resposta:
        historico_estado.append((resposta))
        gr.Info("Adicionado ao PDF!", duration=2)
        return historico_estado

def gerar_pdf(historico_estado):
    if not historico_estado:
        return "Nenhum dado para adicionar ao PDF.", None
    timestamp = gerar_timestamp()
    caminho_pdf = f"relatorio_perguntas_respostas_{timestamp}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    for resposta in historico_estado:
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, txt=resposta)
        pdf.ln(6)
    pdf.output(caminho_pdf)
    return caminho_pdf

def resetar_aplicação():
    return None, "A aplicação foi resetada. Por favor, faça upload de um novo arquivo."
