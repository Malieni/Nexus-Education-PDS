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

## 🚀 Como Usar

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

## 🔧 Configuração

### Variáveis de Ambiente

Para funcionar corretamente, configure a variável de ambiente:

```bash
GROQ_API_KEY=sua_chave_api_aqui
```

### Como Configurar no Hugging Face

1. Acesse seu Space no Hugging Face
2. Vá em **Settings** → **Repository secrets**
3. Adicione a variável `GROQ_API_KEY` com sua chave da Groq

## 📋 Requisitos

- Python 3.8+
- Gradio 4.0.0
- Groq API Key
- Dependências listadas em `requirements.txt`

## 🏗️ Arquitetura

```
NexusEducation/
├── app.py              # Interface principal (Gradio)
├── i18n.py             # Sistema de internacionalização
├── pdf_tools.py        # Ferramentas de análise e geração de PDF
├── auth.py             # Sistema de autenticação
├── utils.py            # Utilitários gerais
└── requirements.txt    # Dependências do projeto
```

## 🌐 Tecnologias Utilizadas

- **Frontend**: Gradio (Interface web responsiva)
- **IA**: Groq API (Llama 3.1 70B)
- **Processamento**: Docling (Conversão de documentos)
- **PDF**: FPDF (Geração de relatórios)
- **Internacionalização**: Sistema customizado i18n

## 📱 Interface

A interface é organizada em páginas modulares:

- **Login/Cadastro** - Autenticação de usuários
- **Início** - Dashboard principal e configurações
- **Formulário** - Coleta de dados do aluno
- **Análise** - Upload e processamento de PDFs
- **Histórico** - Gerenciamento de análises anteriores

## 🔒 Segurança

- Autenticação de usuários
- Validação de arquivos PDF
- Tratamento seguro de erros
- Isolamento de dados por usuário

## 🐛 Solução de Problemas

### **API não configurada**
- Verifique se `GROQ_API_KEY` está configurada
- Confirme se a chave é válida

### **PDF não é gerado**
- Verifique se há análises no histórico
- Confirme se o arquivo foi criado com sucesso

### **Internacionalização não funciona**
- Recarregue a página após trocar o idioma
- Verifique se todos os textos foram atualizados

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

---

**Desenvolvido com ❤️ para a comunidade educacional**

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024
