@echo off
REM Lancer l'application Streamlit GUI
REM Double-cliquez sur ce fichier pour démarrer l'application

title Systeme de Recommandation IA - Streamlit GUI
cd /d "%~dp0"

echo.
echo ============================================================
echo   Systeme de Recommandation d'Outils IA
echo   Interface Graphique Streamlit
echo ============================================================
echo.

REM Vérifier si Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo. 
    echo Erreur: Python n'est pas installé ou pas dans PATH
    pause
    exit /b 1
)

REM Installer streamlit si nécessaire
python -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Installation de Streamlit...
    python -m pip install streamlit -q
)

REM Lancer l'app
echo.
echo Demarrage de l'application...
echo L'interface s'ouvrira a l'adresse: http://localhost:8501
echo.
echo Appuyez sur Ctrl+C pour arreter l'application.
echo.

python -m streamlit run app.py

pause
