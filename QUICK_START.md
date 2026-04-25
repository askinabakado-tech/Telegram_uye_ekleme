# ⚡ HIZLI BAŞLANGIÇ (5 Dakika)

## Adım 1: API Bilgilerini Al (2 dakika)

1. **https://my.telegram.org/apps** adresine git
2. Telefon numarası ile giriş yap
3. "Create Application" tıkla
4. Formu doldur:
   - **App name**: "Telegram Üye Ekleme"
   - **Short name**: "uye_ekleme"
5. **API_ID** ve **API_HASH**'i kopyala

## Adım 2: config.py Düzenle (1 dakika)

`config.py` dosyasını aç ve şunları gir:

```python
API_ID = 12345678                    # Adım 1'den aldığın API ID
API_HASH = "abcd1234efgh5678..."      # Adım 1'den aldığın API Hash
PHONE_NUMBER = "+905551234567"       # Telegram hesapların telefon (başında +90)
TARGET_GROUP_ID = -1001234567890     # Hedef grup ID (aşağıda bak)
```

### Hedef Grup ID'sini Bulma:

**En Kolay Yol:**
1. Grubunuzu Telegram'da aç
2. Grubun adına sağ tıkla → "Copy Link"
3. Linki not defterine yapıştır: `https://t.me/c/1234567890/`
4. Sayıyı kopyala: `1234567890`
5. Başına `-100` ekle: `-1001234567890` ✓

## Adım 3: Programı Çalıştır (1 dakika)

### Windows'ta:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### Linux/Mac'te:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Veya kullanın:**
- Windows: `run.bat` dosyasını çift tıkla
- Linux/Mac: `bash run.sh` komutu çalıştır

## Adım 4: Web Panelini Aç (1 dakika)

Tarayıcında aç: **http://localhost:5000**

## Adım 5: Kullanıcı Ekle (5 saniye)

1. "Telegram'a Bağlan" tıkla
2. SMS'deki kodu gir
3. TXT/CSV dosya yükle (her satırda bir username)
4. "Eklemeye Başla" tıkla
5. ✅ Hazır!

---

## 📝 Örnek Dosya Oluştur

```bash
python create_examples.py
```

Bu şu dosyaları oluşturacak:
- `example_users.txt`
- `example_users.csv`
- `example_users.xlsx`

---

## ⚠️ Önemli Noktalar

❌ **YAPMA:**
- API Hash'i kimseyle paylaşma
- Başkaının grubuna kullanıcı ekleme
- 20 saniyeden kısa interval ayarlama

✅ **YAP:**
- Sadece kendi gruplarına kullanıcı ekle
- 30 saniye intervalı kullan
- Telegram'ın ToS'unu oku

---

## 🆘 Sorun Giderme

### "Port 5000 zaten kullanımda"
```powershell
Get-NetTCPConnection -LocalPort 5000 | Stop-Process -Force
```

### "ModuleNotFoundError: No module named 'telethon'"
```
pip install telethon openpyxl flask
```

### "Kullanıcı bulunamadı hatası"
- Kullanıcı adı doğru mu?
- Kullanıcı hesabı mı silindi?
- Kullanıcı gizli mu?

### "Bağlanmıyor / SMS kodu almıyor"
- API bilgileri doğru mu?
- İnternet bağlantın var mı?
- 2FA'nı devre dışı bırak (geçici)

---

## 🎯 Başarılı Başlatma İşareti

Konsolda şunu görmeli:
```
🚀 Telegram Toplu Üye Ekleme Paneli Başlıyor...
📍 http://0.0.0.0:5000
⚠  config.py dosyasında API_ID ve API_HASH bilgilerini girin
```

Tarayıcı otomatik açılacak veya http://localhost:5000 ziyaret et ✓

---

**🚀 Başarılar!**
