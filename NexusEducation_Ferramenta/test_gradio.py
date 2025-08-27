#!/usr/bin/env python3
"""
Arquivo de teste para verificar se o Gradio está funcionando corretamente
"""

import gradio as gr
from i18n import i18n

def test_internacionalizacao():
    """Testa se a internacionalização está funcionando"""
    print("Testando internacionalização...")
    
    # Testa português
    i18n.set_language('pt')
    texto_pt = i18n.get_text('bem_vindo')
    print(f"Português: {texto_pt[:50]}...")
    
    # Testa inglês
    i18n.set_language('en')
    texto_en = i18n.get_text('bem_vindo')
    print(f"English: {texto_en[:50]}...")
    
    return "Teste de internacionalização concluído!"

def test_interface_simples():
    """Interface simples para testar o Gradio"""
    with gr.Blocks(title="Teste Nexus Education") as demo:
        gr.Markdown("# Teste da Interface")
        
        # Teste de idioma
        idioma = gr.Dropdown(["pt", "en"], value="pt", label="Idioma")
        texto_teste = gr.Textbox(label="Texto de teste", value=i18n.get_text('bem_vindo'))
        
        def trocar_idioma_teste(novo_idioma):
            i18n.set_language(novo_idioma)
            return i18n.get_text('bem_vindo')
        
        idioma.change(fn=trocar_idioma_teste, inputs=[idioma], outputs=[texto_teste])
        
        # Botão de teste
        btn_teste = gr.Button("Testar")
        resultado = gr.Textbox(label="Resultado")
        
        btn_teste.click(fn=test_internacionalizacao, outputs=[resultado])
    
    return demo

if __name__ == "__main__":
    print("Iniciando teste do Gradio...")
    
    # Testa a internacionalização primeiro
    try:
        resultado = test_internacionalizacao()
        print(f"✅ {resultado}")
    except Exception as e:
        print(f"❌ Erro na internacionalização: {e}")
    
    # Inicia a interface de teste
    try:
        demo = test_interface_simples()
        demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        print("Verifique se o Gradio está instalado corretamente")
