import os
import streamlit as st
import json
from docling.document_converter import DocumentConverter
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from fpdf import FPDF
from datetime import datetime
from auth_streamlit import autenticar, cadastrar
from pdf_tools_streamlit import analisar_documentos, add_historico, gerar_pdf, resetar_aplicacao
from utils import gerar_timestamp
from i18n import i18n

# Configuração da página Streamlit
st.set_page_config(
    page_title="Nexus Education PDS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API_KEY
api_key = os.getenv("chave")

# Config Inicial do QP
Settings.llm = Groq(model='llama3-70b-8192', api_key=api_key)

# Simulação de "banco de dados" simples em memória
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {}

# Estado global para armazenar análises por usuário (em memória)
if 'analises_por_usuario' not in st.session_state:
    st.session_state.analises_por_usuario = {}

# Arquivo para salvar o idioma selecionado
LANGUAGE_FILE = "selected_language.json"

def save_language(language):
    """Salva o idioma selecionado em um arquivo"""
    try:
        with open(LANGUAGE_FILE, 'w') as f:
            json.dump({'language': language}, f)
    except Exception as e:
        st.error(f"Erro ao salvar idioma: {e}")

def load_language():
    """Carrega o idioma salvo ou retorna 'pt' como padrão"""
    try:
        if os.path.exists(LANGUAGE_FILE):
            with open(LANGUAGE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('language', 'pt')
    except Exception as e:
        st.error(f"Erro ao carregar idioma: {e}")
    return 'pt'

def main():
    # Carrega o idioma inicial
    current_language = load_language()
    i18n.set_language(current_language)
    
    # Sidebar para configurações e navegação
    with st.sidebar:
        st.title(i18n.get_text("menu"))
        
        # Seletor de idioma
        novo_idioma = st.selectbox(
            i18n.get_text("idioma"),
            ["pt", "en"],
            index=0 if current_language == "pt" else 1
        )
        
        if novo_idioma != current_language:
            save_language(novo_idioma)
            st.rerun()
        
        st.markdown("---")
        
        # Botões de navegação
        if st.button(i18n.get_text("inicio")):
            st.session_state.pagina_atual = "add_analise"
            st.rerun()
        
        if st.button(i18n.get_text("config")):
            st.session_state.pagina_atual = "config"
            st.rerun()
    
    # Inicializa a página atual se não existir
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = "login"
    
    # Inicializa o usuário logado se não existir
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    
    # Inicializa o histórico se não existir
    if 'historico_estado' not in st.session_state:
        st.session_state.historico_estado = []
    
    # Navegação entre páginas
    if st.session_state.pagina_atual == "login":
        mostrar_pagina_login()
    elif st.session_state.pagina_atual == "cadastro":
        mostrar_pagina_cadastro()
    elif st.session_state.pagina_atual == "add_analise":
        mostrar_pagina_add_analise()
    elif st.session_state.pagina_atual == "formulario":
        mostrar_pagina_formulario()
    elif st.session_state.pagina_atual == "main":
        mostrar_pagina_main()
    elif st.session_state.pagina_atual == "config":
        mostrar_pagina_config()

def mostrar_pagina_login():
    st.title(i18n.get_text("login_titulo"))
    
    with st.form("login_form"):
        email = st.text_input(i18n.get_text("login_email"))
        senha = st.text_input(i18n.get_text("login_senha"), type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button(i18n.get_text("login_entrar")):
                if autenticar(email, senha):
                    st.session_state.usuario_logado = email
                    st.session_state.pagina_atual = "add_analise"
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")
        
        with col2:
            if st.form_submit_button(i18n.get_text("login_nao_tem_conta")):
                st.session_state.pagina_atual = "cadastro"
                st.rerun()

def mostrar_pagina_cadastro():
    st.title(i18n.get_text("cadastro_titulo"))
    
    with st.form("cadastro_form"):
        email = st.text_input(i18n.get_text("cadastro_email"))
        senha = st.text_input(i18n.get_text("cadastro_senha"), type="password")
        instituto = st.text_input(i18n.get_text("cadastro_instituto"))
        campus = st.text_input(i18n.get_text("cadastro_campus"))
        curso = st.text_input(i18n.get_text("cadastro_curso"))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button(i18n.get_text("cadastro_btn")):
                if cadastrar(email, senha, instituto, campus, curso):
                    st.success("Cadastro realizado com sucesso! Faça login.")
                    st.session_state.pagina_atual = "login"
                    st.rerun()
                else:
                    st.error("E-mail já cadastrado.")
        
        with col2:
            if st.form_submit_button(i18n.get_text("login_ja_tem_conta")):
                st.session_state.pagina_atual = "login"
                st.rerun()

def mostrar_pagina_add_analise():
    st.title(i18n.get_text("bem_vindo"))
    
    # Logo (placeholder)
    st.image("https://via.placeholder.com/200x100?text=Logo", caption=i18n.get_text("logo"))
    
    # Lista de análises
    if st.session_state.usuario_logado and st.session_state.usuario_logado in st.session_state.analises_por_usuario:
        st.subheader(i18n.get_text("ementas_anal"))
        for analise in st.session_state.analises_por_usuario[st.session_state.usuario_logado]:
            st.write(f"- {analise}")
    
    # Botão para nova análise
    if st.button(i18n.get_text("nova_analise")):
        st.session_state.pagina_atual = "formulario"
        st.rerun()
    
    # Configurações
    st.markdown("---")
    st.subheader(i18n.get_text("configuracoes"))
    
    with st.form("config_form"):
        tema = st.selectbox(i18n.get_text("tema"), ["shivi/calm_seafoam", "default", "soft"])
        local = st.text_input(i18n.get_text("local"), placeholder="Edite seu local de trabalho")
        curso = st.text_input(i18n.get_text("curso"), placeholder="Edite seu curso")
        
        if st.form_submit_button(i18n.get_text("salvar")):
            st.success(f"Configurações salvas! Tema: {tema}, Local: {local}, Curso: {curso}")

def mostrar_pagina_formulario():
    st.title("Dados do Aluno")
    
    with st.form("formulario_form"):
        nome = st.text_input(i18n.get_text("nome_aluno"))
        matricula = st.text_input(i18n.get_text("matricula"))
        curso_destino = st.text_input(i18n.get_text("curso_destino"))
        codigo = st.text_input(i18n.get_text("codigo_curso"))
        carga = st.text_input(i18n.get_text("carga_horaria"))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button(i18n.get_text("avancar_upload")):
                # Salva os dados em memória
                st.session_state.dados_aluno = {
                    'nome': nome,
                    'matricula': matricula,
                    'curso_destino': curso_destino,
                    'codigo': codigo,
                    'carga': carga
                }
                st.session_state.pagina_atual = "main"
                st.rerun()
        
        with col2:
            if st.form_submit_button(i18n.get_text("voltar")):
                st.session_state.pagina_atual = "add_analise"
                st.rerun()

def mostrar_pagina_main():
    st.title(i18n.get_text("bem_vindo"))
    
    # Upload do PDF
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file is not None:
        # Botão para submeter
        if st.button("Enviar"):
            resposta = analisar_documentos(uploaded_file)
            st.session_state.resposta_atual = resposta
            st.rerun()
        
        # Mostra a resposta se existir
        if 'resposta_atual' in st.session_state and st.session_state.resposta_atual:
            st.subheader(i18n.get_text("pdf_resposta"))
            st.write(st.session_state.resposta_atual)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(i18n.get_text("add_pdf")):
                    add_historico(st.session_state.resposta_atual, st.session_state.historico_estado)
                    st.success("Adicionado ao PDF!")
                    st.rerun()
            
            with col2:
                if st.button(i18n.get_text("gerar_pdf")):
                    pdf_path = gerar_pdf(st.session_state.historico_estado)
                    if pdf_path:
                        with open(pdf_path, "rb") as file:
                            st.download_button(
                                label=i18n.get_text("download_pdf"),
                                data=file.read(),
                                file_name=pdf_path,
                                mime="application/pdf"
                            )
            
            with col3:
                if st.button(i18n.get_text("resetar")):
                    resetar_aplicacao()
                    st.session_state.resposta_atual = None
                    st.session_state.historico_estado = []
                    st.rerun()
    
    # Mostra o histórico
    if st.session_state.historico_estado:
        st.subheader("Histórico de Análises")
        for i, resposta in enumerate(st.session_state.historico_estado):
            st.write(f"**Análise {i+1}:**")
            st.write(resposta)
            st.markdown("---")

def mostrar_pagina_config():
    st.title(i18n.get_text("configuracoes"))
    
    with st.form("config_geral_form"):
        tema = st.selectbox(i18n.get_text("tema"), ["shivi/calm_seafoam", "default", "soft"])
        local = st.text_input(i18n.get_text("local"), placeholder="Edite seu local de trabalho")
        curso = st.text_input(i18n.get_text("curso"), placeholder="Edite seu curso")
        
        if st.form_submit_button(i18n.get_text("salvar")):
            st.success(f"Configurações salvas! Tema: {tema}, Local: {local}, Curso: {curso}")
    
    if st.button("Voltar ao Início"):
        st.session_state.pagina_atual = "add_analise"
        st.rerun()

if __name__ == "__main__":
    main()
