# 🚀 Guia de Setup - SMS Forwarder

Instruções passo a passo para instalar e rodar o projeto.

## 📋 Pré-requisitos

### Obrigatório
- **Python 3.9+** - [Baixar](https://www.python.org/downloads/)
- **Git** - [Baixar](https://git-scm.com/download/win)
- **Android Studio** (para o app Android) - [Baixar](https://developer.android.com/studio)

### Verificar instalação

```bash
# Abrir CMD/PowerShell e testar:
python --version
git --version
```

## 🔧 Setup Backend (Python Flask)

### 1. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/sms-forwarder.git
cd sms-forwarder/backend
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Você deve ver (venv) no início da linha
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o Backend

```bash
python app.py
```

**Saída esperada:**
```
╔════════════════════════════════════════╗
║  SMS FORWARDER - BACKEND               ║
║  Backend iniciado!                     ║
╚════════════════════════════════════════╝

🚀 Servidor rodando em http://localhost:5000
📊 WebSocket disponível em ws://localhost:5000/socket.io
💾 Database: SMS armazenados por 5 horas
```

✅ Backend está rodando!

## 💻 Setup PC App (Windows)

### 1. Abrir novo CMD/PowerShell

```bash
# Não feche o CMD do Backend!
# Abra um novo CMD
cd sms-forwarder/pc-app
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o PC App

```bash
python pc_app.py
```

**Será pedido:**
```
URL do Backend [localhost:5000]: 
# Pressione Enter para usar localhost:5000
# Ou digite: seu-site.com:5000
```

**Saída esperada:**
```
╔═════════════════════════════════════════╗
║  SMS FORWARDER - MONITOR PC             ║
║  Windows CMD - Tempo Real               ║
╚═════════════════════════════════════════╝

[14:30:00] 🔌 Conectando a http://localhost:5000...
[14:30:01] ✅ Conectado ao Backend!
```

✅ PC App está rodando!

## 📱 Setup Android App

### 1. Instalar Android Studio

[Guia completo aqui](./android-app/SETUP.md)

### 2. Abrir projeto em Android Studio

```bash
Arquivo → Abrir → Selecionar pasta "android-app"
```

### 3. Configurar URL do Backend

Abrir: `android-app/app/src/main/kotlin/ApiClient.kt`

```kotlin
// Encontrar esta linha:
private const val BASE_URL = "http://192.168.1.100:5000"

// Substituir pelo seu IP/domínio:
// Localhost: http://localhost:5000 (não funciona no Android físico)
// IP local: http://192.168.1.100:5000 (RECOMENDADO)
// Domínio: https://seu-site.com
```

### 4. Compilar APK

```
Build → Build Bundle(s) / APK(s) → Build APK(s)
```

### 5. Instalar no Android

```
Run → Selecionar device → Run 'app'
```

### 6. Conceder Permissões

- ✅ Ler SMS
- ✅ Conectar à internet

## 📊 Testar o Sistema

### Teste 1: Backend ativo?

```bash
# Abrir navegador:
http://localhost:5000/health

# Deve aparecer:
{
  "status": "ok",
  "timestamp": "2026-07-25T...",
  "conectados": 1
}
```

### Teste 2: PC App recebe dados?

O PC App deve mostrar:
```
✓ ONLINE
Status: Conectado ao Backend!
```

### Teste 3: Enviar SMS de Teste (Android)

```bash
# Abra um terminal Android adb:
adb shell am start -n com.android.mms/.ui.ConversationList

# Ou envie um SMS real para o número do Android
# O app deve capturar e enviar ao Backend automaticamente
```

### Teste 4: PC App mostra SMS?

```
🟢 +5585987654321    (1 SMS)

[14:32] +5585987654321
       "Seu SMS aqui"
```

## 🔌 Conectar a um Servidor Cloud (Railway)

Deixar para depois se quiser.

### Se precisar depois:

1. Ir para [Railway.com](https://railway.com)
2. Fazer signup com GitHub
3. Criar novo projeto
4. Selecionar repo
5. Railway cria Postgres + deploy automático
6. Atualizar URL no Android App

## 🆘 Troubleshooting

### PC App não conecta

**Erro:** `Connection refused`

**Solução:**
```bash
# Verificar se Backend está rodando
# Terminal Backend deve estar mostrando:
# "Servidor rodando em http://localhost:5000"

# Verificar porta 5000:
netstat -ano | findstr :5000
```

### Android não envia SMS

**Solução:**
```
1. Verificar permissões no Android
   Settings → Apps → SMS Forwarder → Permissions
   
2. Verificar se URL está correta
   android-app/ApiClient.kt → BASE_URL
   
3. Conectar Android ao WiFi
   
4. Verificar firewall do PC
   - Abrir porta 5000
```

### Banco de dados cheio / SMS não aparecem

**Solução:**
```bash
# SMS são deletados automaticamente após 5 horas
# Se quiser limpar manualmente, delete:
backend/sms_database.db

# Backend recria o banco automaticamente
```

## 📚 Arquivos Importantes

```
sms-forwarder/
├── backend/
│   ├── app.py              # Servidor principal
│   ├── database.py         # Banco de dados
│   ├── sms_database.db     # Banco SQLite (criado automaticamente)
│   └── requirements.txt
│
├── pc-app/
│   ├── pc_app.py          # Program Windows
│   └── requirements.txt
│
└── android-app/           # (Abrir em Android Studio)
    ├── app/
    │   ├── src/
    │   │   ├── main/
    │   │   │   ├── kotlin/
    │   │   │   │   └── ApiClient.kt  # ← Mudar BASE_URL aqui
    │   │   │   └── AndroidManifest.xml
    │   └── build.gradle
```

## ⚠️ Notas Importantes

### 1. Porta 5000 em uso?

```bash
# Encontrar processo que usa porta 5000:
netstat -ano | findstr :5000

# Matar processo (substitua PID):
taskkill /PID 1234 /F

# Ou mudar porta em backend/app.py linha 290:
socketio.run(app, host='0.0.0.0', port=5001)  # Mudar 5000 → 5001
```

### 2. Android em rede diferente do PC?

Se o Android estiver em rede diferente do PC (ex: celular 4G, PC WiFi):

```
Usar IP público + ngrok:

# Instalar ngrok: https://ngrok.com
ngrok http 5000

# Será gerada URL tipo: https://1234-56-78-90-12.ngrok.io
# Usar esta URL no Android App
```

### 3. SMS armazenados apenas 5 horas

Isso é proposital! SMS são deletados automaticamente após 5 horas para:
- Economizar espaço
- Manter privacidade
- Reduzir DB size

Se quiser armazenar mais tempo, mudar em `backend/app.py`:

```python
# Linha ~170 (função cleanup_old_sms):
limite = datetime.now() - timedelta(hours=5)  # Mudar 5 para 24 (1 dia)
```

## ✅ Próximas Etapas

Depois que tudo estiver funcionando:

1. ✅ Testar envio/recebimento de SMS
2. ✅ Verificar se PC App atualiza em tempo real
3. ⏭️ Adicionar GUI bonita no PC App (PyQt6)
4. ⏭️ Fazer APK oficial do Android
5. ⏭️ Deploy no Railway (se quiser nuvem)

## 📞 Suporte

Qualquer erro? Verificar logs:

```bash
# Backend
# Errors aparecem no terminal onde rodou app.py

# PC App
# Errors aparecem no terminal onde rodou pc_app.py

# Android
# Abra Android Studio → Logcat (embaixo)
```

---

**Tudo pronto?** Vamos começar! 🚀
