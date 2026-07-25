package com.smsforwarder

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

/**
 * BootReceiver - Inicia o app quando o telefone liga
 */
class BootReceiver : BroadcastReceiver() {
    
    companion object {
        private const val TAG = "BootReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent?.action == Intent.ACTION_BOOT_COMPLETED) {
            Log.d(TAG, "📱 Telefone ligou - App iniciado")
            
            // Aqui você pode inicializar serviços se necessário
            // Por enquanto, o SmsReceiver já está ativo
        }
    }
}
