# pdf_tools.py
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from fpdf import FPDF
from datetime import datetime
import gradio as gr
from NexusEducation_Ferramenta.utils import gerar_timestamp

def analisar_documentos(arquivo):
    converter = DocumentConverter()
    textos = ""
    # Converte o PDF e agrega conteúdo
    if not arquivo:
        return "Nenhum arquivo enviado."
    res = converter.convert(arquivo.name)
    doc = res.document
    texto = doc.export_to_markdown()
    textos += texto + "\n\n"
    # Chama o modelo de linguagem para gerar uma resposta
    prompt = f"Resuma o conteúdo do documento:\n{textos}, e faça uma análise semântica a análise semântica deve ser feita apenas do (conteúdo programático) se não tiver apenas faça o resumo dos documentos"
    resposta = Settings.llm.complete(prompt)
    return resposta.text

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
