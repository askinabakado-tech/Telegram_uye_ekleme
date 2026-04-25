"""
Telegram API Yapılandırması

ÖNEMLI: Artık tüm API bilgileri web panelinden dinamik olarak girilir!

YENİ YÖNTEM (Web paneli kullanın):
  1. http://localhost:5000 açın
  2. "🔧 API Ayarları" bölümünde bilgileri girin:
     - API ID (my.telegram.org/apps adresinden)
     - API Hash (my.telegram.org/apps adresinden)
     - Telefon Numarası (+905551234567 formatında)
  3. "💾 Ayarları Kaydet" tıklayın
  4. "📍 Hedef Grup/Kanal ID" alanına grup ID'sini girin
  5. "💾 Kaydet" tıklayın
  6. "🔗 Telegram'a Bağlan" tıklayın
  7. SMS kodu girin ve başlayın!
"""

# Zamanlama
DELAY_SECONDS = 30  # Her kullanıcı arasında bekleme süresi (saniye)

# Flask Ayarları
SECRET_KEY = "your-secret-key-change-this"
DEBUG = False
HOST = "0.0.0.0"
PORT = 5000
