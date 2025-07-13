import os
import gradio as gr
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from fpdf import FPDF
from datetime import datetime
from NexusEducation_Ferramenta.auth import autenticar, cadastrar, mostrar_login, mostrar_cadastro, login_submit, cadastro_submit
from NexusEducation_Ferramenta.pdf_tools import analisar_documentos, add_historico, gerar_pdf, resetar_aplicação
from NexusEducation_Ferramenta.utils import gerar_timestamp

#API_KEY
api_key = os.getenv("chave")

#Config Inicial do QP
Settings.llm = Groq(model='llama3-70b-8192', api_key=api_key)

# Simulação de "banco de dados" simples em memória
usuarios = {}

# Estado global para armazenar análises por usuário (em memória)
analises_por_usuario = {}

# Dicionário de textos para internacionalização
textos = {
    'pt': {
        'bem_vindo': '## Bem-vindo ao Nexus Education!\nAqui você pode analisar ementas de disciplinas e gerar relatórios inteligentes.\nClique no botão "+" para iniciar uma nova análise.',
        'ementas_anal': 'Ementas analisadas',
        'nova_analise': '+ Nova Análise',
        'menu': '## Menu',
        'inicio': 'Início',
        'config': 'Configurações',
        'tema': 'Tema da Página',
        'local': 'Instituto/Câmpus',
        'curso': 'Curso',
        'salvar': 'Salvar Configurações',
        'configuracoes': '# Configurações',
        'idioma': 'Idioma',
        'logo': 'Logo do Projeto',
        'login_titulo': '# Login do Professor',
        'login_email': 'E-mail',
        'login_senha': 'Senha',
        'login_entrar': 'Entrar',
        'login_nao_tem_conta': 'Não tem conta? Cadastre-se',
        'login_ja_tem_conta': 'Já tem conta? Faça login',
        'cadastro_titulo': '# Cadastro do Professor',
        'cadastro_email': 'E-mail',
        'cadastro_senha': 'Senha',
        'cadastro_instituto': 'Instituto',
        'cadastro_campus': 'Câmpus',
        'cadastro_curso': 'Curso',
        'cadastro_btn': 'Cadastrar',
        'pdf_resposta': 'Resposta',
        'add_pdf': 'Adicionar ao histórico do PDF',
        'gerar_pdf': 'Gerar PDF',
        'download_pdf': 'Download do PDF Respostas',
        'resetar': 'Quero analisar outro Documento!',
    },
    'en': {
        'bem_vindo': '## Welcome to Nexus Education!\nHere you can analyze course syllabi and generate smart reports.\nClick the "+" button to start a new analysis.',
        'ementas_anal': 'Analyzed Syllabi',
        'nova_analise': '+ New Analysis',
        'menu': '## Menu',
        'inicio': 'Home',
        'config': 'Settings',
        'tema': 'Theme',
        'local': 'Institute/Campus',
        'curso': 'Course',
        'salvar': 'Save Settings',
        'configuracoes': '# Settings',
        'idioma': 'Language',
        'logo': 'Project Logo',
        'login_titulo': '# Teacher Login',
        'login_email': 'E-mail',
        'login_senha': 'Password',
        'login_entrar': 'Sign In',
        'login_nao_tem_conta': 'Don\'t have an account? Register',
        'login_ja_tem_conta': 'Already have an account? Login',
        'cadastro_titulo': '# Teacher Registration',
        'cadastro_email': 'E-mail',
        'cadastro_senha': 'Password',
        'cadastro_instituto': 'Institute',
        'cadastro_campus': 'Campus',
        'cadastro_curso': 'Course',
        'cadastro_btn': 'Register',
        'pdf_resposta': 'Answer',
        'add_pdf': 'Add to PDF history',
        'gerar_pdf': 'Generate PDF',
        'download_pdf': 'Download PDF Answers',
        'resetar': 'I want to analyze another document!',
    }
}

# Função para atualizar textos conforme idioma
def atualizar_textos(idioma):
    t = textos[idioma]
    return (
        # Add Análise
        t['logo'], t['bem_vindo'], t['ementas_anal'], t['nova_analise'],
        # Configurações
        t['configuracoes'], t['tema'], t['local'], t['curso'], t['salvar'],
        # Menu
        t['menu'], t['inicio'], t['config'], t['idioma'],
        # Login
        t['login_titulo'], t['login_email'], t['login_senha'], t['login_entrar'], t['login_nao_tem_conta'],
        # Cadastro
        t['cadastro_titulo'], t['cadastro_email'], t['cadastro_senha'], t['cadastro_instituto'], t['cadastro_campus'], t['cadastro_curso'], t['cadastro_btn'], t['login_ja_tem_conta'],
        # PDF/Análise
        t['pdf_resposta'], t['add_pdf'], t['gerar_pdf'], t['download_pdf'], t['resetar']
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

# Novo grupo para formulário de dados do aluno e curso de destino
formulario_analise_box = gr.Group(visible=False, elem_id="formulario_analise_box")
with formulario_analise_box:
    with gr.Column():
        nome_aluno = gr.Textbox(label="Nome do Aluno")
        matricula_aluno = gr.Textbox(label="Matrícula")
        curso_destino = gr.Textbox(label="Curso de Destino")
        codigo_curso = gr.Textbox(label="Código do Curso de Destino")
        carga_horaria = gr.Textbox(label="Carga Horária do Curso de Destino")
        avancar_upload = gr.Button("Avançar para Upload do PDF")
        voltar_add_analise = gr.Button("Voltar")

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
    idioma_atual = gr.State(value="pt")

    with gr.Row():
        # Conteúdo principal (dinâmico)
        with gr.Column(scale=4):
            # Add Análise (Início)
            add_analise_box = gr.Group(visible=True, elem_id="add_analise_box")
            with add_analise_box:
                with gr.Column():
                    logo_img = gr.Image(value=None, label=textos['pt']['logo'], height=100)
                    markdown_bemvindo = gr.Markdown(textos['pt']['bem_vindo'])
                    lista_analises = gr.List(label=textos['pt']['ementas_anal'], interactive=False)
                    botao_add = gr.Button(textos['pt']['nova_analise'])
            # Configurações
            configuracoes_box = gr.Group(visible=False, elem_id="configuracoes_box")
            with configuracoes_box:
                markdown_config = gr.Markdown(textos['pt']['configuracoes'])
                tema_select = gr.Dropdown(["shivi/calm_seafoam", "default", "soft"], value="shivi/calm_seafoam", label=textos['pt']['tema'])
                editar_local = gr.Textbox(label=textos['pt']['local'], placeholder="Edite seu local de trabalho")
                editar_curso = gr.Textbox(label=textos['pt']['curso'], placeholder="Edite seu curso")
                salvar_config = gr.Button(textos['pt']['salvar'])
                config_msg = gr.Markdown(visible=False)
            # Login
            login_box = gr.Group(visible=True)
            with login_box:
                markdown_login = gr.Markdown(textos['pt']['login_titulo'])
                login_email = gr.Textbox(label=textos['pt']['login_email'])
                login_senha = gr.Textbox(label=textos['pt']['login_senha'], type="password")
                login_btn = gr.Button(textos['pt']['login_entrar'])
                login_msg = gr.Markdown(visible=False)
                go_cadastro = gr.Button(textos['pt']['login_nao_tem_conta'])
            # Cadastro
            cadastro_box = gr.Group(visible=False)
            with cadastro_box:
                markdown_cadastro = gr.Markdown(textos['pt']['cadastro_titulo'])
                cadastro_email = gr.Textbox(label=textos['pt']['cadastro_email'])
                cadastro_senha = gr.Textbox(label=textos['pt']['cadastro_senha'], type="password")
                cadastro_instituto = gr.Textbox(label=textos['pt']['cadastro_instituto'])
                cadastro_campus = gr.Textbox(label=textos['pt']['cadastro_campus'])
                cadastro_curso = gr.Textbox(label=textos['pt']['cadastro_curso'])
                cadastro_btn = gr.Button(textos['pt']['cadastro_btn'])
                cadastro_msg = gr.Markdown(visible=False)
                go_login = gr.Button(textos['pt']['login_ja_tem_conta'])
            # Tela principal de análise PDF
            main_box = gr.Group(visible=False)
            with main_box:
                markdown_main = gr.Markdown(textos['pt']['bem_vindo'])
                input_arquivo = gr.File(file_count="single", type="filepath", label="Upload PDF")
                botao_submeter = gr.Button("Enviar")
                output_resposta = gr.Textbox(label=textos['pt']['pdf_resposta'])
                with gr.Row():
                    botao_add_pdf = gr.Button(textos['pt']['add_pdf'])
                    botao_gerar_pdf = gr.Button(textos['pt']['gerar_pdf'])
                arquivo_pdf = gr.File(label=textos['pt']['download_pdf'])
                botao_resetar = gr.Button(textos['pt']['resetar'])
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
            markdown_menu = gr.Markdown(textos['pt']['menu'])
            btn_inicio = gr.Button(textos['pt']['inicio'])
            btn_config = gr.Button(textos['pt']['config'])
            gr.Markdown("---")
            idioma_select = gr.Dropdown(["pt", "en"], value="pt", label=textos['pt']['idioma'])

    # Funções de navegação
    def ir_para_inicio():
        return gr.update(visible=True), gr.update(visible=False), "inicio"
    def ir_para_config():
        return gr.update(visible=False), gr.update(visible=True), "configuracoes"
    def trocar_tema(novo_tema):
        return novo_tema
    def trocar_idioma(novo_idioma):
        return novo_idioma
    def salvar_configuracoes(tema, local, curso):
        # Aqui pode salvar no banco futuramente
        return f"Configurações salvas! Tema: {tema}, Local: {local}, Curso: {curso}", gr.update(visible=True)

    # Botões do menu lateral
    btn_inicio.click(fn=ir_para_inicio, inputs=[], outputs=[add_analise_box, configuracoes_box, pagina_atual])
    btn_config.click(fn=ir_para_config, inputs=[], outputs=[add_analise_box, configuracoes_box, pagina_atual])
    tema_select.change(fn=trocar_tema, inputs=[tema_select], outputs=[tema_atual])
    idioma_select.change(
        fn=trocar_idioma,
        inputs=[idioma_select],
        outputs=[logo_img, markdown_bemvindo, lista_analises, botao_add, markdown_config, tema_select, editar_local, editar_curso, salvar_config, markdown_menu, btn_inicio, btn_config, idioma_select, markdown_login, login_email, login_senha, login_btn, go_cadastro, markdown_cadastro, cadastro_email, cadastro_senha, cadastro_instituto, cadastro_campus, cadastro_curso, cadastro_btn, go_login, output_resposta, botao_add_pdf, botao_gerar_pdf, arquivo_pdf, botao_resetar, idioma_atual]
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

    # Ajustar botao_add para mostrar o formulário
    botao_add.click(fn=mostrar_formulario_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    # Botão de avançar para upload do PDF
    avancar_upload.click(fn=avancar_para_upload, inputs=[nome_aluno, matricula_aluno, curso_destino, codigo_curso, carga_horaria], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])
    # Botão de voltar para Add Análise
    voltar_add_analise.click(fn=voltar_para_add_analise, inputs=[], outputs=[login_box, cadastro_box, main_box, add_analise_box, formulario_analise_box])

    # Quando uma nova análise for concluída, salvar na lista do usuário (mock)
    # Exemplo: salvar_analise(usuario_email, "Ementa de Matemática - 2024")

if __name__=="__main__":
    app.launch(share=True)