@echo off
rem Build + test script for Windows (used locally and in GitHub Actions).
setlocal

echo ==^> step: cd to project root
cd /d "%~dp0" || exit /b 1

echo ==^> step: select interpreter
if defined PYTHON (
    set "PY=%PYTHON%"
) else (
    rem "python3 --version" (not "where") skips the Microsoft Store stub alias
    python3 --version >nul 2>&1 && (set "PY=python3") || (set "PY=python")
)
"%PY%" --version || exit /b 1

echo ==^> step: create virtual environment
if not exist ".venv\Scripts\python.exe" (
    "%PY%" -m venv .venv || exit /b 1
)
set "VPY=.venv\Scripts\python.exe"

echo ==^> step: install dependencies
"%VPY%" -m pip install --upgrade pip || exit /b 1
"%VPY%" -m pip install -r requirements-dev.txt || exit /b 1

echo ==^> step: run tests
if not exist reports mkdir reports
"%VPY%" -m pytest -v --junitxml=reports/junit.xml || exit /b 1

echo ==^> step: build executable
if exist dist rmdir /s /q dist
"%VPY%" -m PyInstaller --noconfirm --onefile --name hello --paths src --distpath dist --workpath build --specpath build src\hello_app\__main__.py || exit /b 1

echo ==^> step: smoke test
if not exist "dist\hello.exe" (
    echo smoke test failed: dist\hello.exe not found 1>&2
    exit /b 1
)
"dist\hello.exe" > reports\smoke.txt || exit /b 1
type reports\smoke.txt
findstr /c:"Hello, World!" reports\smoke.txt >nul || (
    echo smoke test failed: unexpected output 1>&2
    exit /b 1
)

echo ==^> CI OK
exit /b 0
