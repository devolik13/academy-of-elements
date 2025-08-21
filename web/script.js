// web/script.js
console.log('✅ script.js загружен');

// Проверим, загрузились ли скрипты Firebase
if (typeof firebase === 'undefined') {
    console.error('❌ Ошибка: Не удалось загрузить Firebase');
    document.addEventListener('DOMContentLoaded', function() {
        const factionElement = document.getElementById('faction');
        if (factionElement) {
            factionElement.textContent = 'Ошибка Firebase';
        }
    });
    throw new Error('Firebase not loaded');
}

// Конфигурация Firebase
const firebaseConfig = {
  apiKey: "AIzaSyAHl5EUnVHlIJLqsi_wfT14PkE-NClMtMU",
  authDomain: "academy-of-elements.firebaseapp.com",
  databaseURL: "https://academy-of-elements-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "academy-of-elements",
  storageBucket: "academy-of-elements.firebasestorage.app",
  messagingSenderId: "182622266003",
  appId: "1:182622266003:web:4e9836cffe58eb472c6366",
  measurementId: "G-5V7LG83DS3"
};

// Инициализация Firebase с обработкой ошибок
let database;
try {
    firebase.initializeApp(firebaseConfig);
    database = firebase.database();
    console.log('✅ Firebase инициализирован');
} catch (error) {
    console.error('❌ Ошибка инициализации Firebase:', error);
    document.addEventListener('DOMContentLoaded', function() {
        const factionElement = document.getElementById('faction');
        if (factionElement) {
            factionElement.textContent = 'Ошибка БД';
        }
    });
    throw error;
}

// Получение user_id с улучшенной обработкой
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');

// Глобальные переменные
let userData = null;
let buildingsConfig = {};
let currentModal = null;

// Функция для получения конфигурации зданий
function getBuildingsConfig() {
    return {
        "library": {
            "name": "Библиотека",
            "emoji": "📚",
            "image_url": "/images/library.png",
            "description": "Центр исследований заклинаний.",
            "can_build": false
        },
        "wizard_tower": {
            "name": "Башня магов",
            "emoji": "🧙‍♂️",
            "image_url": "/images/wizard_tower.png",
            "description": "Усиливает магов и позволяет нанимать новых.",
            "can_build": false
        },
        "blessing_tower": {
            "name": "Башня благословений",
            "emoji": "🛐",
            "image_url": "/images/blessing_tower.png",
            "description": "Открывает мощные временные благословения для магов.",
            "can_build": true
        },
        "aom_generator": {
            "name": "Генератор АОМ",
            "emoji": "💎",
            "image_url": "/images/aom_generator.png",
            "description": "Производит кристаллы AOM - основную валюту.",
            "can_build": true
        },
        "pvp_arena": {
            "name": "PvP Арена",
            "emoji": "⚔️",
            "image_url": "/images/pvp_arena.png",
            "description": "Проведение боев 1 на 1 по принципу autochess с рейтингом.",
            "can_build": true
        },
        "defense_tower": {
            "name": "Башня защиты",
            "emoji": "🛡️",
            "image_url": "/images/defense_tower.png",
            "description": "Защищает город, используя изученные заклинания.",
            "can_build": true
        },
        "arcane_lab": {
            "name": "Арканская лаборатория",
            "emoji": "⚗️",
            "image_url": "/images/arcane_lab.png",
            "description": "Ускоряет процесс исследования заклинаний.",
            "can_build": true
        }
    };
}

// Улучшенная функция загрузки данных
async function loadUserData() {
    if (!userId) {
        console.error('User ID not found');
        updateUIWithError('Нет ID пользователя');
        return;
    }
    
    try {
        console.log('📥 Загрузка данных пользователя из Firebase...');
        const snapshot = await database.ref(`users/${userId}`).once('value');
        const data = snapshot.val();
        console.log('✅ Данные пользователя из Firebase:', data);

        if (data) {
            userData = data; // <-- Сохраняем данные в глобальную переменную
            buildingsConfig = getBuildingsConfig(); // <-- Обновляем конфиг
            console.log('✅ Данные пользователя загружены');
            updateUI(); // <-- Обновляем интерфейс
        } else {
            console.error('❌ Пользователь не найден в базе данных');
            updateUIWithError('Пользователь не найден');
        }
    } catch (error) {
        console.error('❌ Ошибка загрузки данных:', error);
        updateUIWithError('Ошибка загрузки данных');
    }
}

// Функция для обновления UI с ошибкой
function updateUIWithError(errorMessage) {
    const factionElement = document.getElementById('faction');
    if (factionElement) {
        factionElement.textContent = errorMessage;
    }
}

// Функция для обновления интерфейса
function updateUI() {
    console.log("updateUI called");
    if (!userData) return;

    // Обновляем фракцию
    const factionElement = document.getElementById('faction');
    console.log("factionElement:", factionElement);
    if (factionElement) {
        factionElement.textContent = userData.faction || 'Неизвестно';
        console.log("faction updated to:", userData.faction);
    }

    // Обновляем сетку зданий
    updateBuildingsGrid();
}

// Обновление сетки зданий (3x3)
function updateBuildingsGrid() {
    const grid = document.getElementById('city-grid');
    if (!grid) {
        console.error('❌ Элемент city-grid не найден в DOM');
        return;
    }

    // Устанавливаем класс для 3x3 сетки
    grid.className = 'grid grid-3x3';
    grid.innerHTML = '';

    // Используем 9 ячеек для 3x3 сетки
    const buildingsGrid = userData.buildings_grid || Array(9).fill(null);

    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.index = i;

        const buildingId = buildingsGrid[i];
        const construction = userData.construction || {};

        // Проверяем, строится ли что-то в этой ячейке
        const isUnderConstruction = construction.active &&
            construction.cell_index != null &&
            parseInt(construction.cell_index) === i &&
            construction.type === 'build';

        if (buildingId) {
            // В ячейке есть здание
            cell.classList.add('built');

            // Получаем информацию о здании из конфигурации
            const buildingConfig = buildingsConfig[buildingId];
            const buildingInfo = userData.buildings[buildingId];

            if (buildingConfig) {
                // Создаем элемент img
                const img = document.createElement('img');
                // Используем image_url, если доступен, иначе fallback на эмодзи
                img.src = buildingConfig.image_url || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
                img.alt = buildingConfig.name;
                img.title = `${buildingConfig.name} (уровень ${buildingInfo?.level || 1})`;
                img.className = 'building-image';
                img.onerror = function() {
                    // Если изображение не загрузилось, показываем эмодзи
                    cell.removeChild(img);
                    cell.textContent = buildingConfig.emoji || '🏛️';
                };

                cell.appendChild(img);

                // Добавляем класс по ID здания для дополнительной стилизации
                cell.classList.add(`building-${buildingId}`);
            } else {
                cell.textContent = '🏛️';
                cell.title = `Здание (${buildingId})`;
            }

            // Добавляем обработчик клика для здания
            cell.addEventListener('click', () => onBuildingClick(cell, buildingId, i));
        } else if (isUnderConstruction) {
            // В ячейке идет постройка
            cell.classList.add('under-construction');
            cell.textContent = '🔨';
            cell.title = 'Идет постройка...';
            cell.classList.add('pulse');
        } else {
            // Пустая ячейка
            cell.classList.add('empty');
            cell.textContent = '+';
            cell.title = 'Пустая ячейка. Кликните, чтобы построить.';

            // Добавляем обработчик клика для пустой ячейки
            cell.addEventListener('click', () => onEmptyCellClick(cell, i));
        }

        grid.appendChild(cell);
    }
}

// Обработчики событий
function onBuildingClick(cell, buildingId, cellIndex) {
    console.log(`🏢 Клик по зданию: ${buildingId} в ячейке ${cellIndex}`);

    // Получаем информацию о здании
    const buildingConfig = buildingsConfig[buildingId];
    const buildingInfo = userData.buildings[buildingId];

    if (!buildingConfig) {
        alert(`Неизвестное здание: ${buildingId}`);
        return;
    }

    // Формируем информацию для отображения
    let infoText = `🏛️ **${buildingConfig.name}**\n`;
    infoText += `📝 ${buildingConfig.description}\n`;
    infoText += `📊 Уровень: ${buildingInfo?.level || 1}\n\n`;

    // Проверяем, можно ли улучшить здание
    const maxLevel = getBuildingMaxLevel(buildingId);
    const currentLevel = buildingInfo?.level || 1;

    if (currentLevel < maxLevel) {
        infoText += `⬆️ Можно улучшить до уровня ${currentLevel + 1}\n`;
        infoText += `Команда в боте: \`/upgrade ${buildingId} ${currentLevel + 1}\``;
    } else {
        infoText += `✅ Здание на максимальном уровне (${maxLevel})`;
    }

    // Показываем информацию
    alert(infoText.replace(/\`/g, ''));
}

function onEmptyCellClick(cell, cellIndex) {
    console.log(`➕ Клик по пустой ячейке: ${cellIndex}`);

    // Формируем список доступных для постройки зданий
    const buildableBuildings = Object.entries(buildingsConfig).filter(
        ([id, data]) => data.can_build !== false
    );

    if (buildableBuildings.length === 0) {
        alert("Нет доступных зданий для постройки.");
        return;
    }

    // Создаем модальное окно с кнопками
    let modalContent = `
        <div style="padding: 15px; max-width: 300px; background: #2c2c3d; border-radius: 10px; color: white;">
            <h3 style="margin-top: 0; color: #7289da;">🏗️ Построить в ячейке ${cellIndex}</h3>
            <p>Выберите здание:</p>
    `;
    
    // Добавляем кнопки для каждого доступного здания
    buildableBuildings.forEach(([id, data], index) => {
        modalContent += `
            <button style="margin: 5px 0; padding: 10px 15px; font-size: 14px; width: 100%; border: none; border-radius: 6px; background: #7289da; color: white; cursor: pointer; transition: background 0.2s;"
                onclick="selectBuildingToBuild('${id}', ${cellIndex})">
                ${data.emoji} ${data.name}
            </button>
        `;
    });
    
    modalContent += `
        <button style="margin: 10px 0 0 0; padding: 8px 15px; font-size: 12px; width: 100%; border: 1px solid #7289da; border-radius: 6px; background: transparent; color: #7289da; cursor: pointer;"
            onclick="closeCurrentModal()">
            Отмена
        </button>
      </div>
    `;
    
    // Отображаем модальное окно
    const modal = document.createElement('div');
    modal.innerHTML = modalContent;
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    modal.style.padding = '20px';
    modal.style.borderRadius = '12px';
    modal.style.zIndex = '1000';
    modal.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.5)';
    
    // Добавляем overlay
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999';
    overlay.onclick = closeCurrentModal;
    
    document.body.appendChild(overlay);
    document.body.appendChild(modal);
    
    // Сохраняем ссылку на модальное окно
    currentModal = { modal, overlay };
}

// Функция для выбора здания
function selectBuildingToBuild(buildingId, cellIndex) {
    console.log(`Пользователь выбрал постройку ${buildingId} в ячейке ${cellIndex}`);
    
    // Закрываем модальное окно
    closeCurrentModal();
    
    // Проверка наличия userId
    if (!userId) {
        alert('❌ Ошибка: Не удалось получить ID пользователя.');
        return;
    }
    
    // Отправляем запрос на постройку здания через API
    fetch('/api/build', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: userId,
            building_id: buildingId,
            cell_index: cellIndex
        })
    })
    .then(response => {
        // Проверяем, является ли ответ JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            // Если не JSON, читаем как текст для отладки
            return response.text().then(text => {
                console.error('Сервер вернул не JSON:', text);
                throw new Error('Сервер вернул неожиданный ответ: ' + text.substring(0, 200));
            });
        }
    })
    .then(data => {
        if (data.success) {
            // Успешно - обновляем отображение города
            alert(`✅ ${data.message}`);
            loadUserData(); // Перезагружаем данные для обновления интерфейса
        } else {
            // Ошибка - показываем сообщение
            alert(`❌ ${data.detail || 'Ошибка при постройке здания'}`);
        }
    })
    .catch(error => {
        console.error('Ошибка при постройке:', error);
        alert(`❌ Ошибка при постройке здания: ${error.message}`);
    });
}

// Функция для закрытия модального окна
function closeCurrentModal() {
    if (currentModal) {
        if (currentModal.overlay && document.body.contains(currentModal.overlay)) {
            document.body.removeChild(currentModal.overlay);
        }
        if (currentModal.modal && document.body.contains(currentModal.modal)) {
            document.body.removeChild(currentModal.modal);
        }
        currentModal = null;
    }
}

// Вспомогательные функции
function getBuildingMaxLevel(buildingId) {
    // В реальной системе нужно получать это из buildings_config
    const maxLevels = {
        "library": 1,
        "wizard_tower": 10,
        "blessing_tower": 5,
        "aom_generator": 20,
        "pvp_arena": 1,
        "defense_tower": 5,
        "arcane_lab": 15
    };
    return maxLevels[buildingId] || 1;
}

// Обработчики кнопок
function onFactionButtonClick() {
    console.log("Кнопка 'Выбор фракции' нажата");
    if (!userData) {
        alert('❌ Данные пользователя не загружены.');
        return;
    }
    
    // Показываем информацию о текущей фракции и команду для смены
    const currentFaction = userData.faction || 'Неизвестно';
    const factionNames = {
        "fire": "🔥 Огонь",
        "water": "💧 Вода", 
        "wind": "🌪️ Ветер",
        "earth": "🌿 Земля"
    };
    const factionDisplay = factionNames[currentFaction] || currentFaction;
    
    alert(
        `🧙‍♂️ Ваша текущая фракция: ${factionDisplay}\n\n` +
        `Для смены фракции используйте команды в Telegram боте:\n` +
        `🔥 /fire - Огонь\n` +
        `💧 /water - Вода\n` +
        `🌪️ /wind - Ветер\n` +
        `🌿 /earth - Земля`
    );
}

function onProfileButtonClick() {
    console.log("Кнопка 'Профиль' нажата");
    if (!userData) {
        alert('❌ Данные пользователя не загружены.');
        return;
    }
    
    // Показываем команду для открытия профиля в Telegram
    alert(
        `📖 Для просмотра профиля используйте команду в Telegram боте:\n\n` +
        `/profile`
    );
}

function onCityButtonClick() {
    console.log("Кнопка 'Город' нажата");
    if (!userData) {
        alert('❌ Данные пользователя не загружены.');
        return;
    }
    
    // Обновляем отображение города
    loadUserData();
    alert('🏰 Город обновлен!');
}

function onUpgradeButtonClick() {
    console.log("Кнопка 'Улучшить здание' нажата");
    if (!userData) {
        alert('❌ Данные пользователя не загружены.');
        return;
    }

    const userBuildings = userData.buildings || {};
    const buildingsList = Object.entries(userBuildings);

    if (buildingsList.length === 0) {
        alert("У вас пока нет построенных зданий для улучшения.");
        return;
    }

    // Создаем модальное окно с кнопками для выбора здания
    let modalContent = `
      <div style="padding: 15px; max-width: 300px; background: #2c2c3d; border-radius: 10px; color: white;">
        <h3 style="margin-top: 0; color: #7289da;">⬆️ Выберите здание для улучшения</h3>
        <p>Выберите здание:</p>
    `;
    
    // Добавляем кнопки для каждого построенного здания
    buildingsList.forEach(([id, data], index) => {
        const buildingConfig = buildingsConfig[id];
        const name = buildingConfig ? buildingConfig.name : id;
        const currentLevel = data.level || 1;
        const emoji = buildingConfig?.emoji || '🏛️';
        
        modalContent += `
          <button style="margin: 5px 0; padding: 10px 15px; font-size: 14px; width: 100%; border: none; border-radius: 6px; background: #7289da; color: white; cursor: pointer; transition: background 0.2s;"
              onclick="selectBuildingToUpgrade('${id}', ${currentLevel})">
            ${emoji} ${name} (уровень ${currentLevel})
          </button>
        `;
    });
    
    modalContent += `
        <button style="margin: 10px 0 0 0; padding: 8px 15px; font-size: 12px; width: 100%; border: 1px solid #7289da; border-radius: 6px; background: transparent; color: #7289da; cursor: pointer;"
            onclick="closeCurrentModal()">
          Отмена
        </button>
      </div>
    `;
    
    // Отображаем модальное окно
    const modal = document.createElement('div');
    modal.innerHTML = modalContent;
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    modal.style.padding = '20px';
    modal.style.borderRadius = '12px';
    modal.style.zIndex = '1000';
    modal.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.5)';
    
    // Добавляем overlay
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999';
    overlay.onclick = closeCurrentModal;
    
    document.body.appendChild(overlay);
    document.body.appendChild(modal);
    
    // Сохраняем ссылку на модальное окно
    currentModal = { modal, overlay };
}

function onHireWizardButtonClick() {
    console.log("Кнопка 'Нанять мага' нажата");
    if (!userData) {
        alert('❌ Данные пользователя не загружены.');
        return;
    }

    const commandText = `/hire_wizard`;
    alert(
        `Для найма нового мага используйте команду в Telegram боте:\n\n${commandText}`
    );
}

// Инициализация
document.addEventListener('DOMContentLoaded', function () {
    console.log('📄 DOM загружен, начинаем инициализацию...');
    
    // Загружаем данные только если есть userId
    if (userId) {
        loadUserData();
    } else {
        updateUIWithError('Откройте через Telegram');
    }
    
    // Добавляем обработчики для кнопок
    const upgradeBtn = document.getElementById('upgrade-btn');
    const hireWizardBtn = document.getElementById('hire-wizard-btn');
    const factionBtn = document.getElementById('faction-btn');
    const profileBtn = document.getElementById('profile-btn');
    const cityBtn = document.getElementById('city-btn');

    if (upgradeBtn) {
        upgradeBtn.addEventListener('click', onUpgradeButtonClick);
    }

    if (hireWizardBtn) {
        hireWizardBtn.addEventListener('click', onHireWizardButtonClick);
    }
    
    if (factionBtn) {
        factionBtn.addEventListener('click', onFactionButtonClick);
    }

    if (profileBtn) {
        profileBtn.addEventListener('click', onProfileButtonClick);
    }

    if (cityBtn) {
        cityBtn.addEventListener('click', onCityButtonClick);
    }
});