@echo off
chcp 65001 > nul
title Deploiement SmartShop sur Render

echo ========================================================
echo        🚀 DEPLOIEMENT DE SMARTSHOP SUR RENDER
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/4] Enregistrement des modifications locales...
git add .
git commit -m "Refonte graphique : photos HD produits et mes commandes" > nul 2>&1
git branch -M main

echo.
echo [2/4] Verification du depot distant GitHub...
echo.
echo Veuillez coller l'adresse HTTPS de votre depot GitHub :
echo (Exemple : https://github.com/votre-nom/smartshop.git)
echo.
set /p REPO_URL="Adresse du depot GitHub : "

if "%REPO_URL%"=="" (
    echo.
    echo [!] Aucune adresse saisie. Operation annulee.
    goto FIN
)

echo.
echo [3/4] Configuration du lien GitHub...
git remote set-url origin %REPO_URL% > nul 2>&1
if errorlevel 1 (
    git remote add origin %REPO_URL% > nul 2>&1
)

echo.
echo [4/4] Envoi des fichiers vers GitHub (deploiement Render)...
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================================
    echo  [!] L'envoi a echoue.
    echo      Verifiez que votre adresse GitHub est correcte
    echo      et que vous etes bien connecte a GitHub.
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo  [OK] SUCCES ! Tous les fichiers sont envoyes a GitHub.
    echo       Render va deployer automatiquement votre site
    echo       sur https://smartshop-awbu.onrender.com/
    echo ========================================================
)

:FIN
echo.
pause

