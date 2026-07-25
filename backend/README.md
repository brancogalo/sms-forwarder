# ☁️ Backend - SMS Server

Servidor que recebe SMS do Android em tempo real e armazena por 5 horas.

## ⚙️ Especificações

- **Recebe SMS:** Assim que chegar do Android
- **Armazena:** Por 5 horas (depois deleta automaticamente)
- **Acesso:** Pela PC App (Windows)
- **Comunicação:** HTTP + WebSocket (tempo real)
- **Banco:** SQLite local

## 🛠️ Stack

- **Framework:** Flask (Python)
- **Database:** SQLite (local, 5h)
- **WebSocket:** Flask-SocketIO (tempo real)
- **Deploy:** Local primeiro (Railway depois se quiser)

## 📦 Dependências

```
Flask==2.3.0
Flask-CORS==4.0.0
Flask-SocketIO==5.3.0
python-dotenv==1.0.0
psycopg2-binary==2.9.0  # Para PostgreSQL
SQLAlchemy==2.0.0
python-jose==3.3.0     # JWT
```

## 🚀 Endpoints API

### POST `/api/sms`
Receber SMS do Android
```json
{
  "numero": "+5585987654321",
  "mensagem": "Olá!",
  "timestamp": "2026-07-25T21:00:00Z",
  "token": "seu_token_aqui"
}
```

### GET `/api/sms`
Listar todos os SMS
```
GET /api/sms?limit=50&offset=0
Authorization: Bearer token
```

### GET `/api/numeros`
Listar números ativos
```
GET /api/numeros
Authorization: Bearer token
```

### WebSocket `/socket.io`
Conexão em tempo real para atualizações

## 🗄️ Schema Database

```sql
-- Tabela de SMS
CREATE TABLE sms (
  id SERIAL PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  mensagem TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW(),
  lido BOOLEAN DEFAULT FALSE
);

-- Tabela de Números Ativos
CREATE TABLE numeros_ativos (
  numero VARCHAR(20) PRIMARY KEY,
  ultimo_sms TIMESTAMP,
  quantidade INT DEFAULT 1
);

-- Tabela de Usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  email VARCHAR(100) UNIQUE NOT NULL,
  senha_hash VARCHAR(255) NOT NULL,
  token_api VARCHAR(255),
  criado_em TIMESTAMP DEFAULT NOW()
);
```

## 🔐 Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:pass@localhost/sms_db
SECRET_KEY=sua_chave_secreta_aqui
FLASK_ENV=production
FLASK_APP=app.py
JWT_SECRET=seu_jwt_secret
```

## 🚀 Desenvolvimento Local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

## 📦 Deploy Railway

1. Conectar GitHub
2. Selecionar este repo
3. Configurar variáveis de ambiente
4. Railway cria Postgres automaticamente
5. Deploy automático ao fazer push

## 📊 Monitoramento

- Logs em `/logs/`
- Metrics em `/api/stats`
- Health check em `/health`

## 🔄 Fluxo

```
Android envia SMS
    ↓ (POST /api/sms)
Backend recebe
    ↓
Salva no Database
    ↓
Emite WebSocket para todos os clientes
    ↓
PC recebe em tempo real
```
