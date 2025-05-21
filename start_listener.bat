@echo off
REM Script de démarrage automatique du listener 3CX
REM À placer à la racine du dossier Documents\FinalProject_3cx

REM Activation de l'environnement virtuel
call "%~dp0.venv\Scripts\activate.bat"

:loop
echo [%date% %time%] ➤ Démarrage du callvitesse_listener.py

REM Définition du fichier log avec date/heure
set LOGFILE=%~dp0logs\listener_%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%.log

REM Lancement du script avec redirection vers le fichier log
python "%~dp0scripts\callvitesse_listener.py" >> "%LOGFILE%" 2>&1

echo [%date% %time%] ❌ Le script callvitesse_listener.py s'est arrêté. Redémarrage dans 5 secondes...
timeout /t 5 /nobreak > nul
goto loop
