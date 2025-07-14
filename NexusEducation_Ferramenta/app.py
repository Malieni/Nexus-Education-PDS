import os
import gradio as gr
import json
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from fpdf import FPDF
from datetime import datetime
from auth import autenticar, cadastrar, mostrar_login, mostrar_cadastro, login_submit, cadastro_submit
from pdf_tools import analisar_documentos, add_historico, gerar_pdf, resetar_aplicação
from utils import gerar_timestamp
from i18n import i18n

#API_KEY
api_key = os.getenv("chave")

#Config Inicial do QP
Settings.llm = Groq(model='llama3-70b-8192', api_key=api_key)

# Simulação de "banco de dados" simples em memória
usuarios = {}

# Estado global para armazenar análises por usuário (em memória)
analises_por_usuario = {}

# Arquivo para salvar o idioma selecionado
LANGUAGE_FILE = "selected_language.json"

def save_language(language):
    """Salva o idioma selecionado em um arquivo"""
    try:
        with open(LANGUAGE_FILE, 'w') as f:
            json.dump({'language': language}, f)
    except Exception as e:
        print(f"Erro ao salvar idioma: {e}")

def load_language():
    """Carrega o idioma salvo ou retorna 'pt' como padrão"""
    try:
        if os.path.exists(LANGUAGE_FILE):
            with open(LANGUAGE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('language', 'pt')
    except Exception as e:
        print(f"Erro ao carregar idioma: {e}")
    return 'pt'

# Função para trocar idioma usando o módulo i18n
def trocar_idioma(novo_idioma):
    # Salva o idioma selecionado
    save_language(novo_idioma)
    
    # Retorna uma mensagem para o usuário recarregar a página
    if novo_idioma == 'pt':
        message = "Idioma alterado para Português! Por favor, recarregue a página (F5) para ver as mudanças."
    else:
        message = "Language changed to English! Please reload the page (F5) to see the changes."
    
    return (
        # Add Análise
        i18n.get_text("logo", novo_idioma), i18n.get_text("bem_vindo", novo_idioma), 
        i18n.get_text("ementas_anal", novo_idioma), i18n.get_text("nova_analise", novo_idioma),
        # Configurações
        i18n.get_text("configuracoes", novo_idioma), i18n.get_text("tema", novo_idioma), 
        i18n.get_text("local", novo_idioma), i18n.get_text("curso", novo_idioma), 
        i18n.get_text("salvar", novo_idioma),
        # Menu
        i18n.get_text("menu", novo_idioma), i18n.get_text("inicio", novo_idioma), 
        i18n.get_text("config", novo_idioma), i18n.get_text("idioma", novo_idioma),
        # Login
        i18n.get_text("login_titulo", novo_idioma), i18n.get_text("login_email", novo_idioma), 
        i18n.get_text("login_senha", novo_idioma), i18n.get_text("login_entrar", novo_idioma), 
        i18n.get_text("login_nao_tem_conta", novo_idioma),
        # Cadastro
        i18n.get_text("cadastro_titulo", novo_idioma), i18n.get_text("cadastro_email", novo_idioma), 
        i18n.get_text("cadastro_senha", novo_idioma), i18n.get_text("cadastro_instituto", novo_idioma), 
        i18n.get_text("cadastro_campus", novo_idioma), i18n.get_text("cadastro_curso", novo_idioma), 
        i18n.get_text("cadastro_btn", novo_idioma), i18n.get_text("login_ja_tem_conta", novo_idioma),
        # PDF/Análise
        i18n.get_text("pdf_resposta", novo_idioma), i18n.get_text("add_pdf", novo_idioma), 
        i18n.get_text("gerar_pdf", novo_idioma), i18n.get_text("download_pdf", novo_idioma), 
        i18n.get_text("resetar", novo_idioma),
        # Formulário
        i18n.get_text("nome_aluno", novo_idioma), i18n.get_text("matricula", novo_idioma), 
        i18n.get_text("curso_destino", novo_idioma), i18n.get_text("codigo_curso", novo_idioma), 
        i18n.get_text("carga_horaria", novo_idioma), i18n.get_text("avancar_upload", novo_idioma), 
        i18n.get_text("voltar", novo_idioma),
        # Mensagem de recarregar
        message,
        # Estado do idioma
        novo_idioma
    )

# Função para exibir a tela de Add Análise
def mostrar_add_analise(email):
    # Recupera as análises do usuário
    analises = analises_por_usuario.get(email, [])
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), analises

# Função chamada ao clicar no botão '+'
def iniciar_nova_analise(email, analises):
    # Aqui pode-se redirecionar para a tela de upload/análise
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

# Função para salvar uma nova análise (mock)
def salvar_analise(email, descricao):
    if email not in analises_por_usuario:
        analises_por_usuario[email] = []
    analises_por_usuario[email].append(descricao)
    return analises_por_usuario[email]

# Função para mostrar formulário ao clicar em '+ Nova Análise'
def mostrar_formulario_analise(*_):
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

# Função para voltar para Add Análise
def voltar_para_add_analise(*_):
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

# Função para avançar para upload do PDF (pode ser expandida para salvar os dados)
def avancar_para_upload(nome, matricula, curso, codigo, carga):
    # Aqui pode salvar os dados em memória ou banco futuramente
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

with gr.Blocks(theme='shivi/calm_seafoam') as app:
    # Estados para navegação
    pagina_atual = gr.State(value="inicio")  # "inicio" ou "configuracoes"
    tema_atual = gr.State(value="shivi/calm_seafoam")
    idioma_atual = gr.State(value=load_language()) # Carrega o idioma salvo ou 'pt' como padrão
    usuario_email = gr.State(value=None)
    usuario_analises = gr.State(value=[])

    # Carrega o idioma inicial
    current_language = load_language()
    i18n.set_language(current_language)
    
    with gr.Row():
        # Conteúdo principal (dinâmico)
        with gr.Column(scale=4):
            # Add Análise (Início)
            add_analise_box = gr.Group(visible=True, elem_id="add_analise_box")
            with add_analise_box:
                logo_img = gr.Image(value=None, label=i18n.get_text("logo"), height=100)
                markdown_bemvindo = gr.Markdown(i18n.get_text("bem_vindo"))
                lista_analises = gr.List(label=i18n.get_text("ementas_anal"), interactive=False)
                botao_add = gr.Button(i18n.get_text("nova_analise"))
                # Mensagem de recarregar (inicialmente vazia)
                reload_message = gr.Markdown("", visible=False)
            
            # Formulário de dados do aluno e curso de destino
            formulario_analise_box = gr.Group(visible=False, elem_id="formulario_analise_box")
            with formulario_analise_box:
                nome_aluno = gr.Textbox(label=i18n.get_text("nome_aluno"))
                matricula_aluno = gr.Textbox(label=i18n.get_text("matricula"))
                curso_destino = gr.Textbox(label=i18n.get_text("curso_destino"))
                codigo_curso = gr.Textbox(label=i18n.get_text("codigo_curso"))
                carga_horaria = gr.Textbox(label=i18n.get_text("carga_horaria"))
                avancar_upload = gr.Button(i18n.get_text("avancar_upload"))
                voltar_add_analise = gr.Button(i18n.get_text("voltar"))
            
            # Configurações
            configuracoes_box = gr.Group(visible=False, elem_id="configuracoes_box")
            with configuracoes_box:
                markdown_config = gr.Markdown(i18n.get_text("configuracoes"))
                tema_select = gr.Dropdown(["shivi/calm_seafoam", "default", "soft"], value="shivi/calm_seafoam", label=i18n.get_text("tema"))
                editar_local = gr.Textbox(label=i18n.get_text("local"), placeholder="Edite seu local de trabalho")
                editar_curso = gr.Textbox(label=i18n.get_text("curso"), placeholder="Edite seu curso")
                salvar_config = gr.Button(i18n.get_text("salvar"))
                config_msg = gr.Markdown(visible=False)
            
            # Login
            login_box = gr.Group(visible=True)
            with login_box:
                markdown_login = gr.Markdown(i18n.get_text("login_titulo"))
                login_email = gr.Textbox(label=i18n.get_text("login_email"))
                login_senha = gr.Textbox(label=i18n.get_text("login_senha"), type="password")
                login_btn = gr.Button(i18n.get_text("login_entrar"))
                login_msg = gr.Markdown(visible=False)
                go_cadastro = gr.Button(i18n.get_text("login_nao_tem_conta"))
            
            # Cadastro
            cadastro_box = gr.Group(visible=False)
            with cadastro_box:
                markdown_cadastro = gr.Markdown(i18n.get_text("cadastro_titulo"))
                cadastro_email = gr.Textbox(label=i18n.get_text("cadastro_email"))
                cadastro_senha = gr.Textbox(label=i18n.get_text("cadastro_senha"), type="password")
                cadastro_instituto = gr.Textbox(label=i18n.get_text("cadastro_instituto"))
                cadastro_campus = gr.Textbox(label=i18n.get_text("cadastro_campus"))
                cadastro_curso = gr.Textbox(label=i18n.get_text("cadastro_curso"))
                cadastro_btn = gr.Button(i18n.get_text("cadastro_btn"))
                cadastro_msg = gr.Markdown(visible=False)
                go_login = gr.Button(i18n.get_text("login_ja_tem_conta"))
            
            # Tela principal de análise PDF
            main_box = gr.Group(visible=False)
            with main_box:
                markdown_main = gr.Markdown(i18n.get_text("bem_vindo"))
                input_arquivo = gr.File(file_count="single", type="filepath", label="Upload PDF")
                botao_submeter = gr.Button("Enviar")
                output_resposta = gr.Textbox(label=i18n.get_text("pdf_resposta"))
                botao_add_pdf = gr.Button(i18n.get_text("add_pdf"))
                botao_gerar_pdf = gr.Button(i18n.get_text("gerar_pdf"))
                arquivo_pdf = gr.File(label=i18n.get_text("download_pdf"))
                botao_resetar = gr.Button(i18n.get_text("resetar"))
                historico_estado = gr.State(value=[])
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
        
        # Barra lateral à direita
        with gr.Column(scale=1, min_width=180):
            markdown_menu = gr.Markdown(i18n.get_text("menu"))
            btn_inicio = gr.Button(i18n.get_text("inicio"))
            btn_config = gr.Button(i18n.get_text("config"))
            gr.Markdown("---")
            idioma_select = gr.Dropdown(["pt", "en"], value=current_language, label=i18n.get_text("idioma"))

    # Funções de navegação
    def ir_para_inicio():
        return gr.update(visible=True), gr.update(visible=False), "inicio"
    def ir_para_config():
        return gr.update(visible=False), gr.update(visible=True), "configuracoes"
    def trocar_tema(novo_tema):
        return novo_tema

    def salvar_configuracoes(tema, local, curso):
        # Aqui pode salvar no banco futuramente
        return f"Configurações salvas! Tema: {tema}, Local: {local}, Curso: {curso}", gr.update(visible=True)

    # Botões do menu lateral
    btn_inicio.click(fn=ir_para_inicio, inputs=[], outputs=[add_analise_box, configuracoes_box, pagina_atual])
    btn_config.click(fn=ir_para_config, inputs=[], outputs=[add_analise_box, configuracoes_box, pagina_atual])
    tema_select.change(fn=trocar_tema, inputs=[tema_select], outputs=[tema_atual])
    
    # Evento de troca de idioma simplificado
    idioma_select.change(
        fn=trocar_idioma,
        inputs=[idioma_select],
        outputs=[
            logo_img, markdown_bemvindo, lista_analises, botao_add,
            markdown_config, tema_select, editar_local, editar_curso, salvar_config,
            markdown_menu, btn_inicio, btn_config, idioma_select,
            markdown_login, login_email, login_senha, login_btn, go_cadastro,
            markdown_cadastro, cadastro_email, cadastro_senha, cadastro_instituto, 
            cadastro_campus, cadastro_curso, cadastro_btn, go_login,
            output_resposta, botao_add_pdf, botao_gerar_pdf, arquivo_pdf, botao_resetar,
            nome_aluno, matricula_aluno, curso_destino, codigo_curso, carga_horaria, 
            avancar_upload, voltar_add_analise, reload_message, idioma_atual
        ]
    )
    
    salvar_config.click(fn=salvar_configuracoes, inputs=[tema_select, editar_local, editar_curso], outputs=[config_msg, config_msg])

    # Navegação entre telas
    go_cadastro.click(fn=mostrar_cadastro, inputs=[], outputs=[login_box, cadastro_box, main_box])
    go_login.click(fn=mostrar_login, inputs=[], outputs=[login_box, cadastro_box, main_box])
    login_btn.click(fn=login_submit,
                   inputs=[login_email, login_senha, login_box, cadastro_box, main_box, add_analise_box],
                   outputs=[login_box, cadastro_box, main_box, add_analise_box, login_msg, usuario_email, usuario_analises])
    cadastro_btn.click(fn=cadastro_submit,
                      inputs=[cadastro_email, cadastro_senha, cadastro_instituto, cadastro_campus, cadastro_curso, login_box, cadastro_box, main_box, add_analise_box],
                      outputs=[login_box, cadastro_box, main_box, add_analise_box, cadastro_msg, usuario_email, usuario_analises])

    # Botão '+' para iniciar nova análise
    botao_add.click(fn=mostrar_formulario_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Botão de avançar para upload do PDF
    avancar_upload.click(fn=avancar_para_upload, inputs=[nome_aluno, matricula_aluno, curso_destino, codigo_curso, carga_horaria], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Botão de voltar para Add Análise
    voltar_add_analise.click(fn=voltar_para_add_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])

    # Quando uma nova análise for concluída, salvar na lista do usuário (mock)
    # Exemplo: salvar_analise(usuario_email, "Ementa de Matemática - 2024")

if __name__=="__main__":
    app.launch(share=True)
