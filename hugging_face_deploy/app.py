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

# Configuração para Hugging Face Spaces
# A API key deve ser configurada nas variáveis de ambiente do HF
api_key = os.getenv("GROQ_API_KEY", os.getenv("chave"))

# Config Inicial do QP
if api_key:
    Settings.llm = Groq(model='llama3-70b-8192', api_key=api_key)
else:
    print("⚠️ GROQ_API_KEY não encontrada. Configure a variável de ambiente.")

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
    
    # Atualiza o idioma no módulo i18n
    i18n.set_language(novo_idioma)
    
    # Retorna uma mensagem para o usuário recarregar a página
    if novo_idioma == 'pt':
        message = "Idioma alterado para Português! Por favor, recarregue a página (F5) para ver as mudanças."
    else:
        message = "Language changed to English! Please reload the page (F5) to see the changes."
    
    # Retorna todos os textos atualizados na ordem correta
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

# Funções de navegação simplificadas
def mostrar_pagina(pagina_destino):
    """Função centralizada para navegação entre páginas"""
    paginas = {
        "login": [True, False, False, False, False],      # login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box
        "cadastro": [False, True, False, False, False],
        "main": [False, False, True, False, False],
        "add_analise": [False, False, False, True, False],
        "formulario": [False, False, False, False, True]
    }
    
    if pagina_destino in paginas:
        return [gr.update(visible=visivel) for visivel in paginas[pagina_destino]]
    return [gr.update(visible=False)] * 5

def ir_para_inicio():
    """Navega para a página inicial (Add Análise)"""
    return mostrar_pagina("add_analise")

def ir_para_config():
    """Navega para a página de configurações"""
    return mostrar_pagina("add_analise")  # Configurações ficam na mesma página

def mostrar_formulario_analise():
    """Mostra o formulário de dados do aluno"""
    return mostrar_pagina("formulario")

def voltar_para_add_analise():
    """Volta para a página Add Análise"""
    return mostrar_pagina("add_analise")

def avancar_para_upload(nome, matricula, curso, codigo, carga):
    """Avança para a página de upload do PDF"""
    # Aqui pode salvar os dados em memória ou banco futuramente
    return mostrar_pagina("main")

def salvar_analise(email, descricao):
    """Salva uma nova análise"""
    if email not in analises_por_usuario:
        analises_por_usuario[email] = []
    analises_por_usuario[email].append(descricao)
    return analises_por_usuario[email]

# Interface principal otimizada para HF Spaces
with gr.Blocks(
    title="Nexus Education - Análise de Ementas",
    theme=gr.themes.Soft(),
    css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .main-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    """
) as app:
    
    # Estados para navegação
    pagina_atual = gr.State(value="add_analise")
    tema_atual = gr.State(value="shivi/calm_seafoam")
    idioma_atual = gr.State(value=load_language())
    usuario_email = gr.State(value=None)
    usuario_analises = gr.State(value=[])

    # Carrega o idioma inicial
    current_language = load_language()
    i18n.set_language(current_language)
    
    # Header principal
    with gr.Row():
        gr.HTML("""
            <div class="main-header">
                <h1>🎓 Nexus Education</h1>
                <p>Análise Inteligente de Ementas de Disciplinas</p>
            </div>
        """)
    
    with gr.Row():
        # Conteúdo principal (dinâmico)
        with gr.Column(scale=4):
            # ===== PÁGINA: LOGIN =====
            login_box = gr.Group(visible=True)
            with login_box:
                markdown_login = gr.Markdown(i18n.get_text("login_titulo"))
                login_email = gr.Textbox(label=i18n.get_text("login_email"))
                login_senha = gr.Textbox(label=i18n.get_text("login_senha"), type="password")
                login_btn = gr.Button(i18n.get_text("login_entrar"), variant="primary")
                login_msg = gr.Markdown(visible=False)
                go_cadastro = gr.Button(i18n.get_text("login_nao_tem_conta"), variant="secondary")
            
            # ===== PÁGINA: CADASTRO =====
            cadastro_box = gr.Group(visible=False)
            with cadastro_box:
                markdown_cadastro = gr.Markdown(i18n.get_text("cadastro_titulo"))
                cadastro_email = gr.Textbox(label=i18n.get_text("cadastro_email"))
                cadastro_senha = gr.Textbox(label=i18n.get_text("cadastro_senha"), type="password")
                cadastro_instituto = gr.Textbox(label=i18n.get_text("cadastro_instituto"))
                cadastro_campus = gr.Textbox(label=i18n.get_text("cadastro_campus"))
                cadastro_curso = gr.Textbox(label=i18n.get_text("cadastro_curso"))
                cadastro_btn = gr.Button(i18n.get_text("cadastro_btn"), variant="primary")
                cadastro_msg = gr.Markdown(visible=False)
                go_login = gr.Button(i18n.get_text("login_ja_tem_conta"), variant="secondary")
            
            # ===== PÁGINA: ADD ANÁLISE (INÍCIO) =====
            add_analise_box = gr.Group(visible=False)
            with add_analise_box:
                logo_img = gr.Image(value=None, label=i18n.get_text("logo"), height=100)
                markdown_bemvindo = gr.Markdown(i18n.get_text("bem_vindo"))
                lista_analises = gr.List(label=i18n.get_text("ementas_anal"), interactive=False)
                botao_add = gr.Button(i18n.get_text("nova_analise"), variant="primary", size="lg")
                reload_message = gr.Markdown("", visible=False)
                
                # Configurações (na mesma página)
                with gr.Accordion("⚙️ Configurações", open=False):
                    markdown_config = gr.Markdown(i18n.get_text("configuracoes"))
                    tema_select = gr.Dropdown(["shivi/calm_seafoam", "default", "soft"], value="shivi/calm_seafoam", label=i18n.get_text("tema"))
                    editar_local = gr.Textbox(label=i18n.get_text("local"), placeholder="Edite seu local de trabalho")
                    editar_curso = gr.Textbox(label=i18n.get_text("curso"), placeholder="Edite seu curso")
                    salvar_config = gr.Button(i18n.get_text("salvar"), variant="secondary")
                    config_msg = gr.Markdown(visible=False)
            
            # ===== PÁGINA: FORMULÁRIO =====
            formulario_analise_box = gr.Group(visible=False)
            with formulario_analise_box:
                with gr.Row():
                    nome_aluno = gr.Textbox(label=i18n.get_text("nome_aluno"), scale=2)
                    matricula_aluno = gr.Textbox(label=i18n.get_text("matricula"), scale=1)
                with gr.Row():
                    curso_destino = gr.Textbox(label=i18n.get_text("curso_destino"), scale=2)
                    codigo_curso = gr.Textbox(label=i18n.get_text("codigo_curso"), scale=1)
                carga_horaria = gr.Textbox(label=i18n.get_text("carga_horaria"))
                with gr.Row():
                    voltar_add_analise = gr.Button(i18n.get_text("voltar"), variant="secondary")
                    avancar_upload = gr.Button(i18n.get_text("avancar_upload"), variant="primary")
            
            # ===== PÁGINA: ANÁLISE PDF (MAIN) =====
            main_box = gr.Group(visible=False)
            with main_box:
                markdown_main = gr.Markdown(i18n.get_text("bem_vindo"))
                input_arquivo = gr.File(file_count="single", type="filepath", label="📄 Upload PDF")
                botao_submeter = gr.Button("🔍 Analisar PDF", variant="primary")
                output_resposta = gr.Textbox(label=i18n.get_text("pdf_resposta"), lines=8)
                with gr.Row():
                    botao_add_pdf = gr.Button(i18n.get_text("add_pdf"), variant="secondary")
                    botao_gerar_pdf = gr.Button(i18n.get_text("gerar_pdf"), variant="primary")
                arquivo_pdf = gr.File(label=i18n.get_text("download_pdf"))
                botao_resetar = gr.Button(i18n.get_text("resetar"), variant="secondary")
                historico_estado = gr.State(value=[])
                
                # Eventos da página de análise PDF
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
        
        # ===== BARRA LATERAL =====
        with gr.Column(scale=1, min_width=200):
            with gr.Group():
                markdown_menu = gr.Markdown(i18n.get_text("menu"))
                btn_inicio = gr.Button(i18n.get_text("inicio"), variant="secondary", size="sm")
                btn_config = gr.Button(i18n.get_text("config"), variant="secondary", size="sm")
                gr.Markdown("---")
                idioma_select = gr.Dropdown(["pt", "en"], value=current_language, label=i18n.get_text("idioma"))
            
            # Informações do sistema
            with gr.Group():
                gr.Markdown("### ℹ️ Informações")
                gr.Markdown(f"**Versão:** 1.0.0")
                gr.Markdown(f"**API:** {'✅ Configurada' if api_key else '❌ Não configurada'}")
                if not api_key:
                    gr.Markdown("⚠️ Configure GROQ_API_KEY nas variáveis de ambiente")

    # ===== FUNÇÕES DE NAVEGAÇÃO =====
    def trocar_tema(novo_tema):
        return novo_tema

    def salvar_configuracoes(tema, local, curso):
        return f"✅ Configurações salvas! Tema: {tema}, Local: {local}, Curso: {curso}", gr.update(visible=True)

    # ===== EVENTOS DE NAVEGAÇÃO =====
    # Menu lateral
    btn_inicio.click(fn=ir_para_inicio, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    btn_config.click(fn=ir_para_config, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Troca de idioma
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
    
    # Configurações
    salvar_config.click(fn=salvar_configuracoes, inputs=[editar_local, editar_curso], outputs=[config_msg, config_msg])

    # ===== NAVEGAÇÃO ENTRE TELAS =====
    # Login/Cadastro
    go_cadastro.click(fn=lambda: mostrar_pagina("cadastro"), inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    go_login.click(fn=lambda: mostrar_pagina("login"), inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Login/Cadastro submit
    login_btn.click(fn=login_submit,
                   inputs=[login_email, login_senha, login_box, cadastro_box, main_box, add_analise_box],
                   outputs=[login_box, cadastro_box, main_box, add_analise_box, login_msg, usuario_email, usuario_analises])
    cadastro_btn.click(fn=cadastro_submit,
                      inputs=[cadastro_email, cadastro_senha, cadastro_instituto, cadastro_campus, cadastro_curso, login_box, cadastro_box, main_box, add_analise_box],
                      outputs=[login_box, cadastro_box, main_box, add_analise_box, cadastro_msg, usuario_email, usuario_analises])

    # ===== NAVEGAÇÃO DO FLUXO PRINCIPAL =====
    # Botão '+' para iniciar nova análise
    botao_add.click(fn=mostrar_formulario_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Botão de avançar para upload do PDF
    avancar_upload.click(fn=avancar_para_upload, inputs=[nome_aluno, matricula_aluno, curso_destino, codigo_curso, carga_horaria], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    
    # Botão de voltar para Add Análise
    voltar_add_analise.click(fn=voltar_para_add_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])

# Configuração para Hugging Face Spaces
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Não compartilhar por padrão no HF
        show_error=True,
        quiet=False
    )
