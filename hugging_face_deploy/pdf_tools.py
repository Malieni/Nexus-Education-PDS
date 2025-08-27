from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from fpdf import FPDF
from datetime import datetime
import gradio as gr
from utils import gerar_timestamp
import json
import os

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
    try:
        if resposta and resposta.strip():
            if historico_estado is None:
                historico_estado = []
            
            # Adiciona a resposta ao histórico
            historico_estado.append(resposta)
            
            # Mostra mensagem de sucesso
            gr.Info("Análise adicionada ao histórico!", duration=3)
            
            return historico_estado
        else:
            gr.Warning("Nenhuma resposta para adicionar ao histórico.")
            return historico_estado
    except Exception as e:
        gr.Error(f"Erro ao adicionar ao histórico: {str(e)}")
        return historico_estado

def gerar_pdf(historico_estado):
    try:
        if not historico_estado or len(historico_estado) == 0:
            gr.Warning("Nenhum dado para gerar o PDF. Adicione algumas análises primeiro.")
            return None
        
        timestamp = gerar_timestamp()
        caminho_pdf = f"relatorio_perguntas_respostas_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Cabeçalho
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Relatório de Análises - Nexus Education", ln=True, align='C')
        pdf.ln(10)
        
        # Data de geração
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, txt=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
        pdf.ln(5)
        
        # Conteúdo das análises
        for i, resposta in enumerate(historico_estado, 1):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, txt=f"Análise {i}:", ln=True)
            pdf.set_font("Arial", '', 11)
            
            # Quebra o texto em linhas para caber na página
            linhas = resposta.split('\n')
            for linha in linhas:
                if len(linha) > 80:  # Se a linha for muito longa
                    palavras = linha.split()
                    linha_atual = ""
                    for palavra in palavras:
                        if len(linha_atual + " " + palavra) <= 80:
                            linha_atual += " " + palavra if linha_atual else palavra
                        else:
                            pdf.multi_cell(0, 6, txt=linha_atual)
                            linha_atual = palavra
                    if linha_atual:
                        pdf.multi_cell(0, 6, txt=linha_atual)
                else:
                    pdf.multi_cell(0, 6, txt=linha)
            
            pdf.ln(5)
        
        # Salva o PDF
        pdf.output(caminho_pdf)
        
        # Verifica se o arquivo foi criado
        if os.path.exists(caminho_pdf):
            gr.Info(f"PDF gerado com sucesso: {caminho_pdf}")
            return caminho_pdf
        else:
            gr.Error("Erro ao gerar o PDF")
            return None
            
    except Exception as e:
        gr.Error(f"Erro ao gerar PDF: {str(e)}")
        return None

def resetar_aplicação():
    return None, "A aplicação foi resetada. Por favor, faça upload de um novo arquivo."
