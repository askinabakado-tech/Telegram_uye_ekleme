"""
Telegram Toplu Üye Ekleme Paneli
Flask Backend
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import asyncio
import os
import threading
from config import SECRET_KEY, HOST, PORT, DEBUG
from app.telegram_handler import TelegramHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Uploads klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Telegram handler
telegram_handler = None
loop = asyncio.new_event_loop()

def init_telegram():
    """Telegram handler'ı başlat"""
    global telegram_handler
    if telegram_handler is None:
        telegram_handler = TelegramHandler()


@app.route('/', methods=['GET'])
def index():
    """Ana sayfa"""
    return render_template('index.html')


@app.route('/api/connect', methods=['POST'])
def connect_telegram():
    """Telegram'a bağlan"""
    global telegram_handler, loop
    
    try:
        data = request.get_json()
        api_id = data.get('apiId')
        api_hash = data.get('apiHash')
        phone_number = data.get('phoneNumber')
        
        if not api_id or not api_hash or not phone_number:
            return jsonify({
                'success': False,
                'message': 'API bilgileri eksik'
            }), 400
        
        init_telegram()
        
        # API bilgilerini handler'a ilet
        telegram_handler.set_credentials(api_id, api_hash, phone_number)
        
        # Telegram'a bağlan (async işlemi threadsafe yap)
        def connect():
            return loop.run_until_complete(telegram_handler.start_client())
        
        thread = threading.Thread(target=connect)
        thread.start()
        thread.join(timeout=30)
        
        if telegram_handler.is_connected:
            return jsonify({
                'success': True,
                'message': 'Telegram\'a bağlanıldı'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Telegram bağlantı başarısız. API bilgilerini kontrol edin.'
            }), 400
    
    except Exception as e:
        logger.error(f"Bağlantı hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/disconnect', methods=['POST'])
def disconnect_telegram():
    """Telegram'dan çıkış"""
    global telegram_handler, loop
    
    try:
        if telegram_handler and telegram_handler.is_connected:
            def disconnect():
                return loop.run_until_complete(telegram_handler.stop_client())
            
            thread = threading.Thread(target=disconnect)
            thread.start()
            thread.join(timeout=10)
        
        return jsonify({
            'success': True,
            'message': 'Bağlantı kesildi'
        })
    
    except Exception as e:
        logger.error(f"Çıkış hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Dosya yükle ve eklemeyi başlat"""
    global telegram_handler, loop
    
    try:
        if not telegram_handler or not telegram_handler.is_connected:
            return jsonify({
                'success': False,
                'message': 'Önce Telegram\'a bağlanınız'
            }), 400
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Dosya seçilmedi'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Dosya seçilmedi'
            }), 400
        
        # Dosya uzantısı kontrol et
        if not (file.filename.endswith('.txt') or 
                file.filename.endswith('.csv') or 
                file.filename.endswith('.xlsx')):
            return jsonify({
                'success': False,
                'message': 'Sadece TXT, CSV veya XLSX dosyaları desteklenir'
            }), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Kullanıcı adlarını oku
        usernames = read_usernames_from_file(filepath)
        
        if not usernames:
            return jsonify({
                'success': False,
                'message': 'Dosyada geçerli kullanıcı adı bulunamadı'
            }), 400
        
        logger.info(f"✓ {len(usernames)} kullanıcı bulundu")
        
        return jsonify({
            'success': True,
            'message': f'{len(usernames)} kullanıcı hazır',
            'count': len(usernames),
            'usernames': usernames
        })
    
    except Exception as e:
        logger.error(f"Dosya yükleme hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


@app.route('/api/start-adding', methods=['POST'])
def start_adding():
    """Toplu eklemeyi başlat"""
    global telegram_handler, loop
    
    try:
        data = request.get_json()
        usernames = data.get('usernames', [])
        group_id = data.get('groupId')
        
        if not usernames:
            return jsonify({
                'success': False,
                'message': 'Kullanıcı listesi boş'
            }), 400
        
        if not group_id:
            return jsonify({
                'success': False,
                'message': 'Grup ID belirtilmedi'
            }), 400
        
        if not telegram_handler or not telegram_handler.is_connected:
            return jsonify({
                'success': False,
                'message': 'Telegram bağlantı koptu'
            }), 400
        
        # Grup ID'sini handler'a ilet
        telegram_handler.target_group_id = int(group_id)
        
        # Async işlemi başlat
        async def add_users():
            results = []
            async for result in telegram_handler.add_users_bulk(usernames):
                results.append(result)
                yield f"data: {result}\n\n"
            
            return results
        
        # Generator döndür (Server-Sent Events)
        return stream_response(add_users())
    
    except Exception as e:
        logger.error(f"Ekleme hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 400


def stream_response(generator):
    """Server-Sent Events yanıtı oluştur"""
    def generate():
        for item in generator:
            yield str(item) + '\n'
    
    return app.response_class(generate(), mimetype='text/event-stream')


def read_usernames_from_file(filepath):
    """Dosyadan kullanıcı adlarını oku"""
    usernames = []
    
    try:
        # CSV veya XLSX için
        if filepath.endswith('.csv'):
            import csv
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        # İlk kolon kullanıcı adı
                        username = row[0].strip().lstrip('@').lower()
                        if username:
                            usernames.append(username)
        
        elif filepath.endswith('.xlsx'):
            import openpyxl
            wb = openpyxl.load_workbook(filepath)
            ws = wb.active
            for row in ws.iter_rows(min_row=1, values_only=True):
                if row and row[0]:
                    username = str(row[0]).strip().lstrip('@').lower()
                    if username:
                        usernames.append(username)
        
        else:  # TXT dosyası
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    username = line.strip().lstrip('@').lower()
                    if username:
                        usernames.append(username)
        
        # Duplikaları kaldır
        usernames = list(dict.fromkeys(usernames))
        
        return usernames
    
    except Exception as e:
        logger.error(f"Dosya okuma hatası: {str(e)}")
        return []


@app.template_filter('tojson_filter')
def tojson_filter(obj):
    """JSON filter"""
    import json
    return json.dumps(obj)


if __name__ == '__main__':
    logger.info("🚀 Telegram Toplu Üye Ekleme Paneli Başlıyor...")
    logger.info(f"📍 http://{HOST}:{PORT}")
    logger.info("⚠  config.py dosyasında API_ID ve API_HASH bilgilerini girin")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
