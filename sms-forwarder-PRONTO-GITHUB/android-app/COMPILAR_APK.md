# 🔨 Como Compilar o APK Android

Instruções passo a passo para gerar o arquivo APK pronto para instalar.

---

## 📋 Pré-requisitos

1. **Android Studio** instalado
   - [Baixar](https://developer.android.com/studio)
   - Recomendado: Versão 2023.1+

2. **JDK 11+**
   - Geralmente vem com Android Studio

3. **SDK Android**
   - Android 14 (API 34)
   - Instalado via Android Studio

---

## 🚀 Passo a Passo

### Passo 1: Abrir Projeto no Android Studio

```
1. Abra Android Studio
2. Clique em "File" → "Open"
3. Selecione a pasta "android-app"
4. Aguarde indexar (pode levar 2-3 minutos)
```

Você vai ver a pasta com estrutura:
```
android-app/
├── app/
│   ├── src/
│   ├── build.gradle
│   └── ...
├── build.gradle
└── settings.gradle
```

---

### Passo 2: IMPORTANTE - Configurar IP do Backend

#### Opção A: Emulador Android (Teste local)

Se está testando com emulador, deixe como está:
```kotlin
// ApiClient.kt - Linha ~20
private const val BACKEND_URL = "http://10.0.2.2:5000"
// 10.0.2.2 é localhost do emulador
```

#### Opção B: Android Físico (Seu telefone)

**Você PRECISA mudar para seu IP local:**

```bash
# Abrir CMD/PowerShell e descobrir IP:
ipconfig

# Procurar por "IPv4 Address:" (algo como: 192.168.1.100)
```

Depois, abrir arquivo:
```
android-app/app/src/main/kotlin/ApiClient.kt
```

Mudar linha ~20 de:
```kotlin
private const val BACKEND_URL = "http://10.0.2.2:5000"
```

Para:
```kotlin
private const val BACKEND_URL = "http://192.168.1.100:5000"
// ⚠️ Substituir 192.168.1.100 pelo SEU IP!
```

**Como descobrir seu IP:**
```bash
# Windows - CMD ou PowerShell
ipconfig
# Procurar: IPv4 Address... : 192.168.x.x

# Linux/Mac - Terminal
ifconfig | grep "inet "
```

---

### Passo 3: Sincronizar Gradle

```
1. No Android Studio, pressione: Ctrl + Shift + O
   (Ou: File → Sync Now)

2. Aguarde sincronizar (pode levar 1-2 minutos)

3. Se houver erros, verificar:
   - Internet conectada
   - JDK correto
   - SDK atualizado
```

---

### Passo 4: Build do APK

#### Opção A: APK Debug (Rápido - para teste)

```
1. Menu: Build → Build Bundle(s) / APK(s) → Build APK(s)

2. Aguarde compilar (2-5 minutos)

3. Se sucesso, notificação aparece:
   "APK(s) generated successfully"

4. Clique em "locate" para abrir a pasta
```

**Arquivo gerado:**
```
app/build/outputs/apk/debug/app-debug.apk
```

#### Opção B: APK Release (Oficial - para distribuição)

```
1. Menu: Build → Generate Signed Bundle / APK

2. Selecionar "APK"

3. Criar ou selecionar keystore:
   - Se primeira vez:
     * Clique "Create new"
     * Preencher informações
     * Salvar em local seguro (não deletar!)
   - Se já tem:
     * Selecionar arquivo .jks existente

4. Preencher senha

5. Selecionar "Release"

6. Próximo → Próximo → Finish

7. Aguarde compilar (2-5 minutos)
```

**Arquivo gerado:**
```
app/build/outputs/bundle/release/app-release.apk
```

---

## 📱 Instalar no Android

### Opção 1: Emulador (Teste no PC)

```
1. Abrir emulador (AVD Manager no Android Studio)
2. Deixar rodando
3. Conectar APK:
   - Menu: Run → Run 'app'
   - Ou arrastar APK para janela do emulador
```

### Opção 2: Telefone Físico

#### Habilitar Debug Mode

```
1. Ir para: Settings → About Phone
2. Procurar "Build Number"
3. Clicar 7x em "Build Number"
4. Mensagem: "You are a developer!"
5. Voltar para Settings → Developer Options
6. Ligar "USB Debugging"
7. Conectar telefone ao PC via USB
```

#### Instalar APK

**Método 1: Arrastar APK**
```
1. Conectar telefone ao PC (USB Debugging ativo)
2. Android Studio detecta automaticamente
3. Menu: Run → Run 'app'
4. Selecionar seu telefone
5. APK instala automaticamente
```

**Método 2: Transferir Arquivo**
```
1. Copiar app-debug.apk para pasta
2. Transferir para telefone via:
   - Cabo USB + Windows Explorer
   - Email
   - WhatsApp
   - Google Drive
   
3. No telefone:
   - Abrir Gerenciador de Arquivos
   - Localizar APK
   - Clicar para instalar
   - Conceder permissões
```

**Método 3: Linha de Comando**
```bash
# Conectar telefone com USB Debugging
# Abrir CMD na pasta onde está app-debug.apk

adb install app-debug.apk

# Se sucesso: "Success"
# Se erro: seguir instruções na tela
```

---

## ✅ Após Instalação

### Verificar Permissões

```
1. Abrir app SMS Forwarder
2. Conceder permissões:
   - ✅ Ler SMS
   - ✅ Conectar à internet
   - ✅ Detectar telefone (opcional)
3. Voltar para tela anterior
4. Pronto! App está monitorando SMS
```

### Testar

```
1. Enviar SMS para seu número
2. Backend deve receber
3. PC App mostra o SMS
4. ✅ Tudo funcionando!
```

---

## 🐛 Troubleshooting

### Erro: "Could not find com.android.application"

**Solução:**
```
1. File → Sync Now
2. Se persistir:
   - Delete .gradle folder
   - File → Sync Now (novamente)
```

### Erro: "Failed to resolve: androidx.appcompat:appcompat"

**Solução:**
```
1. File → Project Structure
2. SDK Location
3. Verificar se SDK está instalado
4. Se não: Tools → SDK Manager → Install
```

### APK não instala no telefone

**Solução:**
```
1. Verificar USB Debugging está ligado
2. Tentar: adb install app-debug.apk
3. Se der erro, adb uninstall com.smsforwarder
4. Tentar instalar novamente
```

### App instalado mas não recebe SMS

**Problema:** Backend URL errada ou não rodando

**Solução:**
```
1. Verificar Backend rodando: python app.py
2. Verificar IP correto em ApiClient.kt
3. Recompilar APK com IP correto
4. Desinstalar versão antiga: adb uninstall com.smsforwarder
5. Instalar nova versão
```

### Permissões não são solicitadas

**Solução:**
```
1. Android 6+: Ir para Settings → Apps → SMS Forwarder
2. Permissions → Ligar tudo
3. Voltar ao app
4. Tentar enviar SMS
```

---

## 📊 Tamanho Esperado

- **APK Debug:** ~5-10 MB
- **APK Release:** ~3-5 MB (comprimido)

---

## 🎯 Resumo Rápido

1. **Abrir:** Projeto em Android Studio
2. **Mudar:** IP em ApiClient.kt (se telefone físico)
3. **Sincronizar:** Gradle (Ctrl+Shift+O)
4. **Build:** Build → Build APK
5. **Instalar:** Conectar telefone ou emulador
6. **Testar:** Enviar SMS e verificar PC App

---

## 📱 Arquivo Final

Após compilação bem-sucedida:

```
📦 Arquivo APK Pronto:
   
   app/build/outputs/apk/debug/app-debug.apk
   ↓
   Copiar para telefone
   ↓
   Clicar para instalar
   ↓
   ✅ App em funcionamento!
```

---

## ⏭️ Próximo Passo

Depois de instalar no telefone:

1. ✅ Backend rodando
2. ✅ PC App rodando
3. ✅ APK instalado no Android
4. 📱 Envie um SMS real
5. 💻 PC App mostra em tempo real!

---

**Sucesso na compilação!** 🚀

Qualquer dúvida, verificar mensagens de erro no logcat do Android Studio.
