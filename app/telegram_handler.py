"""
Telegram API İşlemlerini Yöneten Modül
Telethon kütüphanesi kullanıyor
"""
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestricted, UserAlreadyParticipant
from config import DELAY_SECONDS
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramHandler:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone_number = None
        self.client = None
        self.is_connected = False
        self.target_group_id = None
        self.results = {
            'success': [],
            'failed': [],
            'already_member': [],
            'blocked': []
        }

    def set_credentials(self, api_id, api_hash, phone_number):
        self.api_id = int(api_id)
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)

    async def start_client(self):
        try:
            if not self.client:
                logger.error("✗ Client ayarlanmamış")
                return False
            # Bağlantıyı başlat, ancak kullanıcıya kod sormak için hemen bekleme
            await self.client.connect()
            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone_number)
                logger.info("✓ Doğrulama kodu gönderildi")
                # Bu noktada kodun girilmesi beklenir, bu yüzden False dönüyoruz
                self.is_connected = False
                return "code_needed"
            self.is_connected = True
            logger.info("✓ Telegram'a bağlanıldı")
            return True
        except Exception as e:
            logger.error(f"✗ Telegram bağlantı hatası: {str(e)}")
            return False

    async def verify_code(self, code, password=None):
        try:
            await self.client.sign_in(self.phone_number, code)
            self.is_connected = True
            return True
        except SessionPasswordNeededError:
            if password:
                await self.client.sign_in(password=password)
                self.is_connected = True
                return True
            else:
                return "2fa_needed"
        except Exception as e:
            logger.error(f"Doğrulama hatası: {str(e)}")
            return False
    
    async def stop_client(self):
        """Telegram istemcisini kapat"""
        try:
            if self.client:
                await self.client.disconnect()
            self.is_connected = False
            logger.info("✓ Telegram'dan çıkıldı")
        except Exception as e:
            logger.error(f"✗ Çıkış hatası: {str(e)}")
    
    async def add_user_to_group(self, username):
        """
        Bir kullanıcıyı gruba/kanala ekle
        
        Args:
            username: Telegram kullanıcı adı (@ olmadan)
        
        Returns:
            dict: İşlem sonucu
        """
        if not self.is_connected:
            return {
                'username': username,
                'status': 'error',
                'message': 'Telegram bağlantısı yok'
            }
        
        if not self.target_group_id:
            return {
                'username': username,
                'status': 'error',
                'message': 'Hedef grup belirtilmedi'
            }
        
        try:
            # Kullanıcıyı bul
            user = await self.client.get_entity(username)
            
            # Proper AddChatUserRequest kullan
            from telethon.tl.functions.channels import InviteToChannelRequest
            from telethon.tl.functions.messages import AddChatUserRequest
            
            try:
                # Kanal ise
                await self.client(InviteToChannelRequest(
                    channel=self.target_group_id,
                    user_ids=[user.id]
                ))
                logger.info(f"✓ {username} kanala eklendi")
                return {
                    'username': username,
                    'status': 'success',
                    'message': 'Başarıyla eklendi'
                }
            except:
                # Grup ise
                await self.client(AddChatUserRequest(
                    chat_id=self.target_group_id,
                    user_id=user.id,
                    fwd_limit=0
                ))
                logger.info(f"✓ {username} gruba eklendi")
                return {
                    'username': username,
                    'status': 'success',
                    'message': 'Başarıyla eklendi'
                }
        
        except UserAlreadyParticipant:
            logger.warning(f"⚠ {username} zaten üye")
            return {
                'username': username,
                'status': 'already_member',
                'message': 'Zaten üye'
            }
        
        except UserPrivacyRestricted:
            logger.warning(f"⚠ {username} gizlilik ayarlarından eklenemiyor")
            return {
                'username': username,
                'status': 'blocked',
                'message': 'Gizlilik kısıtlaması'
            }
        
        except FloodWaitError as e:
            wait_time = e.seconds
            logger.warning(f"⚠ Telegram flood kontrol: {wait_time} saniye bekleniyor")
            await asyncio.sleep(wait_time)
            return {
                'username': username,
                'status': 'error',
                'message': f'Flood kontrol, {wait_time} saniye beklendi'
            }
        
        except Exception as e:
            logger.error(f"✗ {username} eklenemiyor: {str(e)}")
            return {
                'username': username,
                'status': 'error',
                'message': f'Hata: {str(e)}'
            }
    
    async def add_users_bulk(self, usernames):
        """
        Birden fazla kullanıcıyı gruba/kanala ekle
        
        Args:
            usernames: Kullanıcı adlarının listesi
        
        Yields:
            dict: Her kullanıcı için işlem sonucu
        """
        for i, username in enumerate(usernames):
            # Kullanıcı adını temizle
            username = username.strip().lstrip('@').lower()
            
            if not username:
                continue
            
            # İşlem yap
            result = await self.add_user_to_group(username)
            yield {
                **result,
                'index': i + 1,
                'total': len(usernames)
            }
            
            # Bekleme (son kullanıcı için bekleme yok)
            if i < len(usernames) - 1:
                await asyncio.sleep(DELAY_SECONDS)


# Global istemci örneği
telegram_handler = None

async def get_handler():
    """Telegram handler'ı al veya oluştur"""
    global telegram_handler
    if telegram_handler is None:
        telegram_handler = TelegramHandler()
    return telegram_handler
