/* Telegram Toplu Üye Ekleme - Frontend JavaScript */

// Durum değişkenleri
let isConnected = false;
let uploadedUsernames = [];
let isAddingInProgress = false;
let selectedGroupId = null;
let apiSettings = {
    apiId: null,
    apiHash: null,
    phoneNumber: null
};

const elements = {
    // API Ayarları
    apiIdInput: document.getElementById('apiIdInput'),
    apiHashInput: document.getElementById('apiHashInput'),
    phoneInput: document.getElementById('phoneInput'),
    saveSettingsBtn: document.getElementById('saveSettingsBtn'),
    settingsStatus: document.getElementById('settingsStatus'),
    settingsStatusText: document.getElementById('settingsStatusText'),
    
    // Grup ID girişi
    groupIdInput: document.getElementById('groupIdInput'),
    saveGroupBtn: document.getElementById('saveGroupBtn'),
    groupStatus: document.getElementById('groupStatus'),
    groupStatusText: document.getElementById('groupStatusText'),
    
    connectBtn: document.getElementById('connectBtn'),
    disconnectBtn: document.getElementById('disconnectBtn'),
    connectionStatus: document.getElementById('connectionStatus'),
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadStatus: document.getElementById('uploadStatus'),
    uploadStatusText: document.getElementById('uploadStatusText'),
    userList: document.getElementById('userList'),
    userListContent: document.getElementById('userListContent'),
    userCount: document.getElementById('userCount'),
    startBtn: document.getElementById('startBtn'),
    progressSection: document.getElementById('progressSection'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    successCount: document.getElementById('successCount'),
    errorCount: document.getElementById('errorCount'),
    alreadyCount: document.getElementById('alreadyCount'),
    blockedCount: document.getElementById('blockedCount'),
    resultsList: document.getElementById('resultsList'),
    resultsContent: document.getElementById('resultsContent')
};

// ==================== İlk Yükleme ====================

document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkConnectionStatus();
    loadGroupIdFromStorage();
    loadSettingsFromStorage();
});

// ==================== Event Listeners ====================

function setupEventListeners() {
    // API Ayarları kaydetme
    elements.saveSettingsBtn.addEventListener('click', saveApiSettings);
    elements.apiIdInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') saveApiSettings();
    });
    elements.apiHashInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') saveApiSettings();
    });
    elements.phoneInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') saveApiSettings();
    });
    
    // Grup ID kaydetme
    elements.saveGroupBtn.addEventListener('click', saveGroupId);
    elements.groupIdInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') saveGroupId();
    });
    
    // Bağlantı butonları
    elements.connectBtn.addEventListener('click', connectTelegram);
    elements.disconnectBtn.addEventListener('click', disconnectTelegram);

    // Dosya yükleme
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileUpload);

    // Drag & Drop
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);

    // Eklemeyi başlat
    elements.startBtn.addEventListener('click', startAdding);
}

// ==================== API Ayarları Yönetimi ====================

function saveApiSettings() {
    const apiId = elements.apiIdInput.value.trim();
    const apiHash = elements.apiHashInput.value.trim();
    const phoneNumber = elements.phoneInput.value.trim();
    
    // Validasyon
    if (!apiId) {
        showNotification('✗ Lütfen API ID girin', 'error');
        return;
    }
    if (!apiHash) {
        showNotification('✗ Lütfen API Hash girin', 'error');
        return;
    }
    if (!phoneNumber) {
        showNotification('✗ Lütfen telefon numarası girin', 'error');
        return;
    }
    
    // API ID sayı olmalı
    if (!/^\d+$/.test(apiId)) {
        showNotification('✗ API ID sadece sayılardan oluşmalı', 'error');
        return;
    }
    
    // Telefon +90 ile başlamalı veya 0 ile
    if (!/^\+\d{10,}$/.test(phoneNumber) && !/^0\d{9,}$/.test(phoneNumber)) {
        showNotification('✗ Telefon formatı: +905551234567 veya 05551234567', 'error');
        return;
    }
    
    // Ayarları kaydet
    apiSettings = {
        apiId: apiId,
        apiHash: apiHash,
        phoneNumber: phoneNumber
    };
    
    // LocalStorage'e kaydet
    localStorage.setItem('telegramApiSettings', JSON.stringify(apiSettings));
    
    // UI'ı güncelle
    elements.settingsStatus.style.display = 'inline-flex';
    elements.settingsStatusText.textContent = '✓ API ayarları kaydedildi!';
    
    showNotification('✓ API ayarları kaydedildi!', 'success');
}

function loadSettingsFromStorage() {
    const savedSettings = localStorage.getItem('telegramApiSettings');
    if (savedSettings) {
        try {
            apiSettings = JSON.parse(savedSettings);
            elements.apiIdInput.value = apiSettings.apiId || '';
            elements.apiHashInput.value = apiSettings.apiHash || '';
            elements.phoneInput.value = apiSettings.phoneNumber || '';
            elements.settingsStatus.style.display = 'inline-flex';
            elements.settingsStatusText.textContent = '✓ API ayarları kaydedildi!';
        } catch (e) {
            console.error('Settings load error:', e);
        }
    }
}

// ==================== Grup ID Yönetimi ====================

function saveGroupId() {
    const groupId = elements.groupIdInput.value.trim();
    
    if (!groupId) {
        showNotification('✗ Lütfen bir grup ID girin', 'error');
        return;
    }
    
    // Grup ID validasyonu (sayı olmalı ve başında - olabilir)
    if (!/^-?\d+$/.test(groupId)) {
        showNotification('✗ Geçersiz grup ID formatı. Örnek: -1001234567890', 'error');
        return;
    }
    
    selectedGroupId = groupId;
    
    // LocalStorage'e kaydet
    localStorage.setItem('telegramGroupId', groupId);
    
    // UI'ı güncelle
    elements.groupStatus.style.display = 'inline-flex';
    elements.groupStatusText.textContent = '✓ Grup ID kaydedildi: ' + groupId;
    
    showNotification('✓ Grup ID kaydedildi!', 'success');
}

function loadGroupIdFromStorage() {
    const savedGroupId = localStorage.getItem('telegramGroupId');
    if (savedGroupId) {
        selectedGroupId = savedGroupId;
        elements.groupIdInput.value = savedGroupId;
        elements.groupStatus.style.display = 'inline-flex';
        elements.groupStatusText.textContent = '✓ Grup ID kaydedildi: ' + savedGroupId;
    }
}

// ==================== Bağlantı İşlemleri ====================

async function connectTelegram() {
    try {
        // API ayarları kontrol et
        if (!apiSettings.apiId || !apiSettings.apiHash || !apiSettings.phoneNumber) {
            showNotification('✗ Lütfen önce API ayarlarını kaydediniz', 'error');
            return;
        }
        
        elements.connectBtn.disabled = true;
        elements.connectBtn.innerHTML = '<span class="icon">⏳</span> Bağlanıyor...';

        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                apiId: apiSettings.apiId,
                apiHash: apiSettings.apiHash,
                phoneNumber: apiSettings.phoneNumber
            })
        });

        const data = await response.json();

        if (response.ok) {
            isConnected = true;
            updateConnectionStatus(true);
            showNotification('✓ Telegram\'a başarıyla bağlanıldı!', 'success');
        } else {
            showNotification('✗ ' + data.message, 'error');
        }
    } catch (error) {
        showNotification('✗ Bağlantı hatası: ' + error.message, 'error');
    } finally {
        elements.connectBtn.disabled = false;
        elements.connectBtn.innerHTML = '<span class="icon">🔗</span> Telegram\'a Bağlan';
    }
}

async function disconnectTelegram() {
    try {
        elements.disconnectBtn.disabled = true;
        elements.disconnectBtn.innerHTML = '<span class="icon">⏳</span> Çıkılıyor...';

        const response = await fetch('/api/disconnect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok) {
            isConnected = false;
            updateConnectionStatus(false);
            showNotification('✓ Bağlantı kesildi', 'success');
        } else {
            showNotification('✗ ' + data.message, 'error');
        }
    } catch (error) {
        showNotification('✗ Hata: ' + error.message, 'error');
    } finally {
        elements.disconnectBtn.disabled = false;
        elements.disconnectBtn.innerHTML = '<span class="icon">❌</span> Bağlantıyı Kes';
    }
}

function updateConnectionStatus(connected) {
    if (connected) {
        elements.connectionStatus.classList.remove('disconnected');
        elements.connectionStatus.classList.add('connected');
        elements.connectionStatus.querySelector('.status-text').textContent = 'Bağlı ✓';
        elements.connectBtn.disabled = true;
        elements.disconnectBtn.disabled = false;
    } else {
        elements.connectionStatus.classList.remove('connected');
        elements.connectionStatus.classList.add('disconnected');
        elements.connectionStatus.querySelector('.status-text').textContent = 'Bağlı Değil ✗';
        elements.connectBtn.disabled = false;
        elements.disconnectBtn.disabled = true;
    }
}

function checkConnectionStatus() {
    // Backend'den bağlantı durumunu kontrol et
    // Şimdilik varsayılan olarak bağlı değil
    updateConnectionStatus(false);
}

// ==================== Dosya Yükleme ====================

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        elements.fileInput.files = files;
        handleFileUpload();
    }
}

async function handleFileUpload() {
    if (!isConnected) {
        showNotification('✗ Önce Telegram\'a bağlanınız', 'error');
        elements.fileInput.value = '';
        return;
    }

    const file = elements.fileInput.files[0];
    if (!file) return;

    try {
        elements.uploadStatusText.textContent = '⏳ Dosya yükleniyor...';
        elements.uploadStatus.style.display = 'block';

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            uploadedUsernames = data.usernames;
            elements.uploadStatusText.textContent = `✓ ${data.count} kullanıcı hazır`;
            showUserList(uploadedUsernames);
            elements.startBtn.disabled = false;
            showNotification(`✓ ${data.count} kullanıcı yüklendi!`, 'success');
        } else {
            elements.uploadStatusText.textContent = '✗ ' + data.message;
            showNotification('✗ ' + data.message, 'error');
        }
    } catch (error) {
        elements.uploadStatusText.textContent = '✗ Yükleme hatası';
        showNotification('✗ Hata: ' + error.message, 'error');
    }
}

function showUserList(usernames) {
    elements.userList.style.display = 'block';
    elements.userCount.textContent = usernames.length;

    const html = usernames.slice(0, 50).map(username => 
        `<span class="user-tag">@${username}</span>`
    ).join('');

    elements.userListContent.innerHTML = html + 
        (usernames.length > 50 ? `<span class="user-tag">... +${usernames.length - 50} daha</span>` : '');
}

// ==================== Ekleme İşlemi ====================

async function startAdding() {
    if (!isConnected) {
        showNotification('✗ Telegram bağlantısı koptu', 'error');
        return;
    }

    if (!selectedGroupId) {
        showNotification('✗ Lütfen önce grup ID\'sini kaydediniz', 'error');
        return;
    }

    if (uploadedUsernames.length === 0) {
        showNotification('✗ Kullanıcı listesi boş', 'error');
        return;
    }

    try {
        isAddingInProgress = true;
        elements.startBtn.disabled = true;
        elements.progressSection.style.display = 'block';
        elements.resultsList.style.display = 'none';
        
        // Sayaçları sıfırla
        resetCounters();

        const response = await fetch('/api/start-adding', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                usernames: uploadedUsernames,
                groupId: selectedGroupId
            })
        });

        if (!response.ok) {
            const error = await response.json();
            showNotification('✗ ' + error.message, 'error');
            return;
        }

        // Server-Sent Events stream'ini oku
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const result = JSON.parse(line.substring(6));
                        updateProgress(result);
                    } catch (e) {
                        // JSON parse hatası, yoksay
                    }
                }
            }
        }

        isAddingInProgress = false;
        elements.startBtn.disabled = false;
        showNotification('✓ Ekleme işlemi tamamlandı!', 'success');

    } catch (error) {
        isAddingInProgress = false;
        elements.startBtn.disabled = false;
        showNotification('✗ Hata: ' + error.message, 'error');
    }
}

function updateProgress(result) {
    // Sayaçları güncelle
    const total = result.total;
    const current = result.index;
    const percentage = (current / total) * 100;

    elements.progressFill.style.width = percentage + '%';
    elements.progressText.textContent = `İşleme alındı: ${current}/${total} (${Math.round(percentage)}%)`;

    // Sonuç sayaçlarını güncelle
    switch (result.status) {
        case 'success':
            elements.successCount.textContent = parseInt(elements.successCount.textContent) + 1;
            break;
        case 'already_member':
            elements.alreadyCount.textContent = parseInt(elements.alreadyCount.textContent) + 1;
            break;
        case 'blocked':
            elements.blockedCount.textContent = parseInt(elements.blockedCount.textContent) + 1;
            break;
        case 'error':
            elements.errorCount.textContent = parseInt(elements.errorCount.textContent) + 1;
            break;
    }

    // Sonuç listesine ekle
    addResultItem(result);
}

function addResultItem(result) {
    const statusEmoji = {
        'success': '✓',
        'error': '✗',
        'already_member': '⚠',
        'blocked': '🔒'
    };

    const resultItem = document.createElement('div');
    resultItem.className = `result-item ${result.status}`;
    resultItem.innerHTML = `
        <span class="result-item-status">${statusEmoji[result.status] || '?'}</span>
        <span class="result-item-username">@${result.username}</span>
        <span class="result-item-message">${result.message}</span>
    `;

    // Sonuç listesini göster
    if (elements.resultsList.style.display === 'none') {
        elements.resultsList.style.display = 'block';
    }

    // Yeni sonucu ekle (en üste)
    if (elements.resultsContent.firstChild) {
        elements.resultsContent.insertBefore(resultItem, elements.resultsContent.firstChild);
    } else {
        elements.resultsContent.appendChild(resultItem);
    }

    // Max 100 sonuç göster
    while (elements.resultsContent.children.length > 100) {
        elements.resultsContent.removeChild(elements.resultsContent.lastChild);
    }
}

function resetCounters() {
    elements.successCount.textContent = '0';
    elements.errorCount.textContent = '0';
    elements.alreadyCount.textContent = '0';
    elements.blockedCount.textContent = '0';
    elements.resultsContent.innerHTML = '';
}

// ==================== Yardımcı Fonksiyonlar ====================

function showNotification(message, type = 'info') {
    // Konsola yazdır
    console.log(message);

    // İsteğe bağlı: Toast bildirim (gelecekte eklenebilir)
    // showToast(message, type);
}

// Export fonksiyonları (global scope'a)
window.setupEventListeners = setupEventListeners;
window.connectTelegram = connectTelegram;
window.disconnectTelegram = disconnectTelegram;
window.handleFileUpload = handleFileUpload;
window.startAdding = startAdding;
