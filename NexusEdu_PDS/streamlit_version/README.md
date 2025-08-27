# 🚀 Nexus Education PDS - Versão Streamlit

Esta pasta contém a versão **Streamlit** da aplicação Nexus Education PDS, convertida do Gradio original.

## 📁 **Estrutura da Pasta**

```
streamlit_version/
├── 📱 app_streamlit.py          # Aplicação principal
├── 🔐 auth_streamlit.py         # Autenticação
├── 📄 pdf_tools_streamlit.py    # Processamento PDF
├── 🚀 run_streamlit.py          # Execução Python
├── ⚡ run_streamlit.bat         # Execução Windows
├── 📋 requirements.txt          # Dependências
├── ⚙️ .streamlit/               # Configurações
│   ├── config.toml
│   └── secrets.toml
├── 🚀 Procfile                  # Deploy Heroku
├── 🌐 render.yaml               # Deploy Render
├── 📚 DEPLOY.md                 # Guia de deploy
├── 📖 README_Streamlit.md       # Documentação completa
└── ⚡ INSTALACAO_RAPIDA.md      # Instalação rápida
```

## 🎯 **Como Usar**

### **1. Instalação Rápida**
```bash
cd streamlit_version
pip install -r requirements.txt
```

### **2. Configuração**
```bash
# Configure sua API key do Groq
export chave="sua-api-key-aqui"
```

### **3. Execução**
```bash
# Opção 1: Script Python
python run_streamlit.py

# Opção 2: Script Windows
run_streamlit.bat

# Opção 3: Comando direto
streamlit run app_streamlit.py
```

## 🌐 **Deploy**

### **Streamlit Cloud (Recomendado)**
1. Faça push para GitHub
2. Acesse: https://share.streamlit.io/
3. Configure: `NexusEducation_Ferramenta/streamlit_version/app_streamlit.py`
4. Deploy!

### **Outras Plataformas**
- **Render**: Use `render.yaml`
- **Heroku**: Use `Procfile`
- **VPS**: Veja `DEPLOY.md`

## 📚 **Documentação**

- **`README_Streamlit.md`** - Documentação completa
- **`INSTALACAO_RAPIDA.md`** - Instalação em 3 passos
- **`DEPLOY.md`** - Guia de deploy completo

## 🔄 **Diferenças da Versão Original**

- ✅ **Interface**: Gradio → Streamlit
- ✅ **Navegação**: Sistema de páginas
- ✅ **Estado**: Session State
- ✅ **Layout**: Sidebar responsiva
- ✅ **Formulários**: Mais elegantes

---

**🎓 Transformando a educação com IA e Streamlit!**
