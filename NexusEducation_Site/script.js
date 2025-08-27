// Estado global da aplicação
const appState = {
    currentSection: 'login',
    currentUser: null,
    currentLanguage: 'pt',
    currentTheme: 'light',
    uploadedFiles: [],
    analysisHistory: []
};

// Elementos DOM
const elements = {
    sections: {},
    forms: {},
    buttons: {},
    inputs: {}
};

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserPreferences();
});

// Inicialização da aplicação
function initializeApp() {
    // Mapear seções
    elements.sections = {
        login: document.getElementById('loginSection'),
        register: document.getElementById('registerSection'),
        dashboard: document.getElementById('dashboardSection'),
        newAnalysis: document.getElementById('newAnalysisSection'),
        pdfUpload: document.getElementById('pdfUploadSection'),
        results: document.getElementById('resultsSection')
    };

    // Mapear formulários
    elements.forms = {
        login: document.getElementById('loginForm'),
        register: document.getElementById('registerForm'),
        analysis: document.getElementById('analysisForm')
    };

    // Mapear botões
    elements.buttons = {
        languageToggle: document.getElementById('languageToggle'),
        themeToggle: document.getElementById('themeToggle'),
        showRegister: document.getElementById('showRegister'),
        showLogin: document.getElementById('showLogin'),
        newAnalysis: document.getElementById('newAnalysisBtn'),
        backToDashboard: document.getElementById('backToDashboard'),
        backToAnalysis: document.getElementById('backToAnalysis'),
        backToUpload: document.getElementById('backToUpload'),
        analyzeBtn: document.getElementById('analyzeBtn'),
        addToHistoryBtn: document.getElementById('addToHistoryBtn'),
        generatePdfBtn: document.getElementById('generatePdfBtn'),
        resetBtn: document.getElementById('resetBtn')
    };

    // Mapear inputs
    elements.inputs = {
        fileInput: document.getElementById('fileInput'),
        uploadArea: document.getElementById('uploadArea')
    };

    // Mostrar seção inicial
    showSection('login');
}

// Configuração dos event listeners
function setupEventListeners() {
    // Navegação entre seções
    elements.buttons.showRegister.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('register');
    });

    elements.buttons.showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('login');
    });

    elements.buttons.newAnalysis.addEventListener('click', () => {
        showSection('newAnalysis');
    });

    elements.buttons.backToDashboard.addEventListener('click', () => {
        showSection('dashboard');
    });

    elements.buttons.backToAnalysis.addEventListener('click', () => {
        showSection('newAnalysis');
    });

    elements.buttons.backToUpload.addEventListener('click', () => {
        showSection('pdfUpload');
    });

    // Formulários
    elements.forms.login.addEventListener('submit', handleLogin);
    elements.forms.register.addEventListener('submit', handleRegister);
    elements.forms.analysis.addEventListener('submit', handleAnalysisForm);

    // Botões de ação
    elements.buttons.analyzeBtn.addEventListener('click', handleAnalyze);
    elements.buttons.addToHistoryBtn.addEventListener('click', handleAddToHistory);
    elements.buttons.generatePdfBtn.addEventListener('click', handleGeneratePdf);
    elements.buttons.resetBtn.addEventListener('click', handleReset);

    // Toggle de idioma e tema
    elements.buttons.languageToggle.addEventListener('click', toggleLanguage);
    elements.buttons.themeToggle.addEventListener('click', toggleTheme);

    // Upload de arquivos
    setupFileUpload();
}

// Configuração do upload de arquivos
function setupFileUpload() {
    const uploadArea = elements.inputs.uploadArea;
    const fileInput = elements.inputs.fileInput;

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        handleFileSelection(files);
    });

    // Clique para selecionar
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFileSelection(files);
    });
}

// Manipulação da seleção de arquivos
function handleFileSelection(files) {
    const pdfFiles = files.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length === 0) {
        showToast('Por favor, selecione apenas arquivos PDF', 'warning');
        return;
    }

    appState.uploadedFiles = pdfFiles;
    updateUploadedFilesList();
    elements.buttons.analyzeBtn.disabled = false;
    
    showToast(`${pdfFiles.length} arquivo(s) selecionado(s) com sucesso!`, 'success');
}

// Atualizar lista de arquivos enviados
function updateUploadedFilesList() {
    const uploadedFilesContainer = document.getElementById('uploadedFiles');
    
    if (appState.uploadedFiles.length === 0) {
        uploadedFilesContainer.innerHTML = '';
        return;
    }

    const filesList = appState.uploadedFiles.map((file, index) => `
        <div class="file-item">
            <i class="fas fa-file-pdf"></i>
            <span>${file.name}</span>
            <button class="btn-remove-file" onclick="removeFile(${index})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');

    uploadedFilesContainer.innerHTML = filesList;
}

// Remover arquivo
function removeFile(index) {
    appState.uploadedFiles.splice(index, 1);
    updateUploadedFilesList();
    
    if (appState.uploadedFiles.length === 0) {
        elements.buttons.analyzeBtn.disabled = true;
    }
}

// Navegação entre seções
function showSection(sectionName) {
    // Ocultar todas as seções
    Object.values(elements.sections).forEach(section => {
        section.classList.remove('active');
    });

    // Mostrar seção selecionada
    if (elements.sections[sectionName]) {
        elements.sections[sectionName].classList.add('active');
        appState.currentSection = sectionName;
    }

    // Atualizar navegação ativa
    updateActiveNavigation(sectionName);
}

// Atualizar navegação ativa
function updateActiveNavigation(sectionName) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    const activeLink = document.querySelector(`[href="#${sectionName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Manipulação de login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showToast('Por favor, preencha todos os campos', 'error');
        return;
    }

    showLoading(true);

    try {
        // Simular autenticação (substituir por chamada real à API)
        await simulateApiCall(1000);
        
        appState.currentUser = {
            email: email,
            name: email.split('@')[0],
            institute: 'Instituto Exemplo',
            campus: 'Campus Principal',
            course: 'Ciência da Computação'
        };

        showToast('Login realizado com sucesso!', 'success');
        showSection('dashboard');
        updateDashboard();
        
    } catch (error) {
        showToast('Erro no login. Tente novamente.', 'error');
    } finally {
        showLoading(false);
    }
}

// Manipulação de cadastro
async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const institute = document.getElementById('registerInstitute').value;
    const campus = document.getElementById('registerCampus').value;
    const course = document.getElementById('registerCourse').value;

    if (!email || !password || !institute || !campus || !course) {
        showToast('Por favor, preencha todos os campos', 'error');
        return;
    }

    showLoading(true);

    try {
        // Simular cadastro (substituir por chamada real à API)
        await simulateApiCall(1500);
        
        showToast('Cadastro realizado com sucesso! Faça login para continuar.', 'success');
        showSection('login');
        
        // Limpar formulário
        elements.forms.register.reset();
        
    } catch (error) {
        showToast('Erro no cadastro. Tente novamente.', 'error');
    } finally {
        showLoading(false);
    }
}

// Manipulação do formulário de análise
function handleAnalysisForm(e) {
    e.preventDefault();
    
    const studentName = document.getElementById('studentName').value;
    const studentId = document.getElementById('studentId').value;
    const targetCourse = document.getElementById('targetCourse').value;
    const courseCode = document.getElementById('courseCode').value;
    const workload = document.getElementById('workload').value;

    if (!studentName || !studentId || !targetCourse || !courseCode || !workload) {
        showToast('Por favor, preencha todos os campos', 'error');
        return;
    }

    // Salvar dados do aluno no estado
    appState.currentStudent = {
        name: studentName,
        id: studentId,
        targetCourse: targetCourse,
        courseCode: courseCode,
        workload: workload
    };

    showSection('pdfUpload');
}

// Manipulação da análise
async function handleAnalyze() {
    if (appState.uploadedFiles.length === 0) {
        showToast('Por favor, selecione arquivos para análise', 'warning');
        return;
    }

    showLoading(true);

    try {
        // Simular análise (substituir por chamada real à API)
        await simulateApiCall(3000);
        
        // Simular resultados
        const mockResults = generateMockResults();
        
        showSection('results');
        displayResults(mockResults);
        
        showToast('Análise concluída com sucesso!', 'success');
        
    } catch (error) {
        showToast('Erro na análise. Tente novamente.', 'error');
    } finally {
        showLoading(false);
    }
}

// Gerar resultados simulados
function generateMockResults() {
    const disciplines = [
        'Cálculo I', 'Física I', 'Programação I', 'Álgebra Linear',
        'Estatística', 'Estrutura de Dados', 'Banco de Dados'
    ];
    
    const recognized = Math.floor(Math.random() * disciplines.length) + 1;
    const credits = Math.floor(Math.random() * 20) + 10;
    
    return {
        disciplinesCount: disciplines.length,
        creditsCount: credits,
        status: 'Concluída',
        details: disciplines.slice(0, recognized).map(discipline => ({
            name: discipline,
            status: 'Reconhecida',
            credits: Math.floor(Math.random() * 4) + 2
        }))
    };
}

// Exibir resultados
function displayResults(results) {
    document.getElementById('disciplinesCount').textContent = results.disciplinesCount;
    document.getElementById('creditsCount').textContent = results.creditsCount;
    document.getElementById('analysisStatus').textContent = results.status;
    
    const detailsContainer = document.getElementById('analysisDetails');
    const detailsHTML = results.details.map(discipline => `
        <div class="discipline-item">
            <span class="discipline-name">${discipline.name}</span>
            <span class="discipline-status success">${discipline.status}</span>
            <span class="discipline-credits">${discipline.credits} créditos</span>
        </div>
    `).join('');
    
    detailsContainer.innerHTML = detailsHTML;
}

// Adicionar ao histórico
function handleAddToHistory() {
    if (appState.currentStudent && appState.uploadedFiles.length > 0) {
        const analysis = {
            id: Date.now(),
            student: appState.currentStudent,
            files: appState.uploadedFiles.map(f => f.name),
            date: new Date().toLocaleDateString('pt-BR'),
            status: 'Concluída'
        };
        
        appState.analysisHistory.push(analysis);
        showToast('Análise adicionada ao histórico!', 'success');
    }
}

// Gerar PDF
function handleGeneratePdf() {
    showToast('Gerando PDF...', 'info');
    
    // Simular geração de PDF
    setTimeout(() => {
        showToast('PDF gerado com sucesso!', 'success');
        
        // Criar link de download simulado
        const link = document.createElement('a');
        link.href = '#';
        link.download = 'analise_pds.pdf';
        link.click();
    }, 2000);
}

// Reset da aplicação
function handleReset() {
    appState.uploadedFiles = [];
    appState.currentStudent = null;
    
    // Limpar formulários
    elements.forms.analysis.reset();
    
    // Voltar para o dashboard
    showSection('dashboard');
    
    showToast('Aplicação resetada com sucesso!', 'success');
}

// Toggle de idioma
function toggleLanguage() {
    appState.currentLanguage = appState.currentLanguage === 'pt' ? 'en' : 'pt';
    
    const languageSpan = elements.buttons.languageToggle.querySelector('span');
    languageSpan.textContent = appState.currentLanguage.toUpperCase();
    
    // Atualizar textos da interface (implementar sistema de i18n)
    updateInterfaceLanguage(appState.currentLanguage);
    
    showToast(`Idioma alterado para ${appState.currentLanguage === 'pt' ? 'Português' : 'English'}`, 'info');
    
    // Salvar preferência
    localStorage.setItem('nexus_language', appState.currentLanguage);
}

// Toggle de tema
function toggleTheme() {
    appState.currentTheme = appState.currentTheme === 'light' ? 'dark' : 'light';
    
    const themeIcon = elements.buttons.themeToggle.querySelector('i');
    themeIcon.className = appState.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    
    document.documentElement.setAttribute('data-theme', appState.currentTheme);
    
    showToast(`Tema alterado para ${appState.currentTheme === 'light' ? 'Claro' : 'Escuro'}`, 'info');
    
    // Salvar preferência
    localStorage.setItem('nexus_theme', appState.currentTheme);
}

// Atualizar idioma da interface
function updateInterfaceLanguage(language) {
    // Implementar sistema de internacionalização
    // Por enquanto, apenas placeholder
    console.log(`Atualizando idioma para: ${language}`);
}

// Atualizar dashboard
function updateDashboard() {
    if (appState.currentUser) {
        document.getElementById('userName').textContent = appState.currentUser.name;
        
        // Atualizar lista de análises
        updateAnalysesList();
    }
}

// Atualizar lista de análises
function updateAnalysesList() {
    const analysesList = document.getElementById('analysesList');
    
    if (appState.analysisHistory.length === 0) {
        analysesList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>Nenhuma análise encontrada</p>
                <small>Comece criando sua primeira análise</small>
            </div>
        `;
        return;
    }
    
    const analysesHTML = appState.analysisHistory.map(analysis => `
        <div class="analysis-item">
            <div class="analysis-info">
                <h4>${analysis.student.name}</h4>
                <p>${analysis.student.targetCourse}</p>
                <small>${analysis.date}</small>
            </div>
            <div class="analysis-status">
                <span class="status-badge ${analysis.status.toLowerCase()}">${analysis.status}</span>
            </div>
        </div>
    `).join('');
    
    analysesList.innerHTML = analysesHTML;
}

// Mostrar/ocultar loading
function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (show) {
        loadingOverlay.classList.add('active');
    } else {
        loadingOverlay.classList.remove('active');
    }
}

// Sistema de notificações toast
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        toast.remove();
    }, 5000);
    
    // Remover ao clicar
    toast.addEventListener('click', () => {
        toast.remove();
    });
}

// Obter ícone do toast baseado no tipo
function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    return icons[type] || 'info-circle';
}

// Simular chamada de API
function simulateApiCall(delay) {
    return new Promise((resolve) => {
        setTimeout(resolve, delay);
    });
}

// Carregar preferências do usuário
function loadUserPreferences() {
    const savedLanguage = localStorage.getItem('nexus_language');
    const savedTheme = localStorage.getItem('nexus_theme');
    
    if (savedLanguage) {
        appState.currentLanguage = savedLanguage;
        const languageSpan = elements.buttons.languageToggle.querySelector('span');
        if (languageSpan) {
            languageSpan.textContent = savedLanguage.toUpperCase();
        }
    }
    
    if (savedTheme) {
        appState.currentTheme = savedTheme;
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const themeIcon = elements.buttons.themeToggle.querySelector('i');
        if (themeIcon) {
            themeIcon.className = savedTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// Adicionar estilos CSS dinâmicos para elementos adicionais
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .file-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: var(--bg-primary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            margin-bottom: 0.5rem;
        }
        
        .file-item i {
            color: var(--error-color);
            font-size: 1.2rem;
        }
        
        .btn-remove-file {
            background: var(--error-color);
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: var(--radius-sm);
            cursor: pointer;
            margin-left: auto;
        }
        
        .discipline-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: var(--bg-primary);
            border-radius: var(--radius-md);
            margin-bottom: 0.5rem;
            border: 1px solid var(--border-light);
        }
        
        .discipline-status.success {
            color: var(--success-color);
            font-weight: 600;
        }
        
        .empty-state {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
        }
        
        .empty-state i {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        .analysis-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            margin-bottom: 0.5rem;
            border: 1px solid var(--border-light);
        }
        
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-md);
            font-size: 0.875rem;
            font-weight: 600;
        }
        
        .status-badge.concluída {
            background: var(--success-color);
            color: white;
        }
        
        .toast-content {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .toast-content i {
            font-size: 1.2rem;
        }
    `;
    
    document.head.appendChild(style);
}

// Adicionar estilos dinâmicos quando a página carregar
document.addEventListener('DOMContentLoaded', addDynamicStyles);


