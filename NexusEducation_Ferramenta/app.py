import os
import gradio as gr
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from fpdf import FPDF
from datetime import datetime

#API_KEY
api_key = os.getenv("chave")

#Config Inicial do QP
Settings.llm = Groq(model='llama3-70b-8192', api_key=api_key)


def analisar_documentos(arquivos):
    converter = DocumentConverter()
    textos = ""
    # Converte cada PDF e agrega conteúdo
    for file in arquivos:
        res = converter.convert(file.name)
        doc = res.document
        texto = doc.export_to_markdown()
        textos += texto + "\n\n"
    # Chama o modelo de linguagem para gerar uma resposta
    prompt = f"Resuma o conteúdo dos seguintes documentos:\n{textos}, e faça uma análise semântica a análise semântica deve ser feita apenas do (conteúdo programático) se não tiver apenas faça o resumo dos documentos"
    
    if arquivos is None or len(arquivos) == 0:
        return "Nenhum arquivo enviado."


    # Chamada ao LLM usando o método `.complete()`
    resposta = Settings.llm.complete(prompt)

    return resposta.text  # `.text` contém a resposta

def add_historico(resposta, historico_estado):
    if  resposta:
        historico_estado.append((resposta))
        gr.Info("Adicionado ao PDF!", duration=2)
        return historico_estado


def gerar_pdf(historico_estado):
    if not historico_estado:
        return "Nenhum dado para adicionar ao PDF.", None

    # Gerar nome de arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
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


with gr.Blocks(theme='shivi/calm_seafoam') as app:

    gr.Markdown('# Bem Vindo ao Nexus Education🔎🎲')

    gr.Markdown('''
    Carregue um arquivo PDF e faça análise sobre os dados da ementa do aluno.Você poderá
    visualizar a resposta e, se desejar, adicionar essa interação ao PDF final, basta clicar
    em "Adicionar ao histórico do PDF".
    Após definir os arquivos e gerar respostas no histórico, clique em "Gerar PDF". Assim, será possível
    baixar um PDF com o registro completo das suas interações. Se você quiser analisar um novo dataset,
    basta clicar em "Quero analisar outro documento" ao final da página.
    ''')

    # Campo de entrada de arquivos
    input_arquivo = gr.File(file_count="multiple", type="filepath", label="Upload PDFs")

    #upload_status = gr.Textbox(label="Status do Upload:")

    # Botão de envio posicionado após a pergunta
    botao_submeter = gr.Button("Enviar")

    # Componente de resposta
    output_resposta = gr.Textbox(label="Resposta")

    with gr.Row():
        botao_add_pdf = gr.Button("Adicionar ao histórico do PDF")
        botao_gerar_pdf = gr.Button("Gerar PDF")

    arquivo_pdf = gr.File(label="Download do PDF Respostas ")
    
    botao_resetar = gr.Button("Quero analisar outro Documento!")

    historico_estado = gr.State(value=[])  # Estado para armazenar o histórico

    botao_submeter.click(fn=analisar_documentos,
                         inputs=[input_arquivo],
                         outputs=output_resposta)
    
    botao_add_pdf.click(fn=add_historico,
                        inputs=[output_resposta, historico_estado],
                        outputs=historico_estado)

    botao_gerar_pdf.click(fn=gerar_pdf,
                          inputs=[historico_estado],
                          outputs=arquivo_pdf)
    
    botao_resetar.click(fn=resetar_aplicação,
                        inputs=[],
                        outputs=[input_arquivo, output_resposta])

if __name__=="__main__":
    app.launch(share=True)