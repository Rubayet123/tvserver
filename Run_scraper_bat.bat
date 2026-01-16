@echo off
setlocal

REM ===== Run Python scrapers =====
python generate_channels-rforce.py
python generate_channels-rzone.py

REM ===== Go to GitHub repo =====
cd /d "C:\Users\Rubayet Alam\Documents\VScode Projects\Vscode_My_Apps\TV_server_scrape"

REM ===== Add generated M3U files =====
git add channels-rforce.m3u
git add channels-rzone.m3u

REM ===== Commit changes =====
git commit -m "Auto-update channel playlists"

REM ===== Push to GitHub =====
git push --force origin main

endlocal
