@echo off
REM Telegram Toplu Üye Ekleme - Başlatma Scripti (Windows)

echo.
echo ========================================
echo  Telegram Toplu Uye Ekleme Paneli
echo ========================================
echo.

REM Python kontrol
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python kurulu degil!
    echo Lutfen Python 3.8+ kurunuz: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python bulundu

REM Sanal ortam kontrol
if not exist "venv\" (
    echo [INFO] Sanal ortam olusturuluyor...
    python -m venv venv
    echo [OK] Sanal ortam olusturuldu
)

REM Sanal ortamı aktif et
echo [INFO] Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat

REM Bağımlılıklar kontrol
echo [INFO] Baglantiliklar kontrol ediliyor...
pip list | find "Flask" >nul
if %errorlevel% neq 0 (
    echo [INFO] Baglantiliklar yukleniyor... (ilk kez biraz uzun surebilir)
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Baglantilik yukleme basarisiz!
        pause
        exit /b 1
    )
    echo [OK] Baglantiliklar yuklendi
)

REM config.py kontrol
echo.
echo ========================================
echo  AYARLAR KONTROL EDILIYOR
echo ========================================
echo.

python -c "from config import API_ID, API_HASH, PHONE_NUMBER, TARGET_GROUP_ID; print('API_ID:', API_ID); print('API_HASH:', API_HASH[:10] + '...' if len(API_HASH) > 10 else 'BOSH'); print('PHONE:', PHONE_NUMBER); print('TARGET_GROUP_ID:', TARGET_GROUP_ID)" 2>nul

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] config.py dosyasinda sorun var!
    echo.
    echo Lutfen config.py dosyasini acin ve bilgileri girin:
    echo   - API_ID
    echo   - API_HASH
    echo   - PHONE_NUMBER
    echo   - TARGET_GROUP_ID
    echo.
    pause
    exit /b 1
)

echo [OK] Ayarlar basarili

REM Uygulama başlat
echo.
echo ========================================
echo  UYGULAMA BASLATILIYOR
echo ========================================
echo.

python main.py
