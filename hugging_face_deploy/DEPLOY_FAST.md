# 🚀 DEPLOY RÁPIDO - Nexus Education

## ⚡ **PASSOS ESSENCIAIS (5 minutos)**

### **1. Criar Space no HF**
- Acesse: [huggingface.co/spaces](https://huggingface.co/spaces)
- **Create new Space** → **Gradio** → **nexus-education**

### **2. Configurar API Key**
- **Settings** → **Repository secrets**
- **Name**: `GROQ_API_KEY`
- **Value**: Sua chave da Groq

### **3. Upload dos Arquivos**
- **Files** → **Add file** → **Upload files**
- **Selecione TODOS os arquivos** desta pasta
- **NÃO crie subpastas** - tudo na raiz!
- **Commit changes**

### **4. Aguardar Build**
- Monitore **Build logs**
- Aguarde **"Build completed successfully"**

### **5. Testar**
- Acesse seu Space
- Teste: idioma, upload PDF, geração de relatórios

---

## 📁 **ARQUIVOS INCLUÍDOS**

✅ `app.py` - Interface principal  
✅ `requirements.txt` - Dependências  
✅ `i18n.py` - Internacionalização  
✅ `pdf_tools.py` - Ferramentas PDF  
✅ `auth.py` - Autenticação  
✅ `utils.py` - Utilitários  
✅ `README.md` - Documentação  
✅ `.gitignore` - Config Git  

---

## ⚠️ **PONTOS CRÍTICOS**

- ❌ **NÃO crie subpastas** no HF
- ❌ **NÃO altere** nomes dos arquivos
- ✅ **Configure** `GROQ_API_KEY`
- ✅ **Aguarde** build completar
- ✅ **Teste** todas as funcionalidades

---

## 🆘 **PROBLEMAS COMUNS**

| Problema | Solução |
|----------|---------|
| Build failed | Verificar se todos os arquivos estão na raiz |
| Module not found | Confirmar upload de todos os arquivos Python |
| API error | Configurar `GROQ_API_KEY` corretamente |
| Interface não carrega | Aguardar build completar |

---

**🎯 Status**: ✅ Pronto para deploy!  
**⏱️ Tempo estimado**: 5-10 minutos  
**📚 Documentação completa**: `INSTRUCOES_DEPLOY.md`
