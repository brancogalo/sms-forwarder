# 💻 Desktop App - SMS Visualizer (Windows)

Aplicação Windows para visualizar SMS em tempo real direto no CMD.

## ⚙️ Especificações

- **Plataforma:** Windows apenas
- **Interface:** CMD/Terminal (sem GUI por enquanto)
- **Linguagem:** Python
- **Execução:** `python pc_app.py` ou `python pc_app.py`
- **Tempo Real:** WebSocket com Backend

## 🛠️ Stack

- **Linguagem:** Python 3.9+
- **Framework:** PyQt6 (para versão GUI depois)
- **Comunicação:** WebSocket (python-socketio)
- **Plataforma:** Windows

## 📦 Dependências

```
PyQt6==6.5.0
python-socketio==5.9.0
python-engineio==4.7.1
requests==2.31.0
python-dotenv==1.0.0
```

## 🎨 Features

- ✅ Visualiza SMS em tempo real
- ✅ Mostra números ativos
- ✅ Filtro por número
- ✅ Busca por texto
- ✅ Notificações de novo SMS
- ✅ Salvar SMS como PDF
- ✅ Dark mode

## 📊 Interface

```
┌─────────────────────────────────────┐
│  SMS Forwarder        [_] [□] [×]   │
├─────────────────────────────────────┤
│ Números Ativos:                     │
│ ✓ +5585987654321 (5 SMS)            │
│ ✓ +5585999999999 (2 SMS)            │
├─────────────────────────────────────┤
│ 🔍 [Buscar...]      [Atualizar]     │
├─────────────────────────────────────┤
│                                     │
│ De: +5585987654321    22:45        │
│ "Oi, como vai?"                    │
│                                     │
│ De: +5585999999999    22:30        │
│ "Tudo bem?"                        │
│                                     │
└─────────────────────────────────────┘
```

## 🚀 Como Usar

```bash
# Clonar
git clone seu-repo
cd pc-app

# Criar venv
python -m venv venv
source venv/bin/activate

# Instalar
pip install -r requirements.txt

# Rodar
python main.py
```

## ⚙️ Configuração

Arquivo `config.json`:
```json
{
  "servidor": "https://seu-railway-app.com",
  "token": "seu_token_api",
  "auto_conectar": true,
  "tema": "escuro"
}
```

## 🔄 Fluxo

```
PC inicia
    ↓
Conecta ao servidor (WebSocket)
    ↓
Carrega SMS anterior
    ↓
Escuta atualizações em tempo real
    ↓
Novo SMS chega → notificação + exibe
```

## 📁 Estrutura

```
pc-app/
├── main.py              # Arquivo principal
├── ui/
│   ├── main_window.py   # Janela principal
│   ├── config_dialog.py # Dialog de config
│   └── styles.py        # Temas/CSS
├── api/
│   └── client.py        # Cliente HTTP/WebSocket
├── requirements.txt
└── config.json
```

## 🔌 Conectar ao Servidor

1. Abrir o app
2. Menu: Settings → Server Configuration
3. Colar URL do Railway
4. Colar Token API
5. Conectar
6. Pronto!

## 📝 Logs

Logs salvos em `logs/desktop-app.log`

## 🐛 Troubleshooting

- Não conecta? Verificar URL e Token
- Nenhum SMS? Verificar se Android está enviando
- Lento? Aumentar refresh rate em config
