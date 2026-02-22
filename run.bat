@echo off
echo Starting MenuAI Backend and Frontend...

:: Start the FastAPI backend in a new command window
start cmd /k "title MenuAI-Backend && cd Backend && ..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

:: Start the HTML/JS frontend in a new command window using Python's built-in web server
start cmd /k "title MenuAI-Frontend && cd Frontend && ..\.venv\Scripts\python.exe -m http.server 3000"

echo Both services have been started in separate windows.
echo Frontend will be available at: http://localhost:3000
