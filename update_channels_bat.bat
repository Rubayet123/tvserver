@echo off
REM Run the Python script to generate channels.m3u
python generate_channels.py

REM Navigate to your GitHub repository
cd C:\Users\Rubayet Alam\Documents\VScode Projects\Vscode_My_Apps\TV_server_scrape

REM Add the updated channels.m3u file to Git
git add channels.m3u

REM Commit the changes
git commit -m "Overwrite channels.m3u with local version"

REM Force push the changes to GitHub
git push --force origin main
