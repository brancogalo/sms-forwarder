# 🔨 Como Gerar EXE do PC App

Instruções passo a passo para criar um executável Windows pronto para usar.

---

## 📋 Pré-requisitos

1. **Python 3.9+** instalado
   - [Baixar](https://www.python.org/downloads/)
   - ⚠️ Marcar "Add Python to PATH" na instalação!

2. **Verificar Python instalado:**
   ```bash
   python --version
   ```
   Resultado esperado: `Python 3.9.x` ou superior

---

## 🚀 Opção 1: Automática (Recomendado)

Se estiver na pasta `pc-app/`:

```bash
# Duplo clique em:
COMPILAR_EXE.bat

# Ou em CMD:
COMPILAR_EXE.bat
```

**Pronto!** O arquivo EXE será gerado em `dist/SMS Forwarder.exe`

---

## 🚀 Opção 2: Manual

Se o .bat não funcionar ou quiser fazer passo a passo:

### Passo 1: Criar Ambiente Virtual

```bash
# Abrir CMD em pc-app/
cd pc-app

# Windows
python -m venv venv
venv\Scripts\activate

# Você deve ver (venv) antes do path
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Passo 3: Gerar EXE

```bash
pyinstaller --onefile ^
    --name="SMS Forwarder" ^
    --console ^
    pc_app.py
```

**Aguarde 2-5 minutos...**

### Passo 4: Localizar EXE

```
Arquivo gerado em:
dist/SMS Forwarder.exe
```

---

## 📦 Resultado Final

```
pc-app/
├── dist/
│   └── SMS Forwarder.exe    ← 👈 Arquivo principal
├── build/                    (pode ignorar)
├── pc_app.spec              (pode ignorar)
└── ...
```

---

## 🎯 Usar o EXE

### Opção 1: Direto da Pasta

```
1. Abrir pasta: pc-app/dist/
2. Duplo clique em: SMS Forwarder.exe
3. Digite URL do Backend
4. Pronto!
```

### Opção 2: Copiar para Área de Trabalho

```
1. Direita em: SMS Forwarder.exe
2. Enviar para → Área de Trabalho (atalho)
3. Na desktop, duplo clique
4. Pronto!
```

### Opção 3: Criar Pasta Separada

```
1. Criar pasta: C:\SMS Forwarder\
2. Copiar: SMS Forwarder.exe (para essa pasta)
3. Duplo clique para rodar
4. Criar atalho na desktop se quiser
```

---

## ⚙️ Usar o EXE (Em Detalhes)

### Primeira Vez

```
1. Duplo clique em SMS Forwarder.exe

2. Abre janela CMD:
   ╔═════════════════════════════════════════╗
   ║  SMS FORWARDER - MONITOR PC             ║
   ║  Windows CMD - Tempo Real               ║
   ╚═════════════════════════════════════════╝

3. Será pedido:
   URL do Backend [localhost:5000]: 
   
4. Opções:
   - Se Backend na mesma máquina: Pressione Enter
   - Se outro PC: Digite IP (ex: 192.168.1.100:5000)
   - Se domínio: Digite (ex: seu-site.com)

5. Pressione Enter

6. Conecta e mostra SMS!
```

### Dashboard

```
════════════════════════════════════════════
  SMS FORWARDER - MONITOR
════════════════════════════════════════════

Status: ✓ ONLINE
Horário: 14:30:45

NÚMEROS ATIVOS (2)
──────────────────────────────────────────
🟢 +5585987654321 (3 SMS)
🟢 +5585999999999 (1 SMS)

ÚLTIMOS SMS
──────────────────────────────────────────
[14:32] +5585987654321
       "Oi, como vai?"

[14:28] +5585999999999
       "Tudo bem?"

────────────────────────────────────────────
Pressione Ctrl+C para sair
```

---

## 📝 URL do Backend

### Se Backend Local

```
URL do Backend [localhost:5000]: 
→ Pressionar Enter (usa padrão)
```

### Se Backend em Outro PC

```
1. Descobrir IP da máquina do Backend:
   CMD: ipconfig
   Procurar: IPv4 Address (ex: 192.168.1.100)

2. Na janela do EXE:
   URL do Backend [localhost:5000]: 192.168.1.100:5000
   → Pressionar Enter

3. Pronto! Conecta ao PC remoto
```

### Se Backend na Nuvem (Railway)

```
1. Pegar URL do Railway (ex: sms-forwarder-123.railway.app)

2. Na janela do EXE:
   URL do Backend [localhost:5000]: sms-forwarder-123.railway.app
   → Pressionar Enter

3. Pronto! Conecta à nuvem
```

---

## 🔐 Onde Salvar o EXE?

### Opção A: Área de Trabalho
```
C:\Users\[Seu Usuário]\Desktop\SMS Forwarder.exe
```
✅ Fácil acesso

### Opção B: Pasta do Usuário
```
C:\Users\[Seu Usuário]\SMS Forwarder.exe
```
✅ Organizado

### Opção C: Pasta do Projeto
```
C:\[pasta do projeto]\pc-app\dist\SMS Forwarder.exe
```
✅ Junto com código

### Opção D: Programa Files
```
C:\Program Files\SMS Forwarder\SMS Forwarder.exe
```
⚠️ Precisa de permissão admin

---

## ⚠️ Antivírus / SmartScreen

Se Windows avisar que arquivo é suspeito:

```
1. Mensagem aparece: "Windows protected your PC"
2. Clicar em "More info"
3. Clicar em "Run anyway"
4. Pronto! EXE abre
```

**Por que aparece?**
- PyInstaller gera executáveis que antivírus desconhecem
- Completamente seguro (código aberto no GitHub)

---

## 🐛 Troubleshooting

### EXE não abre

**Solução 1:**
```bash
# Tentar rodar direto da pasta pc-app
cd pc-app
python pc_app.py
# Se funcionar aqui, compilação teve erro
```

**Solução 2:**
```bash
# Recompilar EXE
# Deletar pastas: dist/, build/, __pycache__
# Rodar COMPILAR_EXE.bat novamente
```

### Antivírus bloqueia EXE

**Solução:**
```
1. Excluir pasta do projeto do antivírus
2. Ou compilar com PyInstaller --onefile --noconsole
3. Ou usar versão Python (.py) direto
```

### EXE não conecta ao Backend

**Verificar:**
```
1. Backend está rodando? 
   (Command: python app.py)

2. Firewall bloqueando porta 5000?
   Windows Defender → Firewall → Apps permitidas
   Permitir Python.exe

3. IP está correto?
   Se Backend em outro PC:
   - Verificar IP com: ipconfig
   - Testar no navegador: http://192.168.1.100:5000/health
   - Se abre, URL está certa
```

### EXE abre mas fecha imediatamente

**Solução:**
```
1. Rodar via CMD para ver erro:
   CMD > cd dist
   CMD > SMS Forwarder.exe

2. Ler mensagem de erro
3. Se for dependência faltando:
   - Recompilar com: pip install -r requirements.txt
   - Depois: pyinstaller --onefile pc_app.py
```

---

## 📊 Tamanho do EXE

- **Esperado:** 30-50 MB
- **Razão:** Python inteiro + bibliotecas inclusos
- **Normal:** PyInstaller cria executáveis grandes

---

## 🔄 Atualizar EXE

Se mudar código em `pc_app.py`:

```bash
1. Editar pc_app.py
2. Rodar: COMPILAR_EXE.bat
3. Novo EXE gerado automaticamente
4. Copiar para lugar de uso
```

---

## 📦 Distribuir EXE

Para dar para outra pessoa:

```bash
# Arquivo necessário:
dist/SMS Forwarder.exe

# Enviar via:
- Email (anexo)
- Google Drive
- Pendrive
- GitHub Releases

# Pessoa pode:
1. Baixar EXE
2. Duplo clique
3. Usar direto (sem instalar Python)
```

---

## ✅ Resumo Rápido

1. **Gerar:** Rodar COMPILAR_EXE.bat
2. **Esperar:** 2-5 minutos de compilação
3. **Localizar:** dist/SMS Forwarder.exe
4. **Executar:** Duplo clique no EXE
5. **Configurar:** Digitar URL do Backend
6. **Usar:** Receber SMS em tempo real

---

## 🚀 Pronto!

Seu EXE está pronto para usar! 

**Não precisa mais de:**
- ❌ CMD/Terminal
- ❌ Python instalado
- ❌ pip install
- ❌ Nada complicado

**Só:**
- ✅ Duplo clique no EXE
- ✅ Digitar URL
- ✅ Receber SMS!

---

**Sucesso na compilação!** 🎉
