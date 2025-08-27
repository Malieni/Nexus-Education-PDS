# 🎓 Nexus Education - Análise de Ementas

## Descrição

O **Nexus Education** é uma ferramenta inteligente para análise de ementas de disciplinas acadêmicas. Utiliza IA avançada para extrair, analisar e gerar relatórios detalhados sobre o conteúdo programático das disciplinas.

## ✨ Funcionalidades

- 🔍 **Análise Inteligente de PDFs** - Extração e análise semântica de ementas
- 🌍 **Internacionalização** - Suporte completo para português e inglês
- 📊 **Geração de Relatórios** - Criação automática de PDFs com análises
- 👤 **Sistema de Usuários** - Login, cadastro e histórico de análises
- 🎨 **Interface Moderna** - Design responsivo e intuitivo
- ⚙️ **Configurações Personalizáveis** - Temas e preferências do usuário

## 🚀 Deploy no Hugging Face

### Opção 1: Hugging Face Spaces (Recomendado)

1. **Crie um novo Space:**
   - Acesse [huggingface.co/spaces](https://huggingface.co/spaces)
   - Clique em "Create new Space"
   - Escolha "Gradio" como SDK
   - Nome: `nexus-education`
   - License: MIT

2. **Configure as variáveis de ambiente:**
   - Vá em **Settings** → **Repository secrets**
   - Adicione: `GROQ_API_KEY` = sua_chave_api_groq

3. **Upload dos arquivos:**
   - Faça upload de todos os arquivos do projeto
   - Certifique-se de que `app.py` está na raiz

4. **Aguarde o build:**
   - O HF fará o build automaticamente
   - Acesse seu Space quando estiver pronto

### Opção 2: Deploy Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar API key
export GROQ_API_KEY=sua_chave_aqui

# Executar aplicação
python app.py
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
GROQ_API_KEY=sua_chave_api_groq
```

### Como Obter a API Key da Groq

1. Acesse [console.groq.com](https://console.groq.com)
2. Crie uma conta ou faça login
3. Vá em **API Keys**
4. Crie uma nova chave
5. Copie e configure no Hugging Face

## 📋 Requisitos

- Python 3.8+
- Gradio 4.0.0
- Groq API Key
- Dependências listadas em `requirements.txt`

## 🏗️ Estrutura do Projeto

```
NexusEducation/
├── app.py              # Interface principal (Gradio)
├── i18n.py             # Sistema de internacionalização
├── pdf_tools.py        # Ferramentas de análise e geração de PDF
├── auth.py             # Sistema de autenticação
├── utils.py            # Utilitários gerais
├── requirements.txt    # Dependências do projeto
├── README.md           # Este arquivo
└── README_HF.md       # Documentação específica para HF
```

## 🌐 Tecnologias Utilizadas

- **Frontend**: Gradio (Interface web responsiva)
- **IA**: Groq API (Llama 3.1 70B)
- **Processamento**: Docling (Conversão de documentos)
- **PDF**: FPDF (Geração de relatórios)
- **Internacionalização**: Sistema customizado i18n

## 📱 Como Usar

### 1. **Acesso à Interface**
- A interface principal carrega automaticamente
- Use o menu lateral para navegar entre as funcionalidades

### 2. **Análise de Ementas**
1. Clique em **"+ Nova Análise"**
2. Preencha os dados do aluno
3. Faça upload do PDF da ementa
4. Clique em **"Analisar PDF"**
5. Adicione ao histórico e gere relatórios

### 3. **Troca de Idioma**
- Use o dropdown **"Idioma"** na barra lateral
- Alterna entre português e inglês em tempo real

### 4. **Geração de PDFs**
- Adicione análises ao histórico
- Clique em **"Gerar PDF"** para criar relatórios
- Download automático dos arquivos gerados

## 🔒 Segurança

- Autenticação de usuários
- Validação de arquivos PDF
- Tratamento seguro de erros
- Isolamento de dados por usuário

## 🐛 Solução de Problemas

### **API não configurada**
- Verifique se `GROQ_API_KEY` está configurada no HF
- Confirme se a chave é válida

### **PDF não é gerado**
- Verifique se há análises no histórico
- Confirme se o arquivo foi criado com sucesso

### **Internacionalização não funciona**
- Recarregue a página após trocar o idioma
- Verifique se todos os textos foram atualizados

### **Erro no Hugging Face**
- Verifique os logs do build
- Confirme se todos os arquivos estão na raiz
- Verifique se as dependências estão corretas

## 📞 Suporte

Para suporte técnico ou dúvidas:

- **Issues**: Use o sistema de issues do GitHub
- **Documentação**: Consulte este README
- **Comunidade**: Participe da comunidade Hugging Face

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📈 Roadmap

- [ ] Integração com mais modelos de IA
- [ ] Sistema de banco de dados persistente
- [ ] API REST para integrações
- [ ] Suporte a mais idiomas
- [ ] Análise de múltiplos PDFs simultaneamente
- [ ] Exportação para outros formatos

## 🎯 Status do Projeto

- ✅ **Internacionalização**: Funcionando (PT/EN)
- ✅ **Geração de PDF**: Funcionando
- ✅ **Interface Gradio**: Otimizada para HF
- ✅ **Sistema de Autenticação**: Implementado
- ✅ **Análise de PDFs**: Funcionando com Groq API

---

**Desenvolvido com ❤️ para a comunidade educacional**

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024  
**Compatível com**: Hugging Face Spaces ✅
