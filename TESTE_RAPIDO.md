# ⚡ Teste Rápido - SMS Forwarder

Validar que tudo está funcionando corretamente.

## 📋 Checklist

### ✅ 1. Backend Rodando

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Resultado esperado:**
```
╔════════════════════════════════════════╗
║  SMS FORWARDER - BACKEND               ║
║  Backend iniciado!                     ║
╚════════════════════════════════════════╝

🚀 Servidor rodando em http://localhost:5000
```

✅ **Backend OK**

---

### ✅ 2. Verificar Health Check

```bash
# Terminal diferente - Testar API
curl http://localhost:5000/health
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "timestamp": "2026-07-25T21:30:00.000000",
  "conectados": 0
}
```

✅ **API OK**

---

### ✅ 3. PC App Conectando

```bash
# Terminal 2 - PC App
cd pc-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python pc_app.py
```

**Será pedido:**
```
URL do Backend [localhost:5000]: 
# Pressione Enter
```

**Resultado esperado:**
```
╔═════════════════════════════════════════╗
║  SMS FORWARDER - MONITOR PC             ║
║  Windows CMD - Tempo Real               ║
╚═════════════════════════════════════════╝

[14:30:00] 🔌 Conectando a http://localhost:5000...
[14:30:01] ✅ Conectado ao Backend!
[14:30:01] 📊 0 números ativos

════════════════════════════════════════════
  SMS FORWARDER - MONITOR
════════════════════════════════════════════

Status: ✓ ONLINE
...
```

✅ **PC App OK**

---

### ✅ 4. Simular SMS via API

```bash
# Terminal 3 - Simular SMS
curl -X POST http://localhost:5000/api/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"+5585987654321\",\"mensagem\":\"Teste SMS\",\"timestamp\":\"2026-07-25T21:30:00Z\"}"
```

**Resultado esperado no Terminal Backend:**
```
[SMS] De +5585987654321: Teste SMS...
```

**Resultado esperado no Terminal PC App:**
```
📬 NOVO SMS!
==================================================
De: +5585987654321
Mensagem: Teste SMS
Hora: 2026-07-25T21:30:00Z
==================================================

🟢 +5585987654321     (1 SMS)

[21:30] +5585987654321
       "Teste SMS"
```

✅ **SMS OK**

---

### ✅ 5. Listar Números Ativos

```bash
# Testar endpoint de números
curl http://localhost:5000/api/numeros
```

**Resultado esperado:**
```json
{
  "numeros": [
    {
      "numero": "+5585987654321",
      "quantidade": 1,
      "ultimo_sms": "2026-07-25T21:30:00",
      "status": "ativo"
    }
  ],
  "total": 1
}
```

✅ **Números OK**

---

### ✅ 6. Listar SMS

```bash
# Testar endpoint de SMS
curl http://localhost:5000/api/sms
```

**Resultado esperado:**
```json
{
  "sms": [
    {
      "id": 1,
      "numero": "+5585987654321",
      "mensagem": "Teste SMS",
      "timestamp": "2026-07-25T21:30:00Z",
      "device_id": "desconhecido"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

✅ **SMS Listing OK**

---

### ✅ 7. Múltiplos SMS em Tempo Real

```bash
# Enviar vários SMS de teste
curl -X POST http://localhost:5000/api/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"+5585987654321\",\"mensagem\":\"SMS 2\",\"timestamp\":\"2026-07-25T21:31:00Z\"}"

# Esperar um pouco
timeout /t 2

curl -X POST http://localhost:5000/api/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"+5585999999999\",\"mensagem\":\"SMS de outro número\",\"timestamp\":\"2026-07-25T21:32:00Z\"}"
```

**Resultado PC App:**
```
🟢 +5585999999999     (1 SMS)
🟢 +5585987654321     (2 SMS)

[21:32] +5585999999999
       "SMS de outro número"

[21:31] +5585987654321
       "SMS 2"

[21:30] +5585987654321
       "Teste SMS"
```

✅ **Múltiplos SMS OK**

---

## 🎯 Resumo de Testes

| Teste | Comando | Status |
|-------|---------|--------|
| Backend rodando | `python app.py` | ✅ |
| Health Check | `curl /health` | ✅ |
| PC App conectado | `python pc_app.py` | ✅ |
| Enviar SMS | `curl POST /api/sms` | ✅ |
| Números ativos | `curl /api/numeros` | ✅ |
| Listar SMS | `curl /api/sms` | ✅ |
| Tempo real | WebSocket | ✅ |

---

## 🐛 Troubleshooting Rápido

### Backend não inicia

```bash
# Erro: "Address already in use"
# Solução: Porta 5000 em uso

netstat -ano | findstr :5000
# Anote o PID
taskkill /PID 1234 /F
```

### PC App não conecta

```bash
# Erro: "Connection refused"
# Solução: Backend não está rodando

# Terminal Backend deve mostrar:
# "🚀 Servidor rodando em http://localhost:5000"
```

### Curl não reconhecido

```bash
# Windows pode não ter curl
# Usar em PowerShell:
Invoke-WebRequest http://localhost:5000/health

# Ou instalar:
choco install curl
```

### Caracteres especiais na mensagem

```bash
# Se usar caracteres acentuados, escape:
-d "{\"numero\":\"+55\",\"mensagem\":\"Olá mundo\"}"
```

---

## 📱 Próximo Passo: Android

Depois que Backend + PC App funcionarem:

1. ✅ Backend rodando
2. ✅ PC App conectado e recebendo SMS
3. ⏭️ Android App compilado
4. ⏭️ Testar envio de SMS real

---

## 🎉 Tudo Ok?

Se todos os testes passaram:

```
✅ Backend funciona
✅ PC App conecta
✅ SMS são recebidos em tempo real
✅ Números ativos são mostrados
✅ Sistema está pronto!
```

Próximo passo: **Compilar Android App** e enviar SMS reais.

---

**Tempo estimado de teste:** ~10 minutos

Qualquer problema? Verificar os logs nos terminais.
