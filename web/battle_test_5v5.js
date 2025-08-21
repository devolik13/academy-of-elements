// web/battle_test_5v5.js

/**
 * Симулятор боя "Линия Сражения" 5 на 5
 *
 * Правила:
 * 1. Две линии по 5 магов.
 * 2. Маги стоят в ячейках, номер ячейки определяет приоритет атаки и первоначальную цель.
 * 3. Инициатор боя (игрок A) делает первый ход одним магом.
 * 4. Затем игроки поочередно атакуют группами по два мага.
 * 5. Маг атакует цель напротив. Если её нет, ищет следующую живую цель, двигаясь влево по линии противника.
 *    Если доходит до начала, продолжает с конца (циклический поиск).
 * 6. Бой идет по раундам, в каждом раунде 6 фаз.
 * 7. Бой заканчивается, когда все маги одной стороны мертвы.
 * 8. Все маги имеют 100 HP и наносят 20 урона.
 */

(function(global) { // Используем IIFE для изоляции области видимости

    /**
     * Представление мага
     * @typedef {Object} Wizard
     * @property {string} id - Уникальный ID мага
     * @property {number} hp - Текущие очки здоровья
     * @property {number} maxHp - Максимальные очки здоровья
     * @property {number} damage - Наносимый урон
     * @property {string} name - Имя мага
     * @property {string} spell - Заклинание мага
     */


    /**
     * Представление игрока
     * @typedef {Object} Player
     * @property {string} id - Уникальный ID игрока
     * @property {string} name - Имя игрока
     * @property {Array<Wizard>} wizards - Массив магов игрока
     */


    /**
     * Состояние боя
     * @typedef {Object} BattleState
     * @property {Player} playerA - Игрок A (инициатор)
     * @property {Player} playerB - Игрок B
     * @property {number} currentRound - Номер текущего раунда
     * @property {number} currentPhase - Номер текущей фазы (1-6)
     * @property {Array<string>} log - Лог событий боя
     */


    /**
     * Инициализирует состояние боя 5 на 5
     * @param {Player} initiator - Игрок, начинающий бой
     * @param {Player} opponent - Второй игрок
     * @returns {BattleState}
     */
    function initializeBattle5v5(initiator, opponent) {
        // Глубокое копирование, чтобы не изменять оригинальные объекты
        const playerA = JSON.parse(JSON.stringify(initiator));
        const playerB = JSON.parse(JSON.stringify(opponent));

        // Определяем, кто из них инициатор
        let trueInitiator, trueOpponent;
        if (playerA.id === initiator.id) {
            trueInitiator = playerA;
            trueOpponent = playerB;
        } else {
            trueInitiator = playerB;
            trueOpponent = playerA;
        }

        return {
            playerA: trueInitiator,
            playerB: trueOpponent,
            currentRound: 1,
            currentPhase: 1,
            log: [`Бой начался! ${trueInitiator.name} атакует первым.`]
        };
    }

    /**
     * Находит цель для мага по правилам "Линии Сражения"
     * @param {Wizard} attacker - Атакующий маг
     * @param {number} attackerIndex - Индекс атакующего мага в своей линии (0-4)
     * @param {Array<Wizard>} opponentWizards - Массив магов противника
     * @returns {{wizard: Wizard, index: number} | null} - Найденная цель и её индекс, или null
     */
    function findTarget5v5(attacker, attackerIndex, opponentWizards) {
        // Первоначальная цель - напротив
        let targetIndex = attackerIndex;

        // Циклический поиск: проверяем 5 позиций, начиная с напротив
        for (let i = 0; i < 5; i++) {
            // Индекс для проверки (идем влево: 0, 4, 3, 2, 1)
            let checkIndex;
            if (i === 0) {
                checkIndex = targetIndex; // Сначала напротив
            } else {
                // Затем влево: (0-1+5)%5=4, (4-1+5)%5=3 и т.д.
                targetIndex = (targetIndex - 1 + 5) % 5;
                checkIndex = targetIndex;
            }

            const potentialTarget = opponentWizards[checkIndex];
            if (potentialTarget && potentialTarget.hp > 0) {
                return { wizard: potentialTarget, index: checkIndex };
            }
        }

        // Если все маги противника мертвы
        return null;
    }

    /**
     * Печатает текущее состояние поля боя в консоль
     * @param {BattleState} state - Текущее состояние боя
     */
    function printBattlefield(state) {
        const { playerA, playerB } = state;

        console.log("\n--- Состояние поля боя ---");

        // Линия магов Игрока A
        let lineA = "A: ";
        for (let i = 0; i < 5; i++) {
            const wizard = playerA.wizards[i];
            const status = wizard.hp > 0 ? `[${wizard.name}]` : `[💀${wizard.name}]`;
            lineA += status.padEnd(8, ' '); // Форматируем ширину ячейки
        }
        console.log(lineA);

        // Линия магов Игрока B
        let lineB = "B: ";
        for (let i = 0; i < 5; i++) {
            const wizard = playerB.wizards[i];
            const status = wizard.hp > 0 ? `[${wizard.name}]` : `[💀${wizard.name}]`;
            lineB += status.padEnd(8, ' ');
        }
        console.log(lineB);

        console.log("--------------------------\n");
    }

    /**
     * Выполняет одну фазу боя 5 на 5
     * @param {BattleState} state - Текущее состояние боя
     * @returns {BattleState} - Обновленное состояние боя
     */
    function executePhase5v5(state) {
        const { playerA, playerB, currentPhase } = state;
        let attacker, defender, attackerWizards, defenderWizards;

        // Определяем, кто атакует в этой фазе
        if (currentPhase === 1) {
            // Фаза 1: Инициатор атакует 1 магом
            attacker = playerA;
            defender = playerB;
            attackerWizards = attacker.wizards.filter(w => w.hp > 0);
            defenderWizards = defender.wizards; // Передаем весь массив для поиска цели
            if (attackerWizards.length > 0) {
                const attackingWizard = attackerWizards[0]; // Первый живой маг
                const attackerIndex = attacker.wizards.findIndex(w => w.id === attackingWizard.id);
                const targetInfo = findTarget5v5(attackingWizard, attackerIndex, defenderWizards);

                if (targetInfo) {
                    targetInfo.wizard.hp -= attackingWizard.damage;
                    state.log.push(`${attacker.name}'s ${attackingWizard.name} атакует ${defender.name}'s ${targetInfo.wizard.name} на ${attackingWizard.damage} урона. (${targetInfo.wizard.name} HP: ${Math.max(targetInfo.wizard.hp, 0)})`);
                    if (targetInfo.wizard.hp <= 0) {
                        state.log.push(`${defender.name}'s ${targetInfo.wizard.name} погибает!`);
                    }
                } else {
                    state.log.push(`${attacker.name}'s ${attackingWizard.name} не может найти цель для атаки.`);
                }
            } else {
                state.log.push(`${attacker.name} не имеет живых магов для атаки в Фазе 1.`);
            }
        } else {
            // Фазы 2, 4, 6: Второй игрок атакует 2 магами
            // Фазы 3, 5: Инициатор атакует 2 магами
            const isOpponentPhase = (currentPhase === 2 || currentPhase === 4 || currentPhase === 6);
            if (isOpponentPhase) {
                attacker = playerB;
                defender = playerA;
            } else {
                attacker = playerA;
                defender = playerB;
            }

            attackerWizards = attacker.wizards.filter(w => w.hp > 0);
            defenderWizards = defender.wizards; // Передаем весь массив для поиска цели

            // Определяем, какие два мага атакуют (по порядку)
            let attackOrderIndex;
            switch (currentPhase) {
                case 2: attackOrderIndex = 0; break; // B1, B2
                case 3: attackOrderIndex = 2; break; // A2, A3
                case 4: attackOrderIndex = 4; break; // B3, B4
                case 5: attackOrderIndex = 6; break; // A4, A5
                case 6: attackOrderIndex = 8; break; // B5, B1 (циклически)
                default: attackOrderIndex = 0;
            }

            let attackers = [];
            // Берем магов по порядку, циклически
            for (let i = 0; i < 2; i++) {
                const wizardIndex = (attackOrderIndex + i) % attackerWizards.length;
                if (attackerWizards[wizardIndex]) {
                    attackers.push(attackerWizards[wizardIndex]);
                }
            }

            // Атака каждого из двух магов
            for (let i = 0; i < attackers.length; i++) {
                const attackingWizard = attackers[i];
                const attackerIndex = attacker.wizards.findIndex(w => w.id === attackingWizard.id);
                const targetInfo = findTarget5v5(attackingWizard, attackerIndex, defenderWizards);

                if (targetInfo) {
                    targetInfo.wizard.hp -= attackingWizard.damage;
                    state.log.push(`${attacker.name}'s ${attackingWizard.name} атакует ${defender.name}'s ${targetInfo.wizard.name} на ${attackingWizard.damage} урона. (${targetInfo.wizard.name} HP: ${Math.max(targetInfo.wizard.hp, 0)})`);
                    if (targetInfo.wizard.hp <= 0) {
                        state.log.push(`${defender.name}'s ${targetInfo.wizard.name} погибает!`);
                    }
                } else {
                    state.log.push(`${attacker.name}'s ${attackingWizard.name} не может найти цель для атаки.`);
                }
            }
            if (attackers.length === 0) {
                const phaseNames = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6"};
                state.log.push(`${attacker.name} не имеет живых магов для атаки в Фазе ${phaseNames[currentPhase]}.`);
            }
        }

        // В конце функции, после всех действий, добавляем визуализацию
        printBattlefield(state); // Печатаем поле после каждой фазы

        // Переход к следующей фазе или раунду
        state.currentPhase++;
        if (state.currentPhase > 6) {
            state.currentPhase = 1;
            state.currentRound++;
            state.log.push(`--- Конец Раунда ${state.currentRound - 1} ---`);
        }

        return state;
    }

    /**
     * Проверяет, закончен ли бой
     * @param {BattleState} state - Текущее состояние боя
     * @returns {{isOver: boolean, winner: Player | null}} - Результат проверки
     */
    function isBattleOver5v5(state) {
        const aAlive = state.playerA.wizards.some(w => w.hp > 0);
        const bAlive = state.playerB.wizards.some(w => w.hp > 0);

        if (!aAlive) {
            return { isOver: true, winner: state.playerB };
        }
        if (!bAlive) {
            return { isOver: true, winner: state.playerA };
        }
        return { isOver: false, winner: null };
    }

    /**
     * Запускает симуляцию боя 5 на 5 до конца
     * @param {Player} initiator - Игрок, начинающий бой
     * @param {Player} opponent - Второй игрок
     * @returns {Object} - Результат боя и лог
     */
    function runBattle5v5(initiator, opponent) {
        let state = initializeBattle5v5(initiator, opponent);
        let result = isBattleOver5v5(state);

        console.log("=== НАЧАЛО БОЯ ===");
        printBattlefield(state); // Печатаем начальное состояние

        while (!result.isOver) {
            state = executePhase5v5(state);
            result = isBattleOver5v5(state);
        }

        state.log.push(`--- Бой окончен! ---`);
        if (result.winner) {
            state.log.push(`Победитель: ${result.winner.name}!`);
        } else {
            state.log.push(`Ничья! Оба игрока потеряли всех магов одновременно.`);
        }

        return {
            winner: result.winner,
            log: state.log,
            finalState: state
        };
    }

    // --- Пример использования для тестирования ---

    // Функция для создания стандартного мага
    function createStandardWizard(id, name) {
        return {
            id: id,
            name: name,
            hp: 100,
            maxHp: 100,
            damage: 20,
            spell: "Искра"
        };
    }

    // Создаем магов для Игрока A
    const playerAWizards = [
        createStandardWizard("A1", "Маг A1"),
        createStandardWizard("A2", "Маг A2"),
        createStandardWizard("A3", "Маг A3"),
        createStandardWizard("A4", "Маг A4"),
        createStandardWizard("A5", "Маг A5")
    ];

    // Создаем магов для Игрока B
    const playerBWizards = [
        createStandardWizard("B1", "Маг B1"),
        createStandardWizard("B2", "Маг B2"),
        createStandardWizard("B3", "Маг B3"),
        createStandardWizard("B4", "Маг B4"),
        createStandardWizard("B5", "Маг B5")
    ];

    // Создаем игроков
    const playerA = {
        id: "playerA",
        name: "Игрок A",
        wizards: playerAWizards
    };

    const playerB = {
        id: "playerB",
        name: "Игрок B",
        wizards: playerBWizards
    };


    /**
     * Функция для запуска одного теста из браузера
     * Вызывается как BattleSim5v5.runSingleTest();
     */
    function runSingleTest() {
        console.log("=== Симуляция боя: Игрок A (5 магов) против Игрок B (5 магов) ===");
        console.log("Все маги имеют 100 HP и наносят 20 урона заклинанием 'Искра'.\n");

        const battleResult = runBattle5v5(playerA, playerB);

        // Выводим лог
        battleResult.log.forEach(entry => console.log(entry));

        // Выводим результат
        console.log("\n" + "=".repeat(50));
        if (battleResult.winner) {
            console.log(`🏆 Победитель: ${battleResult.winner.name}`);
        } else {
            console.log(`🤝 Ничья`);
        }
        console.log("=".repeat(50) + "\n");

        return battleResult.winner ? battleResult.winner.name : "Ничья";
    }

    /**
     * Функция для запуска множественных тестов из браузера
     * Вызывается как BattleSim5v5.runMultipleTests(N);
     */
    function runMultipleTests(numTests = 100) {
        console.log(`=== Запуск ${numTests} симуляций боя ===`);
        let winsA = 0;
        let winsB = 0;
        let draws = 0;

        for (let i = 0; i < numTests; i++) {
            // Меняем инициатора каждую итерацию для более честной статистики
            let initiator, opponent;
            if (i % 2 === 0) {
                initiator = playerA;
                opponent = playerB;
            } else {
                initiator = playerB;
                opponent = playerA;
            }

            const result = runBattle5v5(initiator, opponent);
            if (result.winner) {
                if (result.winner.id === "playerA") {
                    winsA++;
                } else {
                    winsB++;
                }
            } else {
                draws++;
            }
        }

        console.log("\n" + "=".repeat(50));
        console.log("📊 Результаты множественных тестов:");
        console.log(`Игрок A победил: ${winsA} раз (${(winsA / numTests * 100).toFixed(2)}%)`);
        console.log(`Игрок B победил: ${winsB} раз (${(winsB / numTests * 100).toFixed(2)}%)`);
        console.log(`Ничьи: ${draws} раз (${(draws / numTests * 100).toFixed(2)}%)`);
        console.log("=".repeat(50) + "\n");
    }

    // Экспортируем функции в глобальную область видимости
    global.BattleSim5v5 = {
        runSingleTest: runSingleTest,
        runMultipleTests: runMultipleTests
    };

    console.log("✅ Модуль BattleSim5v5 загружен и готов к использованию.");

})(window); // Передаем 'window' как 'global'