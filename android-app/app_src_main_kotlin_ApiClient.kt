package com.smsforwarder

import android.content.Context
import android.util.Log
import org.json.JSONObject
import java.net.URL
import java.net.HttpURLConnection
import java.nio.charset.StandardCharsets

class ApiClient(private val context: Context) {
    
    companion object {
        private const val TAG = "ApiClient"
        
        // ⚠️ IMPORTANTE: Mudar para seu IP local
        // Descobrir IP: Abra CMD e digite: ipconfig
        // Procure "IPv4 Address" (exemplo: 192.168.1.100)
        // 
        // OPÇÕES:
        // private const val BACKEND_URL = "http://192.168.1.100:5000"  // ← SEU IP LOCAL
        // private const val BACKEND_URL = "http://seu-dominio.com"     // ← OU SEU DOMÍNIO
        
        // POR ENQUANTO, usar localhost (funciona em emulador)
        private const val BACKEND_URL = "http://10.0.2.2:5000"  // Emulador Android
        // private const val BACKEND_URL = "http://192.168.1.100:5000"  // Mudar para seu IP!
    }

    suspend fun enviarSms(numero: String, mensagem: String, timestamp: String): HttpResponse {
        return try {
            val url = URL("$BACKEND_URL/api/sms")
            val connection = url.openConnection() as HttpURLConnection
            
            // Configurar requisição
            connection.requestMethod = "POST"
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
            connection.setRequestProperty("Accept", "application/json")
            connection.doOutput = true
            connection.connectTimeout = 5000
            connection.readTimeout = 5000
            
            // Criar JSON
            val jsonBody = JSONObject().apply {
                put("numero", numero)
                put("mensagem", mensagem)
                put("timestamp", timestamp)
                put("device_id", android.os.Build.ID)
            }
            
            // Enviar dados
            val outputStream = connection.outputStream
            outputStream.write(jsonBody.toString().toByteArray(StandardCharsets.UTF_8))
            outputStream.flush()
            outputStream.close()
            
            // Obter resposta
            val responseCode = connection.responseCode
            val responseMessage = connection.inputStream?.bufferedReader()?.use { it.readText() } ?: ""
            
            connection.disconnect()
            
            Log.d(TAG, "Response Code: $responseCode")
            Log.d(TAG, "Response: $responseMessage")
            
            HttpResponse(responseCode in 200..299, responseCode, responseMessage)
        } catch (e: Exception) {
            Log.e(TAG, "Erro ao enviar SMS", e)
            HttpResponse(false, -1, e.message ?: "Erro desconhecido")
        }
    }
}

data class HttpResponse(
    val isSuccessful: Boolean,
    val code: Int,
    val message: String
)
