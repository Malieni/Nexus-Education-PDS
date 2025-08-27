# 🚀 Guia de Deploy - Nexus Education PDS

## 🌐 **Opções de Hospedagem**

### 1️⃣ **Streamlit Cloud (RECOMENDADO - Gratuito)**

#### **Passos:**
1. **Push para GitHub:**
   ```bash
   git add .
   git commit -m "Aplicação pronta para deploy"
   git push origin main
   ```

2. **Acesse:** https://share.streamlit.io/
3. **Login com GitHub**
4. **New App:**
   - Repository: `seu-usuario/nexus-education-pds`
   - Branch: `main`
   - Main file path: `NexusEducation_Ferramenta/streamlit_version/app_streamlit.py`

5. **Configure variáveis:**
   - **chave**: `sua-api-key-do-groq`

6. **Deploy!**

**✅ Vantagens:** Gratuito, automático, HTTPS, sem configuração

---

### 2️⃣ **Render (Gratuito)**

#### **Passos:**
1. **Acesse:** https://render.com/
2. **Sign up com GitHub**
3. **New Web Service**
4. **Connect repository**
5. **Configure:**
   - **Name:** `nexus-education-pds`
   - **Environment:** `Python 3`
   - **Build Command:** `cd streamlit_version && pip install -r requirements.txt`
   - **Start Command:** `cd streamlit_version && streamlit run app_streamlit.py --server.port $PORT --server.address 0.0.0.0`

6. **Environment Variables:**
   - **chave:** `sua-api-key-do-groq`

7. **Create Web Service**

**✅ Vantagens:** Gratuito, automático, customizável

---

### 3️⃣ **Railway (Gratuito)**

#### **Passos:**
1. **Instale Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Configure variáveis:**
   ```bash
   railway variables set chave=sua-api-key-do-groq
   ```

**✅ Vantagens:** Rápido, simples, gratuito

---

### 4️⃣ **Heroku (Pago)**

#### **Passos:**
1. **Instale Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Crie app:**
   ```bash
   heroku create nexus-education-pds
   ```

4. **Configure variáveis:**
   ```bash
   heroku config:set chave=sua-api-key-do-groq
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

**✅ Vantagens:** Robusto, confiável, escalável

---

### 5️⃣ **VPS/Servidor Próprio**

#### **Configuração Ubuntu/Debian:**

1. **Atualize o servidor:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip nginx git -y
   ```

2. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/nexus-education-pds.git
   cd nexus-education-pds/NexusEducation_Ferramenta/streamlit_version
   ```

3. **Instale dependências:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure variáveis:**
   ```bash
   export chave="sua-api-key-do-groq"
   ```

5. **Crie serviço systemd:**
   ```bash
   sudo nano /etc/systemd/system/nexus-pds.service
   ```

   ```ini
   [Unit]
   Description=Nexus Education PDS
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/nexus-education-pds/NexusEducation_Ferramenta
   Environment="chave=sua-api-key-do-groq"
   ExecStart=/usr/local/bin/streamlit run app_streamlit.py --server.port 8501 --server.address 0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Ative o serviço:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable nexus-pds
   sudo systemctl start nexus-pds
   ```

7. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/nexus-pds
   ```

   ```nginx
   server {
       listen 80;
       server_name seu-dominio.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

8. **Ative o site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/nexus-pds /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

**✅ Vantagens:** Controle total, sem custos recorrentes

---

## 🔧 **Configurações Importantes**

### **Variáveis de Ambiente:**
```bash
chave=sua-api-key-do-groq
```

### **Porta e Endereço:**
```bash
streamlit run app_streamlit.py --server.port $PORT --server.address 0.0.0.0
```

### **Requirements.txt:**
Certifique-se de que todas as dependências estão listadas.

---

## 🚀 **Deploy Rápido (Streamlit Cloud)**

1. **GitHub:** Faça push de todos os arquivos
2. **Streamlit Cloud:** Conecte o repositório
3. **Configure:** Caminho do arquivo e variáveis
4. **Deploy:** Clique e aguarde
5. **Acesso:** Sua aplicação estará online!

---

## 📱 **URLs de Acesso**

Após o deploy, sua aplicação estará disponível em:
- **Streamlit Cloud:** `https://seu-app.streamlit.app`
- **Render:** `https://nexus-education-pds.onrender.com`
- **Railway:** `https://nexus-education-pds.railway.app`
- **Heroku:** `https://nexus-education-pds.herokuapp.com`
- **VPS:** `http://seu-ip-ou-dominio.com`

---

**🎓 Sua aplicação estará online e acessível para todos!**
