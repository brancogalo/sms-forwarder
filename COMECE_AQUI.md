# 🚀 COMECE AQUI - SMS Forwarder

Bem-vindo! Este é o início do seu projeto SMS Forwarder.

## 📋 O Que Você Ganhou

Criamos para você:

✅ **Backend Flask** (Python)
   - Recebe SMS do Android
   - Armazena por 5 horas
   - WebSocket em tempo real

✅ **PC App** (Windows CMD)
   - Mostra SMS em tempo real
   - Status dos números 🟢 (ativo) / 🔴 (inativo)
   - Interface simples

✅ **Android App** (Kotlin)
   - Captura SMS automaticamente
   - Envia para Backend
   - Funciona em background

✅ **Documentação Completa**
   - Setup passo a passo
   - Teste rápido
   - Estrutura do projeto

---

## ⚡ Começar em 5 Minutos

### Passo 1: Instalar Python (se não tiver)

[Baixar Python 3.9+](https://www.python.org/downloads/)

Depois verificar:
```bash
python --version
```

### Passo 2: Clonar Este Projeto

```bash
# Se estiver em GitHub:
git clone seu-repo-aqui
cd sms-forwarder

# Ou se estiver local:
# Copie os arquivos para uma pasta
```

### Passo 3: Rodar Backend

```bash
# Abrir Terminal 1
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar
python app.py
```

**Resultado esperado:**
```
🚀 Servidor rodando em http://localhost:5000
```

✅ **Backend pronto!**

### Passo 4: Rodar PC App

```bash
# Abrir Terminal 2 (novo)
cd pc-app

# Windows
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar
python pc_app.py
```

**Será pedido:**
```
URL do Backend [localhost:5000]: 
# Pressione Enter
```

**Resultado esperado:**
```
✅ Conectado ao Backend!
```

✅ **PC App pronto!**

### Passo 5: Testar

```bash
# Abrir Terminal 3 (novo)
# Enviar SMS de teste:
curl -X POST http://localhost:5000/api/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"+5585987654321\",\"mensagem\":\"Teste!\",\"timestamp\":\"2026-07-25T20:00:00Z\"}"
```

No **Terminal 2 (PC App)** deve aparecer:
```
📬 NOVO SMS!
De: +5585987654321
Mensagem: Teste!
```

✅ **Tudo funcionando!**

---

## 📚 Arquivos Importantes

```
📁 sms-app-project/
├── 📄 README.md              ← Visão geral do projeto
├── 📄 SETUP.md              ← Setup completo
├── 📄 TESTE_RAPIDO.md       ← Validar tudo
├── 📄 COMECE_AQUI.md        ← Você está aqui
│
├── 📁 backend/
│   ├── app.py               ← Servidor Flask (principal)
│   ├── database.py          ← Banco SQLite
│   └── requirements.txt
│
├── 📁 pc-app/
│   ├── pc_app.py            ← Program Windows (main)
│   └── requirements.txt
│
└── 📁 android-app/
    ├── README.md
    └── ESTRUTURA.md         ← Como criar o APK
```

## 🎯 Próximos Passos

### 1️⃣ Backend + PC App (HOJE)

- [x] Instalar Python
- [x] Rodar Backend
- [x] Rodar PC App
- [x] Testar com SMS fictício
- → **Ir para TESTE_RAPIDO.md**

### 2️⃣ Android (PRÓXIMO)

- [ ] Instalar Android Studio
- [ ] Criar projeto no Android Studio
- [ ] Copiar arquivos do android-app/
- [ ] Mudar URL para seu IP
- [ ] Compilar APK
- [ ] Testar com SMS real

### 3️⃣ Cloud (DEPOIS - OPCIONAL)

- [ ] Criar conta Railway.com
- [ ] Deploy do Backend
- [ ] Atualizar URL no Android
- [ ] Usar domínio ao invés de IP

---

## ❓ Dúvidas Comuns

### P: Preciso de Railway agora?
**R:** Não! Deixa para depois. Comece local primeiro. Se funcionar localmente, depois deploy na cloud é fácil.

### P: E se a porta 5000 estiver em uso?
**R:** Ver em **SETUP.md → Troubleshooting**

### P: Quando ativa o Android?
**R:** Depois que Backend + PC App estiverem funcionando. Seguir **ESTRUTURA.md** para Android.

### P: SMS fica armazenado onde?
**R:** No arquivo `backend/sms_database.db` (SQLite local). Deletado automaticamente após 5 horas.

### P: Posso mudar pra 24 horas?
**R:** Sim! Ver em **SETUP.md** → seção SMS armazenados apenas 5 horas.

### P: Posso usar em um servidor remoto?
**R:** Sim! Deploy no Railway.com depois. Por agora, mantenha local.

---

## 🔧 Instalação Rápida (Resumido)

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2 - PC App
cd pc-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python pc_app.py

# Terminal 3 - Testar
curl -X POST http://localhost:5000/api/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"+5585987654321\",\"mensagem\":\"Teste\",\"timestamp\":\"2026-07-25T20:00:00Z\"}"
```

---

## ✅ Checklist

- [ ] Python 3.9+ instalado
- [ ] Terminal 1: Backend rodando
- [ ] Terminal 2: PC App conectado
- [ ] Terminal 3: SMS de teste enviado
- [ ] PC App mostra novo SMS
- [ ] Lido COMECE_AQUI.md
- [ ] Pronto para Android App

---

## 📞 Suporte

Qualquer erro?

1. **Verificar logs nos terminais** - aparecem erros lá
2. **Ler SETUP.md** - tem troubleshooting
3. **Ler TESTE_RAPIDO.md** - validar cada componente

---

## 🎉 Próxima Coisa?

Depois que tudo estiver funcionando:

👉 **Ir para: android-app/ESTRUTURA.md**

Lá você vai criar o APK para seu Android.

---

**Tempo estimado para estar funcionando:** ~15 minutos

**Sucesso!** 🚀
