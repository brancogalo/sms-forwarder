@echo off
echo.
echo ╔════════════════════════════════════════╗
echo ║  SMS FORWARDER - COMPILAR EXE          ║
echo ║  Gerando executável Windows...         ║
echo ╚════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não está instalado ou não está no PATH
    pause
    exit /b 1
)

REM Criar ambiente virtual se não existir
if not exist venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📥 Instalando dependências...
pip install -q -r requirements.txt
pip install -q pyinstaller

REM Compilar EXE
echo 🔨 Compilando para EXE...
echo.

pyinstaller --onefile ^
    --icon=app.ico ^
    --name="SMS Forwarder" ^
    --windowed ^
    --console ^
    pc_app.py

echo.
echo ✅ Compilação concluída!
echo.
echo 📁 Arquivo gerado em: dist\SMS Forwarder.exe
echo.
echo Próximo passo:
echo   1. Copie "dist\SMS Forwarder.exe" para a área de trabalho
echo   2. Clique 2x para executar
echo   3. Digite URL do Backend
echo.
pause
