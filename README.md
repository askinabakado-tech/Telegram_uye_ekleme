# Telegram Toplu Üye Ekleme Paneli - README

## 📋 Sistem Özeti

Bu sistem, Telegram grubunuza/kanalınıza toplu olarak kullanıcı eklemek için tasarlanmıştır.

**Özellikler:**
- ✅ Web tabanlı modern arayüz
- ✅ Toplu dosya yüklemesi (TXT, CSV, XLSX)
- ✅ 30 saniye bekleme mekanizması (Telegram rate limit'i aşmamak için)
- ✅ Real-time ilerleme takibi
- ✅ Detaylı sonuç raporlaması
- ✅ Hata yönetimi

## 🚀 Kurulum Adımları

### 1. Python Kurulumu
Python 3.8 veya daha yüksek olmalı
```
python --version
```

### 2. Telegram API Bilgileri Alma

1. https://my.telegram.org/apps adresine gidin
2. Telefon numaranız ile giriş yapın
3. "Create Application" tıklayın
4. Bilgileri doldurun (App name, Short name vs)
5. **API ID** ve **API Hash**'i kopyalayın

### 3. Proje Ayarları

`config.py` dosyasını açın ve bilgileri girin:

```python
API_ID = 12345678        # Yukarıda aldığınız API ID
API_HASH = "abcd1234..."  # Yukarıda aldığınız API Hash
PHONE_NUMBER = "+905551234567"  # Telegram hesabınızın telefon numarası
TARGET_GROUP_ID = -1001234567890  # Hedef grubun/kanalın ID'si
```

#### Hedef Grup/Kanal ID'sini Bulma:

**Seçenek 1 (Kolay):** 
- Grubu açın → Info menüsü → Grubun linkine sağ tıkla → "Copy Link" 
- Link: `t.me/c/1234567890/` → ID: `-1001234567890`

**Seçenek 2 (Python ile):**
```python
from telethon import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)
# Telegram'a bağlanın
# Grubu bulun ve entity.id'sini aldığınız chat_id değeridir
```

### 4. Sanal Ortam Oluştur

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Bağımlılıkları Kur

```
pip install -r requirements.txt
```

### 6. Uygulamayı Başlat

```
python main.py
```

Başarılı başlangıçta şu çıkış görüntülenecek:
```
🚀 Telegram Toplu Üye Ekleme Paneli Başlıyor...
📍 http://0.0.0.0:5000
```

### 7. Web Paneline Erişim

Tarayıcıda aç: **http://localhost:5000**

## 📱 Kullanım Talimatları

### Adım 1: Telegram'a Bağlan
1. "Telegram'a Bağlan" butonuna tıkla
2. Telegram sana SMS ile kod gönderecek
3. Kodu gir
4. 2FA varsa, şifreni gir
5. "Bağlı ✓" durumunu görüncene kadar bekle

### Adım 2: Kullanıcı Listesi Yükle
1. "Dosya Seçin" alanına TXT, CSV veya XLSX dosyası yükle
2. **Dosya formatı:**
   - Her satırda bir kullanıcı adı
   - @ ile başlayabilir veya başlamayabilir
   - Örnek: `username1`, `@username2`, `USERNAME3`

**Örnek TXT dosyası:**
```
john_doe
maria_smith
@alex_jones
user_123
```

**Örnek CSV dosyası:**
```
username
john_doe
maria_smith
alex_jones
```

### Adım 3: Eklemeyi Başlat
1. "Eklemeye Başla" butonuna tıkla
2. Her kullanıcı arasında 30 saniye bekleme yapılacak
3. İlerleme çubuğunun artmasını izle
4. Sonuçları gerçek zamanlı olarak görüntüle

### Sonuçlar

Ekran aşağıdaki bilgileri gösterecek:
- ✓ **Başarılı**: Başarıyla eklenen kullanıcılar
- ✗ **Başarısız**: Ekleme başarısız olan kullanıcılar
- ⚠ **Zaten Üye**: Halihazırda gruptaki kullanıcılar
- 🔒 **Engelli**: Gizlilik ayarlarından engellenen kullanıcılar

## ⚙️ İleri Ayarlar

### Bekleme Süresini Değiştir

`config.py`'de değiştir:
```python
DELAY_SECONDS = 30  # 30 saniye → istediğin değer
```

**Not:** Telegram rate limiting'i aşmamak için 30 saniyeden az ayarlamayın!

### Port Değiştir

`config.py`'de değiştir:
```python
PORT = 5000  # Başka port numarası gir
```

### Ortamda Çalıştır

```python
DEBUG = True  # Geliştirme ortamı
# veya
DEBUG = False  # Üretim ortamı
```

## 🔐 Güvenlik Notları

1. **Session File**: İlk bağlantı sonrası `session_name.session` dosyası oluşturulur
   - Bu dosyayı güvenli bir yerde saklayın
   - Paylaşmayın!

2. **API Bilgileri**: `config.py` dosyasını asla paylaşmayın
   - `.gitignore`'a ekleyin

3. **Grup Gizliliği**: 
   - Sadece sahip olduğunuz gruplara kullanıcı ekleyin
   - Telegram ToS'a uyun

## 🆘 Sık Sorulan Sorular

### P: "Flood Wait" hatası alıyorum?
C: Telegram rate limiting yapıyor. Bekleme süresini artırın veya sonra tekrar deneyin.

### P: Kullanıcı bulunamıyor hatası?
C: 
- Kullanıcı adı doğru yazılı mı?
- Kullanıcı var mı?
- Kullanıcı hesabını gizli tuttu mu?

### P: Grup ID'sini nasıl bulabilirim?
C: Grubun linkini kopyalayın ve format: `t.me/c/{ID}/` - `-100` ön ekini ekleyin.

### P: Bağlantı kesildi, tekrar başlamalı mı?
C: Evet, "Bağlantıyı Kes" sonra "Telegram'a Bağlan"ı tıklayın.

### P: Kaç kullanıcıya tek seferde ekleyebilirim?
C: Teorik olarak sınırsız, ancak Telegram rate limiting'i dikkate alın (30sn/user).

## 🐛 Sorun Giderme

### Portun zaten kullanımda olması
```powershell
# Portu kullanan işlemi bul ve kapat
Get-NetTCPConnection -LocalPort 5000 | Stop-Process -Force
```

### Telethon sorunları
```
pip install --upgrade telethon
```

### Session sorunları
```
# session_name.session dosyasını sil ve yeniden bağlan
Remove-Item session_name.session
```

## 📞 Destek

Herhangi bir sorun için:
1. Consol output'unu kontrol et
2. `config.py` ayarlarını doğrula
3. Telegram API limitleri kontrol et

## ⚠️ Uyarılar

- **Spam Engeli**: Çok hızlı kullanıcı eklerse Telegram seni kısa süreliğine banlar
- **Gizlilik**: Bazı kullanıcılar gruplara eklenmek istemiyor olabilir
- **ToS**: Telegram hizmet şartlarına uyun

## 📄 Lisans

Bu proje kişisel kullanım için tasarlanmıştır.

---

**Başarılar! 🚀**
