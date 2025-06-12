@echo off
echo Starting HMM Shipping Tracking Automation...

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Installing Playwright browser...
playwright install chromium --with-deps --no-shell

echo Starting the tracking script...
python browser_auto.py

pause
