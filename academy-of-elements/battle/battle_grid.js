// battle_grid.js

/**
 * Инициализация и отрисовка сетки боя
 */
function initializeBattleGrid() {
    const grid = document.getElementById('battleGrid');
    if (!grid) {
        console.error('Элемент battleGrid не найден в DOM');
        return;
    }

    // Очищаем сетку
    grid.innerHTML = '';

    // Создаем 30 ячеек
    for (let i = 1; i <= 30; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.index = i;

        // Определяем тип ячейки и игрока
        let cellType = 'empty';
        let player = '';

        if (i >= 1 && i <= 5) {
            cellType = 'magician';
            player = 'player-a';
            cell.textContent = '🧙‍♂️'; // Эмодзи мага Игрока A
            cell.title = `Маг Игрока A (Позиция ${i})`;
        } else if (i >= 6 && i <= 10) {
            cellType = 'summon';
            player = 'player-a';
            cell.textContent = '🐾'; // Эмодзи существа Игрока A
            cell.title = `Существо Игрока A (Позиция ${i - 5})`;
        } else if (i >= 11 && i <= 15) {
            cellType = 'effect';
            player = 'player-a';
            cell.textContent = '✨'; // Эмодзи эффекта Игрока A
            cell.title = `Эффект Игрока A (Позиция ${i - 10})`;
        } else if (i >= 16 && i <= 20) {
            cellType = 'effect';
            player = 'player-b';
            cell.textContent = '🌟'; // Эмодзи эффекта Игрока B
            cell.title = `Эффект Игрока B (Позиция ${i - 15})`;
        } else if (i >= 21 && i <= 25) {
            cellType = 'summon';
            player = 'player-b';
            cell.textContent = '🐾'; // Эмодзи существа Игрока B
            cell.title = `Существо Игрока B (Позиция ${i - 20})`;
        } else if (i >= 26 && i <= 30) {
            cellType = 'magician';
            player = 'player-b';
            cell.textContent = '🧙‍♀️'; // Эмодзи мага Игрока B
            cell.title = `Маг Игрока B (Позиция ${i - 25})`;
        }

        // Добавляем классы типа и игрока
        cell.classList.add(cellType);
        if (player) {
            cell.classList.add(player);
        }

        // Добавляем обработчик клика (для демонстрации)
        cell.addEventListener('click', () => onCellClick(cell, i, cellType, player));

        grid.appendChild(cell);
    }

    console.log('✅ Сетка боя инициализирована');
}

/**
 * Обработчик клика по ячейке
 * @param {HTMLElement} cell - Элемент ячейки
 * @param {number} index - Номер ячейки (1-30)
 * @param {string} type - Тип ячейки ('magician', 'summon', 'effect', 'empty')
 * @param {string} player - Игрок ('player-a', 'player-b')
 */
function onCellClick(cell, index, type, player) {
    console.log(`Клик по ячейке ${index} (${type}, ${player})`);
    
    // Пример: показать информацию о ячейке
    let info = `Ячейка ${index}\n`;
    info += `Тип: ${type}\n`;
    info += `Игрок: ${player}\n`;
    
    // Можно добавить больше информации в зависимости от типа
    switch(type) {
        case 'magician':
            info += `Это маг игрока ${player === 'player-a' ? 'A' : 'B'}!`;
            break;
        case 'summon':
            info += `Это вызванное существо игрока ${player === 'player-a' ? 'A' : 'B'}!`;
            break;
        case 'effect':
            info += `Это эффект игрока ${player === 'player-a' ? 'A' : 'B'}!`;
            break;
        case 'empty':
            info += `Эта ячейка пуста.`;
            break;
    }
    
    alert(info);
}

// Загрузка и отображение данных при запуске
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM загружен, инициализируем сетку боя...');
    initializeBattleGrid();
});