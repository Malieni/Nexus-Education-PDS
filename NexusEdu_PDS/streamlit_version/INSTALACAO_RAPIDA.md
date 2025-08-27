# 🚀 Instalação Rápida - Nexus Education PDS Streamlit

## ⚡ Instalação em 3 Passos

### 1️⃣ Instalar Dependências
```bash
cd streamlit_version
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key
```bash
# Windows (PowerShell)
$env:chave="sua-api-key-aqui"

# Windows (CMD)
set chave=sua-api-key-aqui

# Linux/Mac
export chave="sua-api-key-aqui"
```

### 3️⃣ Executar Aplicação
```bash
cd streamlit_version
python run_streamlit.py
```

## 🌐 Acesso
- **URL**: http://localhost:8501
- **Navegador**: Abre automaticamente

---

## 🔧 Solução de Problemas Rápidos

### ❌ "Streamlit não encontrado"
```bash
pip install streamlit
```

### ❌ "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### ❌ "API key não configurada"
Configure a variável de ambiente `chave`

### ❌ "Porta em uso"
```bash
# Mata processos na porta 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

## 📱 Primeiro Uso

1. **Acesse**: http://localhost:8501
2. **Cadastre-se**: Crie uma nova conta
3. **Faça login**: Acesse com suas credenciais
4. **Upload PDF**: Envie um arquivo PDF para análise
5. **Visualize**: Veja a análise gerada pela IA

---

## 🎯 Comandos Úteis

```bash
# Executar com configurações personalizadas
streamlit run app_streamlit.py --server.port 8502

# Executar em modo headless
streamlit run app_streamlit.py --server.headless true

# Ver logs detalhados
streamlit run app_streamlit.py --logger.level debug
```

---

**🎓 Nexus Education PDS - Transformando a educação com IA**
