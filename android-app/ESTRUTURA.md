# 📁 Estrutura do Android App

Como o app será organizado após criação no Android Studio.

## 📂 Pastas e Arquivos Principais

```
android-app/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── kotlin/com/smsforwarder/
│   │       │   ├── MainActivity.kt                 # Tela principal
│   │       │   ├── receivers/
│   │       │   │   └── SmsReceiver.kt              # Captura SMS
│   │       │   ├── services/
│   │       │   │   └── SmsForwardService.kt        # Envia SMS pro servidor
│   │       │   ├── api/
│   │       │   │   └── ApiClient.kt                # Cliente HTTP/Retrofit
│   │       │   ├── database/
│   │       │   │   ├── SmsDatabase.kt              # Room Database
│   │       │   │   ├── SmsEntity.kt                # Entidade SMS
│   │       │   │   └── SmsDao.kt                   # Data Access Object
│   │       │   ├── models/
│   │       │   │   └── SmsModel.kt                 # Modelo de dados
│   │       │   ├── workers/
│   │       │   │   └── SmsWorker.kt                # WorkManager task
│   │       │   └── utils/
│   │       │       ├── LogUtil.kt                  # Logs
│   │       │       └── Constants.kt                # Constantes
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   │   └── activity_main.xml           # Layout da tela
│   │       │   ├── values/
│   │       │   │   ├── strings.xml                 # Textos
│   │       │   │   ├── colors.xml                  # Cores
│   │       │   │   └── dimens.xml                  # Dimensões
│   │       │   └── drawable/                       # Ícones
│   │       └── AndroidManifest.xml                 # Permissões + receivers
│   ├── build.gradle                                # Dependências
│   └── proguard-rules.pro                          # Obfuscação
├── build.gradle                                    # Gradle raiz
├── settings.gradle                                 # Configurações
└── local.properties                                # Config local (gitignore)
```

## 🔑 Arquivos Essenciais

### 1. **AndroidManifest.xml**
Define permissões e componentes do app.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.smsforwarder">

    <!-- PERMISSÕES -->
    <uses-permission android:name="android.permission.RECEIVE_SMS" />
    <uses-permission android:name="android.permission.READ_SMS" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application>
        <!-- Activity Principal -->
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- SMS Receiver -->
        <receiver
            android:name=".receivers.SmsReceiver"
            android:exported="true"
            android:permission="android.permission.RECEIVE_SMS">
            <intent-filter>
                <action android:name="android.provider.Telephony.SMS_RECEIVED" />
            </intent-filter>
        </receiver>

        <!-- Boot Receiver -->
        <receiver
            android:name=".receivers.BootReceiver"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>

        <!-- Serviço -->
        <service
            android:name=".services.SmsForwardService"
            android:exported="false" />
    </application>
</manifest>
```

### 2. **SmsReceiver.kt**
Captura SMS assim que chegam.

```kotlin
package com.smsforwarder.receivers

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.SmsMessage
import com.smsforwarder.services.SmsForwardService
import com.smsforwarder.models.SmsModel
import java.time.LocalDateTime

class SmsReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // Extrair SMS da intent
        val bundle = intent?.extras ?: return
        val pdus = bundle.get("pdus") as? Array<*> ?: return

        for (pdu in pdus) {
            val sms = SmsMessage.createFromPdu(pdu as ByteArray)
            val numero = sms.originatingAddress ?: ""
            val mensagem = sms.messageBody
            val timestamp = LocalDateTime.now().toString()

            // Criar modelo SMS
            val smsModel = SmsModel(
                numero = numero,
                mensagem = mensagem,
                timestamp = timestamp
            )

            // Enviar pro backend
            val service = Intent(context, SmsForwardService::class.java)
            service.putExtra("sms", smsModel)
            context?.startService(service)
        }
    }
}
```

### 3. **ApiClient.kt**
Cliente HTTP para enviar dados ao backend.

```kotlin
package com.smsforwarder.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.POST
import retrofit2.http.Body
import com.smsforwarder.models.SmsModel

// ⚠️ MUDAR AQUI PARA SEU IP/DOMÍNIO
private const val BASE_URL = "http://192.168.1.100:5000/"

interface SmsApiService {
    @POST("api/sms")
    suspend fun enviarSms(@Body sms: SmsModel): SmsResponse
}

data class SmsResponse(
    val sucesso: Boolean,
    val id: Int?,
    val timestamp: String
)

object ApiClient {
    val apiService: SmsApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(SmsApiService::class.java)
    }
}
```

### 4. **SmsForwardService.kt**
Serviço que envia SMS para o backend.

```kotlin
package com.smsforwarder.services

import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import com.smsforwarder.models.SmsModel
import com.smsforwarder.workers.SmsWorker
import com.google.gson.Gson

class SmsForwardService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val sms = intent?.getSerializableExtra("sms") as? SmsModel ?: return START_STICKY

        // Usar WorkManager para enviar em background
        val workRequest = OneTimeWorkRequestBuilder<SmsWorker>()
            .setInputData(
                androidx.work.workDataOf(
                    "sms" to Gson().toJson(sms)
                )
            )
            .build()

        WorkManager.getInstance(this).enqueue(workRequest)

        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
```

### 5. **build.gradle**
Dependências do projeto.

```gradle
plugins {
    id 'com.android.application'
    id 'kotlin-android'
    id 'kotlin-kapt'
}

android {
    compileSdk 34
    
    defaultConfig {
        applicationId "com.smsforwarder"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
}

dependencies {
    // Kotlin
    implementation 'androidx.core:core-ktx:1.10.1'
    
    // Android
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
    
    // Network
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    
    // Database
    implementation 'androidx.room:room-runtime:2.5.2'
    kapt 'androidx.room:room-compiler:2.5.2'
    
    // Background
    implementation 'androidx.work:work-runtime-ktx:2.8.1'
    
    // Gson
    implementation 'com.google.code.gson:gson:2.10.1'
}
```

## 🔄 Fluxo de Funcionamento

```
┌──────────────────────────────────────────────────────┐
│ SMS chega no telefone                                │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ SmsReceiver captura SMS                              │
│ (BroadcastReceiver)                                  │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ Cria SmsModel com dados                              │
│ - Número                                             │
│ - Mensagem                                           │
│ - Timestamp                                          │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ Inicializa SmsForwardService                         │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ SmsWorker envia HTTP POST pro Backend                │
│ ApiClient.apiService.enviarSms(sms)                  │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ Backend recebe em POST /api/sms                      │
│ Armazena no SQLite                                   │
│ Emite WebSocket "novo_sms"                          │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ PC App recebe WebSocket                              │
│ Mostra SMS em tempo real com 🟢 status               │
└──────────────────────────────────────────────────────┘
```

## 📦 Criar APK

Depois que Android Studio terminar setup:

```
1. Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Esperar compilação
3. Arquivo fica em: app/build/outputs/apk/release/app-release.apk
4. Transferir para Android
5. Instalar e testar!
```

## ⚠️ Pontos Importantes

### 1. Mudar URL do Backend!
Arquivo: `ApiClient.kt` linha 7
```kotlin
// Mudar isso:
private const val BASE_URL = "http://192.168.1.100:5000/"

// Para seu IP/domínio:
// - Localhost: NÃO FUNCIONA em Android físico
// - IP local: http://192.168.1.100:5000  ← MELHOR
// - Domínio: https://seu-site.com
```

### 2. Permissões
- ✅ RECEIVE_SMS - Obrigatória
- ✅ READ_SMS - Obrigatória
- ✅ INTERNET - Obrigatória
- ✅ RECEIVE_BOOT_COMPLETED - Para iniciar com telefone
- ✅ ACCESS_NETWORK_STATE - Para verificar internet

### 3. Target SDK
- Usar API 34+ para funcionar em Android 14+
- minSdk 24 (Android 7) para compatibilidade

### 4. Testes
```bash
# Enviar SMS de teste pelo emulador
adb shell am start -n com.android.mms/.ui.ConversationList

# Ou via SMS real
```

---

Arquivo criado como guia. Valores reais virão do Android Studio.
