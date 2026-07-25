# 📱 Android App - SMS Forwarder

App Android que captura SMS e envia para o Backend em tempo real.

## ⚙️ Especificações

- **Visibilidade:** Visível na listagem de apps (normal)
- **Permissões:** RECEIVE_SMS, READ_SMS, INTERNET, BOOT_COMPLETED
- **Funcionamento:** Background + ativa com o telefone
- **Envio:** Assim que SMS chegar (tempo real)

## 🔐 Permissões Necessárias

- `RECEIVE_SMS` - Receber SMS
- `READ_SMS` - Ler SMS  
- `INTERNET` - Enviar dados para Backend
- `BOOT_COMPLETED` - Iniciar com o telefone
- `RUN_IN_BACKGROUND` - Executar em background

## 🎨 Features

- ✅ Recebe SMS automaticamente
- ✅ Funciona em background
- ✅ Sem ícone na tela inicial
- ✅ Envia para servidor seguro (HTTPS)
- ✅ Salva SMS localmente
- ✅ Inicia com o telefone

## 🛠️ Stack

- **Linguagem:** Kotlin
- **Minimo SDK:** API 24 (Android 7)
- **Target SDK:** API 34 (Android 14)
- **Build System:** Gradle

## 📦 Dependências Principais

```gradle
- Retrofit (HTTP)
- OkHttp (HTTPS)
- Room Database (SQLite local)
- WorkManager (Background tasks)
```

## 🚀 Instalação

```bash
1. Abrir em Android Studio
2. Sync Gradle
3. Build APK
4. Instalar no telefone
5. Conceder permissões
```

## 🔄 Fluxo

```
Telefone recebe SMS
    ↓
BroadcastReceiver captura
    ↓
Salva localmente (Room)
    ↓
Envia pro servidor (WorkManager)
    ↓
Servidor armazena
    ↓
PC visualiza em tempo real
```

## 📝 Estrutura de Arquivo

```
android-app/
├── app/
│   ├── src/main/
│   │   ├── java/com/smsforwarder/
│   │   │   ├── receivers/
│   │   │   │   └── SmsReceiver.kt
│   │   │   ├── services/
│   │   │   │   └── SmsService.kt
│   │   │   ├── db/
│   │   │   │   └── SmsDatabase.kt
│   │   │   └── api/
│   │   │       └── ApiClient.kt
│   │   ├── AndroidManifest.xml
│   │   └── res/
│   └── build.gradle
├── build.gradle
└── settings.gradle
```
