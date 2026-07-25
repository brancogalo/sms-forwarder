package com.smsforwarder

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.telephony.SmsMessage
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class SmsReceiver : BroadcastReceiver() {
    
    companion object {
        private const val TAG = "SmsReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent == null || context == null) return
        
        try {
            val bundle = intent.extras ?: return
            val pdus = bundle.get("pdus") as? Array<*> ?: return
            
            Log.d(TAG, "SMS recebido! Total: ${pdus.size}")
            
            for (pdu in pdus) {
                try {
                    val sms = SmsMessage.createFromPdu(pdu as ByteArray)
                    val numero = sms.originatingAddress ?: "Desconhecido"
                    val mensagem = sms.messageBody ?: ""
                    val timestamp = LocalDateTime.now().format(
                        DateTimeFormatter.ISO_DATE_TIME
                    )
                    
                    Log.d(TAG, "De: $numero - Msg: $mensagem")
                    
                    // Enviar para Backend em thread separada
                    GlobalScope.launch(Dispatchers.IO) {
                        enviarParaBackend(context, numero, mensagem, timestamp)
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Erro ao processar SMS", e)
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Erro no SmsReceiver", e)
        }
    }

    private suspend fun enviarParaBackend(
        context: Context,
        numero: String,
        mensagem: String,
        timestamp: String
    ) {
        try {
            val apiClient = ApiClient(context)
            val response = apiClient.enviarSms(numero, mensagem, timestamp)
            
            if (response.isSuccessful) {
                Log.d(TAG, "✅ SMS enviado ao Backend: $numero")
            } else {
                Log.w(TAG, "⚠️ Erro ao enviar: ${response.code()}")
            }
        } catch (e: Exception) {
            Log.e(TAG, "❌ Erro de conexão ao Backend", e)
        }
    }
}
