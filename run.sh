#!/bin/bash
# Telegram Toplu Üye Ekleme - Başlatma Scripti (Linux/Mac)

echo ""
echo "========================================"
echo "  Telegram Toplu Uye Ekleme Paneli"
echo "========================================"
echo ""

# Python kontrol
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 kurulu degil!"
    echo "Lutfen Python 3.8+ kurunuz"
    exit 1
fi

echo "[OK] Python bulundu"

# Sanal ortam kontrol
if [ ! -d "venv" ]; then
    echo "[INFO] Sanal ortam olusturuluyor..."
    python3 -m venv venv
    echo "[OK] Sanal ortam olusturuldu"
fi

# Sanal ortamı aktif et
echo "[INFO] Sanal ortam aktif ediliyor..."
source venv/bin/activate

# Bağımlılıklar kontrol
echo "[INFO] Baglantiliklar kontrol ediliyor..."
if ! pip list | grep -q Flask; then
    echo "[INFO] Baglantiliklar yukleniyor..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Baglantilik yukleme basarisiz!"
        exit 1
    fi
    echo "[OK] Baglantiliklar yuklendi"
fi

# config.py kontrol
echo ""
echo "========================================"
echo "  AYARLAR KONTROL EDILIYOR"
echo "========================================"
echo ""

python3 -c "from config import API_ID, API_HASH, PHONE_NUMBER, TARGET_GROUP_ID; print('API_ID:', API_ID); print('PHONE:', PHONE_NUMBER); print('TARGET_GROUP_ID:', TARGET_GROUP_ID)"

if [ $? -ne 0 ]; then
    echo ""
    echo "[WARNING] config.py dosyasinda sorun var!"
    echo ""
    echo "Lutfen config.py dosyasini acin ve bilgileri girin:"
    echo "  - API_ID"
    echo "  - API_HASH"
    echo "  - PHONE_NUMBER"
    echo "  - TARGET_GROUP_ID"
    echo ""
    exit 1
fi

echo "[OK] Ayarlar basarili"

# Uygulama başlat
echo ""
echo "========================================"
echo "  UYGULAMA BASLATILIYOR"
echo "========================================"
echo ""

python3 main.py
