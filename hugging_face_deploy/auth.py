# auth.py
import gradio as gr

# Simulação de "banco de dados" simples em memória
usuarios = {}

def autenticar(email, senha):
    user = usuarios.get(email)
    if user and user['senha'] == senha:
        return True, f"Bem-vindo, {email}!"
    return False, "E-mail ou senha incorretos."

def cadastrar(email, senha, instituto, campus, curso):
    if email in usuarios:
        return False, "E-mail já cadastrado."
    usuarios[email] = {
        'senha': senha,
        'instituto': instituto,
        'campus': campus,
        'curso': curso
    }
    return True, "Cadastro realizado com sucesso! Faça login."

def mostrar_login():
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

def mostrar_cadastro():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def login_submit(email, senha, login_box, cadastro_box, main_box):
    sucesso, msg = autenticar(email, senha)
    if sucesso:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), msg
    else:
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), msg

def cadastro_submit(email, senha, instituto, campus, curso, login_box, cadastro_box, main_box):
    sucesso, msg = cadastrar(email, senha, instituto, campus, curso)
    if sucesso:
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), msg
    else:
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), msg
