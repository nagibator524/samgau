@echo off
echo Preparing for Vercel deployment...
echo.

echo 1. Checking if all required files exist...
if exist "app.py" (
    echo ✓ app.py found
) else (
    echo ✗ app.py missing
    exit /b 1
)

if exist "wsgi.py" (
    echo ✓ wsgi.py found
) else (
    echo ✗ wsgi.py missing
    exit /b 1
)

if exist "vercel.json" (
    echo ✓ vercel.json found
) else (
    echo ✗ vercel.json missing
    exit /b 1
)

if exist "requirements.txt" (
    echo ✓ requirements.txt found
) else (
    echo ✗ requirements.txt missing
    exit /b 1
)

if exist "static\images\logo.jpeg" (
    echo ✓ logo.jpeg found
) else (
    echo ✗ logo.jpeg missing
    exit /b 1
)

echo.
echo 2. All files are ready for deployment!
echo.
echo 3. Next steps:
echo    - Push your code to a Git repository (GitHub, GitLab, etc.)
echo    - Go to https://vercel.com
echo    - Click "New Project"
echo    - Import your repository
echo    - Deploy!
echo.
echo 4. Or use Vercel CLI:
echo    - Install: npm i -g vercel
echo    - Run: vercel
echo.
pause
