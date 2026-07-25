"""
Database module - SQLite para armazenar SMS
"""

import sqlite3
import json
from datetime import datetime
from threading import Lock

class Database:
    def __init__(self, db_file='sms_database.db'):
        self.db_file = db_file
        self.lock = Lock()
        self.init_db()
    
    def get_connection(self):
        """Obter conexão com database"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializar banco de dados"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tabela de SMS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    device_id TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de números ativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS numeros_ativos (
                    numero TEXT PRIMARY KEY,
                    quantidade INTEGER DEFAULT 1,
                    ultimo_sms TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'ativo'
                )
            ''')
            
            # Criar índices para melhorar performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_numero ON sms(numero)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON sms(timestamp)')
            
            conn.commit()
            conn.close()
            
            print("[DB] Banco de dados inicializado")
    
    def add_sms(self, sms_data):
        """Adicionar SMS ao banco"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sms (numero, mensagem, timestamp, device_id)
                VALUES (?, ?, ?, ?)
            ''', (
                sms_data['numero'],
                sms_data['mensagem'],
                sms_data['timestamp'],
                sms_data.get('device_id', 'desconhecido')
            ))
            
            sms_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return sms_id
    
    def get_sms(self, limit=50, offset=0):
        """Obter lista de SMS"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, numero, mensagem, timestamp, device_id
            FROM sms
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        sms_list = []
        for row in cursor.fetchall():
            sms_list.append({
                'id': row['id'],
                'numero': row['numero'],
                'mensagem': row['mensagem'],
                'timestamp': row['timestamp'],
                'device_id': row['device_id']
            })
        
        conn.close()
        return sms_list
    
    def get_sms_por_numero(self, numero, limit=50):
        """Obter SMS de um número específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, numero, mensagem, timestamp, device_id
            FROM sms
            WHERE numero = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (numero, limit))
        
        sms_list = []
        for row in cursor.fetchall():
            sms_list.append({
                'id': row['id'],
                'numero': row['numero'],
                'mensagem': row['mensagem'],
                'timestamp': row['timestamp'],
                'device_id': row['device_id']
            })
        
        conn.close()
        return sms_list
    
    def count_sms(self):
        """Contar total de SMS"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM sms')
        total = cursor.fetchone()['total']
        
        conn.close()
        return total
    
    def count_sms_ultima_hora(self):
        """Contar SMS da última hora"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as total FROM sms
            WHERE datetime(timestamp) >= datetime('now', '-1 hour')
        ''')
        total = cursor.fetchone()['total']
        
        conn.close()
        return total
    
    def update_numero_ativo(self, numero):
        """Atualizar/adicionar número ativo"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Tentar atualizar
            cursor.execute('''
                UPDATE numeros_ativos
                SET quantidade = quantidade + 1,
                    ultimo_sms = CURRENT_TIMESTAMP,
                    status = 'ativo'
                WHERE numero = ?
            ''', (numero,))
            
            # Se não existir, inserir
            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT INTO numeros_ativos (numero, quantidade, ultimo_sms, status)
                    VALUES (?, 1, CURRENT_TIMESTAMP, 'ativo')
                ''', (numero,))
            
            conn.commit()
            conn.close()
    
    def get_numeros_ativos(self):
        """Obter lista de números ativos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT numero, quantidade, ultimo_sms, status
            FROM numeros_ativos
            WHERE status = 'ativo'
            ORDER BY ultimo_sms DESC
        ''')
        
        numeros = []
        for row in cursor.fetchall():
            numeros.append({
                'numero': row['numero'],
                'quantidade': row['quantidade'],
                'ultimo_sms': row['ultimo_sms'],
                'status': row['status']
            })
        
        conn.close()
        return numeros
    
    def delete_sms_antes(self, data_limite):
        """Deletar SMS antes de uma data (para limpeza de 5h)"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM sms
                WHERE datetime(timestamp) < datetime(?)
            ''', (data_limite.isoformat(),))
            
            deletados = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deletados
    
    def get_stats(self):
        """Obter estatísticas gerais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM sms')
        total_sms = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM numeros_ativos WHERE status = "ativo"')
        numeros_ativos = cursor.fetchone()['total']
        
        cursor.execute('''
            SELECT COUNT(*) as total FROM sms
            WHERE datetime(timestamp) >= datetime('now', '-1 hour')
        ''')
        ultima_hora = cursor.fetchone()['total']
        
        conn.close()
        
        return {
            'total_sms': total_sms,
            'numeros_ativos': numeros_ativos,
            'sms_ultima_hora': ultima_hora,
            'timestamp': datetime.now().isoformat()
        }
