"""
Hızlı Testler - Telegram Toplu Üye Ekleme Paneli
"""

import unittest
import sys
import os

# Ana dizini ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestConfig(unittest.TestCase):
    """Config dosyası testleri"""
    
    def test_config_exists(self):
        """Config dosyası var mı?"""
        self.assertTrue(os.path.exists('config.py'))
    
    def test_config_readable(self):
        """Config dosyası okunabilir mi?"""
        try:
            from config import API_ID, API_HASH, PHONE_NUMBER, TARGET_GROUP_ID
            self.assertIsNotNone(API_ID)
            self.assertIsNotNone(API_HASH)
            self.assertIsNotNone(PHONE_NUMBER)
        except ImportError as e:
            self.fail(f"Config import hatası: {e}")


class TestFileStructure(unittest.TestCase):
    """Dosya yapısı testleri"""
    
    def test_app_exists(self):
        """App klasörü var mı?"""
        self.assertTrue(os.path.isdir('app'))
    
    def test_static_exists(self):
        """Static klasörü var mı?"""
        self.assertTrue(os.path.isdir('static'))
    
    def test_templates_exists(self):
        """Templates klasörü var mı?"""
        self.assertTrue(os.path.isdir('templates'))
    
    def test_requirements_exists(self):
        """requirements.txt var mı?"""
        self.assertTrue(os.path.exists('requirements.txt'))
    
    def test_main_py_exists(self):
        """main.py var mı?"""
        self.assertTrue(os.path.exists('main.py'))
    
    def test_html_template_exists(self):
        """HTML template var mı?"""
        self.assertTrue(os.path.exists('templates/index.html'))
    
    def test_css_exists(self):
        """CSS dosyası var mı?"""
        self.assertTrue(os.path.exists('static/style.css'))
    
    def test_js_exists(self):
        """JavaScript dosyası var mı?"""
        self.assertTrue(os.path.exists('static/script.js'))


class TestImports(unittest.TestCase):
    """Import testleri"""
    
    def test_flask_import(self):
        """Flask import edilebilir mi?"""
        try:
            from flask import Flask
            self.assertIsNotNone(Flask)
        except ImportError:
            self.fail("Flask kütüphanesi kurulu değil. 'pip install -r requirements.txt' çalıştır")
    
    def test_telethon_import(self):
        """Telethon import edilebilir mi?"""
        try:
            from telethon import TelegramClient
            self.assertIsNotNone(TelegramClient)
        except ImportError:
            self.fail("Telethon kütüphanesi kurulu değil. 'pip install -r requirements.txt' çalıştır")


class TestTelegramHandler(unittest.TestCase):
    """Telegram Handler testleri"""
    
    def test_handler_import(self):
        """Telegram handler import edilebilir mi?"""
        try:
            from app.telegram_handler import TelegramHandler
            self.assertIsNotNone(TelegramHandler)
        except ImportError as e:
            self.fail(f"Handler import hatası: {e}")
    
    def test_handler_instance(self):
        """Handler örneği oluşturulabilir mi?"""
        try:
            from app.telegram_handler import TelegramHandler
            handler = TelegramHandler()
            self.assertIsNotNone(handler)
            self.assertFalse(handler.is_connected)
        except Exception as e:
            self.fail(f"Handler oluşturma hatası: {e}")


class TestFlaskApp(unittest.TestCase):
    """Flask uygulaması testleri"""
    
    def test_app_import(self):
        """App import edilebilir mi?"""
        try:
            from main import app
            self.assertIsNotNone(app)
        except ImportError as e:
            self.fail(f"App import hatası: {e}")
    
    def test_app_routes(self):
        """Routes tanımlandı mı?"""
        try:
            from main import app
            # Rotaları kontrol et
            routes = [rule.rule for rule in app.url_map.iter_rules()]
            self.assertIn('/', routes)
            self.assertIn('/api/connect', routes)
            self.assertIn('/api/upload', routes)
            self.assertIn('/api/start-adding', routes)
        except Exception as e:
            self.fail(f"Routes test hatası: {e}")


if __name__ == '__main__':
    print("=" * 50)
    print("Telegram Toplu Üye Ekleme - Test Paketi")
    print("=" * 50)
    print()
    
    unittest.main(verbosity=2)
