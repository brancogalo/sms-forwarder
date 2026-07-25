@echo off
echo.
echo ╔════════════════════════════════════════╗
echo ║  SMS FORWARDER - BACKEND               ║
echo ║  Iniciando servidor...                 ║
echo ╚════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não está instalado ou não está no PATH
    echo.
    echo Instale Python de: https://www.python.org/downloads/
    echo (Marque "Add Python to PATH" durante instalação)
    echo.
    pause
    exit /b 1
)

REM Criar ambiente virtual se não existir
if not exist venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências se não tiver
echo 📥 Instalando dependências...
pip install -q -r requirements.txt

REM Iniciar servidor
echo.
echo ✅ Iniciando servidor...
echo.
echo 🚀 Backend rodando em: http://localhost:5000
echo 📊 Compartilhado na rede: http://[SEU_IP]:5000
echo.
echo Para descobrir seu IP local:
echo   Abra CMD e digite: ipconfig
echo   Procure por "IPv4 Address" (exemplo: 192.168.1.100)
echo.
echo ⏸️  Pressione Ctrl+C para parar o servidor
echo.
pause

python app.py
