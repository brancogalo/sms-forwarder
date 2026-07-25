# SMS Forwarding System 📱➡️💻

Um sistema completo para capturar SMS do seu Android e visualizar no PC em tempo real.

## 🎯 Componentes

```
sms-app-project/
├── android-app/          # App Android (Kotlin)
├── backend/              # Servidor Backend (Python/Flask)
├── pc-app/               # Interface Desktop (Python/PyQt ou Electron)
├── docs/                 # Documentação
└── README.md
```

## 🚀 Arquitetura

```
📱 Android (Visível)
   ↓ (captura SMS + envia)
   ↓
🖥️ Backend Python (Local/Cloud)
   ↓ (armazena 5 horas)
   ↓
💻 PC Windows (CMD)
   ↓ (mostra status: 🟢 ou 🔴)
   ↓
✅ Tempo Real!
```

## 🎨 PC App - Visualização

```
════════════════════════════════════════════
  SMS FORWARDER - MONITOR
════════════════════════════════════════════

NÚMEROS ATIVOS:
  🟢 +5585987654321     (4 SMS)
  🟢 +5585999999999     (2 SMS)
  🔴 +5581234567890     (1 SMS)

─────────────────────────────────────────────

[14:32] +5585987654321: "Oi, tudo bem?"
[14:28] +5585999999999: "Olá, como vai?"
[14:15] +5581234567890: "Mensagem importante"

─────────────────────────────────────────────
✓ Backend conectado | Armazena 5h
```

## 📋 Status

- [x] Setup inicial
- [x] Estrutura de pastas
- [ ] App Android (Kotlin)
- [ ] Backend (Python Flask)
- [ ] PC App (Python PyQt6 Windows)
- [ ] Testes completos

## 🔧 O Que Você Precisa Instalar

1. **Android Studio** (para compilar o APK)
2. **Python 3.9+** (para Backend e PC App)
3. **Git** (para clonar o projeto)

---

**Criado:** 2026  
**Linguagens:** Kotlin (Android) + Python (Backend) + Python/Electron (Desktop)
