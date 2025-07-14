"""
Módulo de internacionalização para o Nexus Education
"""

class I18n:
    def __init__(self):
        self.current_language = 'pt'
        self.translations = {
            'pt': {
                'bem_vindo': '## Bem-vindo ao Nexus Education!\nAqui você pode analisar ementas de disciplinas e gerar relatórios inteligentes.\nClique no botão "+" para iniciar uma nova análise.',
                'ementas_anal': 'Ementas analisadas',
                'nova_analise': '+ Nova Análise',
                'menu': '## Menu',
                'inicio': 'Início',
                'config': 'Configurações',
                'tema': 'Tema da Página',
                'local': 'Instituto/Câmpus',
                'curso': 'Curso',
                'salvar': 'Salvar Configurações',
                'configuracoes': '# Configurações',
                'idioma': 'Idioma',
                'logo': 'Logo do Projeto',
                'login_titulo': '# Login do Professor',
                'login_email': 'E-mail',
                'login_senha': 'Senha',
                'login_entrar': 'Entrar',
                'login_nao_tem_conta': 'Não tem conta? Cadastre-se',
                'login_ja_tem_conta': 'Já tem conta? Faça login',
                'cadastro_titulo': '# Cadastro do Professor',
                'cadastro_email': 'E-mail',
                'cadastro_senha': 'Senha',
                'cadastro_instituto': 'Instituto',
                'cadastro_campus': 'Câmpus',
                'cadastro_curso': 'Curso',
                'cadastro_btn': 'Cadastrar',
                'pdf_resposta': 'Resposta',
                'add_pdf': 'Adicionar ao histórico do PDF',
                'gerar_pdf': 'Gerar PDF',
                'download_pdf': 'Download do PDF Respostas',
                'resetar': 'Quero analisar outro Documento!',
                'nome_aluno': 'Nome do Aluno',
                'matricula': 'Matrícula',
                'curso_destino': 'Curso de Destino',
                'codigo_curso': 'Código do Curso de Destino',
                'carga_horaria': 'Carga Horária do Curso de Destino',
                'avancar_upload': 'Avançar para Upload do PDF',
                'voltar': 'Voltar',
            },
            'en': {
                'bem_vindo': '## Welcome to Nexus Education!\nHere you can analyze course syllabi and generate smart reports.\nClick the "+" button to start a new analysis.',
                'ementas_anal': 'Analyzed Syllabi',
                'nova_analise': '+ New Analysis',
                'menu': '## Menu',
                'inicio': 'Home',
                'config': 'Settings',
                'tema': 'Theme',
                'local': 'Institute/Campus',
                'curso': 'Course',
                'salvar': 'Save Settings',
                'configuracoes': '# Settings',
                'idioma': 'Language',
                'logo': 'Project Logo',
                'login_titulo': '# Teacher Login',
                'login_email': 'E-mail',
                'login_senha': 'Password',
                'login_entrar': 'Sign In',
                'login_nao_tem_conta': 'Don\'t have an account? Register',
                'login_ja_tem_conta': 'Already have an account? Login',
                'cadastro_titulo': '# Teacher Registration',
                'cadastro_email': 'E-mail',
                'cadastro_senha': 'Password',
                'cadastro_instituto': 'Institute',
                'cadastro_campus': 'Campus',
                'cadastro_curso': 'Course',
                'cadastro_btn': 'Register',
                'pdf_resposta': 'Answer',
                'add_pdf': 'Add to PDF history',
                'gerar_pdf': 'Generate PDF',
                'download_pdf': 'Download PDF Answers',
                'resetar': 'I want to analyze another document!',
                'nome_aluno': 'Student Name',
                'matricula': 'Registration',
                'curso_destino': 'Destination Course',
                'codigo_curso': 'Course Code',
                'carga_horaria': 'Course Workload',
                'avancar_upload': 'Continue to PDF Upload',
                'voltar': 'Back',
            }
        }
    
    def get_text(self, key, language=None):
        """Obtém o texto traduzido para a chave especificada"""
        lang = language or self.current_language
        return self.translations.get(lang, self.translations['pt']).get(key, key)
    
    def set_language(self, language):
        """Define o idioma atual"""
        if language in self.translations:
            self.current_language = language
    
    def get_all_texts(self, language=None):
        """Retorna todos os textos para o idioma especificado"""
        lang = language or self.current_language
        return self.translations.get(lang, self.translations['pt'])
    
    def update_interface_texts(self, language):
        """Atualiza todos os textos da interface para o idioma especificado"""
        self.set_language(language)
        texts = self.get_all_texts(language)
        
        return (
            # Add Análise
            texts['logo'], texts['bem_vindo'], texts['ementas_anal'], texts['nova_analise'],
            # Configurações
            texts['configuracoes'], texts['tema'], texts['local'], texts['curso'], texts['salvar'],
            # Menu
            texts['menu'], texts['inicio'], texts['config'], texts['idioma'],
            # Login
            texts['login_titulo'], texts['login_email'], texts['login_senha'], texts['login_entrar'], texts['login_nao_tem_conta'],
            # Cadastro
            texts['cadastro_titulo'], texts['cadastro_email'], texts['cadastro_senha'], texts['cadastro_instituto'], texts['cadastro_campus'], texts['cadastro_curso'], texts['cadastro_btn'], texts['login_ja_tem_conta'],
            # PDF/Análise
            texts['pdf_resposta'], texts['add_pdf'], texts['gerar_pdf'], texts['download_pdf'], texts['resetar'],
            # Formulário
            texts['nome_aluno'], texts['matricula'], texts['curso_destino'], texts['codigo_curso'], texts['carga_horaria'], texts['avancar_upload'], texts['voltar'],
            # Estado do idioma
            language
        )

# Instância global do sistema de internacionalização
i18n = I18n() 