# Nexus Education PDS - Versão Streamlit

Esta é a versão da aplicação Nexus Education PDS convertida do Gradio para Streamlit.

## 🚀 Características

- **Interface moderna**: Interface web responsiva e intuitiva
- **Navegação por páginas**: Sistema de navegação entre diferentes seções
- **Autenticação**: Sistema de login e cadastro de usuários
- **Análise de PDFs**: Processamento de ementas usando IA
- **Geração de relatórios**: Criação de PDFs com análises
- **Suporte multilíngue**: Português e Inglês
- **Persistência de dados**: Configurações salvas localmente

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório** (se ainda não fez):
   ```bash
   git clone <url-do-repositorio>
   cd NexusEducation_Ferramenta
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a variável de ambiente**:
   ```bash
   # Windows (PowerShell)
   $env:chave="sua-api-key-aqui"
   
   # Windows (CMD)
   set chave=sua-api-key-aqui
   
   # Linux/Mac
   export chave="sua-api-key-aqui"
   ```

## 🎯 Como Executar

### Opção 1: Script Python (Recomendado)
```bash
cd streamlit_version
python run_streamlit.py
```

### Opção 2: Script Batch (Windows)
```bash
cd streamlit_version
run_streamlit.bat
```

### Opção 3: Comando direto
```bash
cd streamlit_version
streamlit run app_streamlit.py
```

## 🌐 Acesso

Após a execução, a aplicação estará disponível em:
- **URL local**: http://localhost:8501
- **URL da rede**: http://seu-ip:8501

## 📱 Funcionalidades

### 🔐 Autenticação
- **Login**: Acesso com email e senha
- **Cadastro**: Criação de nova conta
- **Sessão persistente**: Mantém o usuário logado

### 📊 Análise de Ementas
- **Upload de PDF**: Envio de arquivos PDF
- **Processamento com IA**: Análise automática do conteúdo
- **Histórico**: Armazenamento de análises anteriores
- **Geração de relatórios**: Criação de PDFs com resultados

### ⚙️ Configurações
- **Temas**: Seleção de aparência visual
- **Idioma**: Português ou Inglês
- **Perfil**: Configurações pessoais

## 🏗️ Estrutura do Projeto

```
NexusEducation_Ferramenta/
├── streamlit_version/        # Versão Streamlit da aplicação
│   ├── app_streamlit.py      # Aplicação principal Streamlit
│   ├── auth_streamlit.py     # Módulo de autenticação
│   ├── pdf_tools_streamlit.py # Ferramentas de processamento PDF
│   ├── run_streamlit.py      # Script de execução Python
│   ├── run_streamlit.bat     # Script de execução Windows
│   ├── requirements.txt      # Dependências Streamlit
│   ├── .streamlit/           # Configurações Streamlit
│   │   ├── config.toml
│   │   └── secrets.toml
│   ├── Procfile             # Para deploy no Heroku
│   ├── render.yaml          # Para deploy no Render
│   ├── DEPLOY.md            # Guia de deploy
│   ├── README_Streamlit.md  # Documentação
│   └── INSTALACAO_RAPIDA.md # Instalação rápida
├── app.py                   # Versão original Gradio
├── auth.py                  # Autenticação original
├── pdf_tools.py             # Ferramentas PDF originais
├── i18n.py                  # Internacionalização
├── utils.py                 # Utilitários
└── README.md                # Documentação original
```

## 🔄 Migração do Gradio

### Principais mudanças:
- **Interface**: Gradio → Streamlit
- **Navegação**: Sistema de páginas com `st.session_state`
- **Estado**: Gerenciamento de estado via `st.session_state`
- **Layout**: Sidebar para navegação e configurações
- **Formulários**: Uso de `st.form` para melhor UX

### Funcionalidades mantidas:
- ✅ Sistema de autenticação
- ✅ Processamento de PDFs
- ✅ Análise com IA
- ✅ Geração de relatórios
- ✅ Suporte multilíngue
- ✅ Configurações de usuário

## 🐛 Solução de Problemas

### Erro: "Streamlit não encontrado"
```bash
pip install streamlit
```

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "API key não configurada"
Configure a variável de ambiente `chave` com sua API key do Groq.

### Aplicação não abre no navegador
Verifique se a porta 8501 não está sendo usada por outro processo.

## 📚 Recursos Adicionais

- **Documentação Streamlit**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/
- **Exemplos Streamlit**: https://github.com/streamlit/streamlit-example

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a mesma licença do projeto original.

---

**Desenvolvido com ❤️ para a comunidade educacional**
