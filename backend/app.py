"""
Backend SMS Forwarder
Recebe SMS do Android e armazena por 5 horas
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime, timedelta
import os
import json
import threading
from database import Database

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-dev')
CORS(app)

# WebSocket
socketio = SocketIO(app, cors_allowed_origins="*")

# Database
db = Database()

# Store de clientes conectados
clients = {}


# ============ ROTAS HTTP ============

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'conectados': len(clients)
    }), 200


@app.route('/api/sms', methods=['POST'])
def receive_sms():
    """
    Receber SMS do Android
    
    Body:
    {
        "numero": "+5585987654321",
        "mensagem": "Conteúdo SMS",
        "timestamp": "2026-07-25T21:00:00Z",
        "device_id": "android123"  # ID do dispositivo
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos
        if not all(k in data for k in ['numero', 'mensagem']):
            return jsonify({'erro': 'Campos numero e mensagem obrigatórios'}), 400
        
        # Salvar no banco
        sms = {
            'numero': data['numero'],
            'mensagem': data['mensagem'],
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'device_id': data.get('device_id', 'desconhecido')
        }
        
        sms_id = db.add_sms(sms)
        
        # Atualizar número ativo
        db.update_numero_ativo(data['numero'])
        
        # Emitir via WebSocket para todos os clientes
        socketio.emit('novo_sms', {
            'id': sms_id,
            'numero': sms['numero'],
            'mensagem': sms['mensagem'],
            'timestamp': sms['timestamp'],
            'device_id': sms['device_id']
        }, broadcast=True)
        
        print(f"[SMS] De {sms['numero']}: {sms['mensagem'][:30]}...")
        
        return jsonify({
            'sucesso': True,
            'id': sms_id,
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        print(f"[ERRO] Receber SMS: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/api/sms', methods=['GET'])
def listar_sms():
    """Listar todos os SMS"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        sms_list = db.get_sms(limit, offset)
        total = db.count_sms()
        
        return jsonify({
            'sms': sms_list,
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/numeros', methods=['GET'])
def listar_numeros():
    """Listar números ativos"""
    try:
        numeros = db.get_numeros_ativos()
        
        return jsonify({
            'numeros': numeros,
            'total': len(numeros)
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/numero/<numero>/sms', methods=['GET'])
def sms_por_numero(numero):
    """Listar SMS de um número específico"""
    try:
        limit = request.args.get('limit', 50, type=int)
        sms_list = db.get_sms_por_numero(numero, limit)
        
        return jsonify({
            'numero': numero,
            'sms': sms_list,
            'total': len(sms_list)
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """Estatísticas"""
    try:
        stats_data = {
            'total_sms': db.count_sms(),
            'numeros_ativos': len(db.get_numeros_ativos()),
            'sms_ultimah': db.count_sms_ultima_hora(),
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(stats_data), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============ WEBSOCKET ============

@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    client_id = request.sid
    clients[client_id] = {
        'conectado_em': datetime.now().isoformat(),
        'endereco_ip': request.remote_addr
    }
    
    # Enviar dados iniciais
    numeros = db.get_numeros_ativos()
    sms_list = db.get_sms(limit=20)
    
    emit('dados_iniciais', {
        'numeros': numeros,
        'sms': sms_list,
        'timestamp': datetime.now().isoformat()
    })
    
    # Notificar outros clientes
    socketio.emit('cliente_conectado', {
        'total_clientes': len(clients),
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)
    
    print(f"[CONNECT] Cliente {client_id} conectado. Total: {len(clients)}")


@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    client_id = request.sid
    if client_id in clients:
        del clients[client_id]
    
    socketio.emit('cliente_desconectado', {
        'total_clientes': len(clients),
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)
    
    print(f"[DISCONNECT] Cliente {client_id} desconectado. Total: {len(clients)}")


@socketio.on('ping')
def handle_ping():
    """Keep-alive"""
    emit('pong', {
        'timestamp': datetime.now().isoformat()
    })


# ============ LIMPEZA AUTOMÁTICA ============

def cleanup_old_sms():
    """Limpar SMS mais antigos que 5 horas a cada 1 hora"""
    while True:
        try:
            # Esperar 1 hora
            threading.Event().wait(3600)
            
            # Calcular limite (5 horas atrás)
            limite = datetime.now() - timedelta(hours=5)
            
            # Deletar
            deletados = db.delete_sms_antes(limite)
            
            if deletados > 0:
                print(f"[CLEANUP] {deletados} SMS antigos deletados")
                socketio.emit('sms_expirados', {
                    'quantidade': deletados,
                    'timestamp': datetime.now().isoformat()
                }, broadcast=True)
        
        except Exception as e:
            print(f"[ERRO] Cleanup: {str(e)}")


# Iniciar thread de limpeza
cleanup_thread = threading.Thread(target=cleanup_old_sms, daemon=True)
cleanup_thread.start()


# ============ MAIN ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════╗
    ║  SMS FORWARDER - BACKEND               ║
    ║  Backend iniciado!                     ║
    ╚════════════════════════════════════════╝
    """)
    
    print("🚀 Servidor rodando em http://localhost:5000")
    print("📊 WebSocket disponível em ws://localhost:5000/socket.io")
    print("💾 Database: SMS armazenados por 5 horas")
    print("\n[INFO] Endpoints disponíveis:")
    print("  GET  /api/sms           - Listar SMS")
    print("  POST /api/sms           - Receber SMS (Android)")
    print("  GET  /api/numeros       - Números ativos")
    print("  GET  /api/stats         - Estatísticas")
    print("  GET  /health            - Health check")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )
