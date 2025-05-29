# Nexus Education - Sistema de Análise Semântica de Ementas

## Visão Geral

O Nexus Education é um sistema inteligente que utiliza análise semântica para avaliar se estudantes estão preparados para ingressar em cursos específicos, baseando-se na comparação entre suas ementas acadêmicas e os requisitos dos cursos desejados.

## Funcionalidades Principais

### 🎯 Análise Semântica Inteligente
- Upload de ementas em PDF
- Conversão automática para JSON estruturado
- Análise de similaridade usando IA e NLP
- Relatório detalhado com percentual de compatibilidade

### 👨‍🏫 Sistema de Autenticação para Professores
- Login seguro com validação de domínio institucional
- Sessões individualizadas por professor
- Controle de acesso baseado em email institucional

### 📊 Relatórios Detalhados
- Percentual de similaridade entre ementa e curso
- Identificação de conhecimentos já adquiridos
- Mapeamento de lacunas de aprendizado
- Recomendações personalizadas para preparação
- Classificação do nível de preparação

### 🗄️ Sistema de Persistência
- Banco de dados MongoDB para armazenamento
- Histórico completo de análises por professor
- Clusterização de documentos para otimização
- Gestão de cursos e ementas

### 📈 Visualizações Interativas
- Gráficos de similaridade em tempo real
- Histórico de evolução das análises
- Dashboard com métricas de desempenho
- Relatórios exportáveis

## Tecnologias Utilizadas

### Backend e IA
- **Python 3.9+**: Linguagem principal
- **LangChain**: Framework para aplicações de IA
- **OpenAI GPT**: Modelo de linguagem para análise semântica
- **Sentence Transformers**: Embeddings para similaridade semântica
- **scikit-learn**: Métricas de similaridade coseno

### Interface e Visualização
- **Streamlit**: Framework web para interface
- **Plotly**: Gráficos interativos e dashboards
- **Pandas**: Manipulação de dados estruturados

### Banco de Dados e Persistência
- **MongoDB**: Banco NoSQL para documentos
- **PyMongo**: Driver Python para MongoDB

### Processamento de Documentos
- **PyPDF2**: Extração de texto de PDFs
- **Regex**: Parsing estruturado de ementas

## Instalação e Configuração

### Pré-requisitos
- Python 3.9 ou superior
- MongoDB (local ou remoto)
- Chave da API OpenAI
- Docker (opcional)

### Instalação Local

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/nexus-education.git
cd nexus-education
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
# Crie um arquivo .env
OPENAI_API_KEY=sua_chave_openai_aqui
MONGODB_URI=mongodb://localhost:27017/
GOOGLE_CLIENT_ID=seu_google_client_id
GOOGLE_CLIENT_SECRET=seu_google_client_secret
```

4. **Execute a aplicação:**
```bash
streamlit run app.py
```

### Instalação com Docker

1. **Configure o arquivo .env**

2. **Execute com Docker Compose:**
```bash
docker-compose up -d
```

A aplicação estará disponível em `http://localhost:8501`

## Como Usar

### 1. Login
- Acesse a aplicação
- Use um email institucional terminado em `@universidade.edu.br`
- Senha padrão para demonstração: `professor123`

### 2. Realizar Análise
1. Faça upload do PDF da ementa do aluno
2. Selecione o curso desejado
3. Clique em "Realizar Análise Semântica"
4. Visualize o relatório detalhado com:
   - Percentual de similaridade
   - Nível de preparação
   - Conhecimentos adquiridos
   - Lacunas identificadas
   - Recomendações personalizadas

### 3. Gerenciar Cursos
- Adicione novos cursos com disciplinas e pré-requisitos
- Visualize cursos existentes
- Configure competências exigidas

### 4. Histórico
- Acesse análises anteriores
- Visualize gráficos de evolução
- Exporte relatórios

## Estrutura do Projeto

```
nexus-education/
├── app.py                 # Aplicação principal Streamlit
├── config.py             # Configurações e variáveis de ambiente
├── database.py           # Gerenciamento do banco MongoDB
├── pdf_processor.py      # Processamento de PDFs
├── semantic_analyzer.py  # Análise semântica com IA
├── auth.py              # Autenticação de usuários
├── requirements.txt     # Dependências Python
└── README.md           # Documentação
```

## Arquitetura do Sistema

### Fluxo de Análise
1. **Upload**: Professor faz upload do PDF da ementa
2. **Processamento**: Sistema extrai e estrutura dados em JSON
3. **Análise**: IA compara ementa com requisitos do curso
4. **Relatório**: Geração de parecer detalhado
5. **Persistência**: Dados salvos para clusterização e histórico

### Componentes Principais
- **PDF Processor**: Extração e parsing de documentos
- **Semantic Analyzer**: Análise de similaridade com IA
- **Database Manager**: Persistência e recuperação de dados
- **Auth Manager**: Controle de acesso de professores
- **Web Interface**: Interface amigável com Streamlit

## Exemplos de Uso

### Cenário 1: Análise de Transferência
Um aluno de Análise de Sistemas deseja migrar para Engenharia de Software. O sistema:
1. Analisa sua ementa atual
2. Compara com requisitos de Engenharia de Software
3. Identifica 75% de compatibilidade
4. Recomenda disciplinas específicas para nivelamento

### Cenário 2: Validação de Pré-requisitos
Professor avalia se aluno tem base para curso avançado:
1. Upload da ementa do aluno
2. Análise automática de competências
3. Relatório indica pontos fortes e fracos
4. Decisão fundamentada sobre admissão

## Personalização

### Adicionando Novos Cursos
```python
curso_data = {
    'nome': 'Seu Curso',
    'disciplinas_base': ['Disciplina 1', 'Disciplina 2'],
    'pre_requisitos': ['Requisito 1'],
    'competencias_exigidas': ['Competência 1']
}
```

### Configurando Domínios Autorizados
Edite `auth.py` para adicionar novos domínios institucionais:
```python
authorized_domains = [
    '@sua-universidade.edu.br',
    '@instituto.edu.br'
]
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

MIT License - veja LICENSE.md para detalhes

## Suporte

Para suporte técnico:
- Email: suporte@nexuseducation.com
- Issues: GitHub Issues
- Documentação: Wiki do projeto

---

**Desenvolvido com ❤️ para democratizar o acesso à educação através da tecnologia**
"""
