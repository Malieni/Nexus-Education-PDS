import streamlit as st

# Simulação de "banco de dados" simples em memória
def get_usuarios():
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = {}
    return st.session_state.usuarios

def autenticar(email, senha):
    """Autentica um usuário"""
    usuarios = get_usuarios()
    user = usuarios.get(email)
    if user and user['senha'] == senha:
        return True
    return False

def cadastrar(email, senha, instituto, campus, curso):
    """Cadastra um novo usuário"""
    usuarios = get_usuarios()
    if email in usuarios:
        return False
    
    usuarios[email] = {
        'senha': senha,
        'instituto': instituto,
        'campus': campus,
        'curso': curso
    }
    st.session_state.usuarios = usuarios
    return True

def get_usuario_info(email):
    """Retorna informações de um usuário"""
    usuarios = get_usuarios()
    return usuarios.get(email, {})
