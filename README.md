# Цель
Поробовал ради шутки заставить мистраль написать программу по описанию. Запрос был такой:

> Мне нужна программа на рабочем столе которая будет считать сколько времени я отработал. Запускаешь её в ней обратный отсчёт с 8 часов до нуля. Если нужно отойти, то есть кнопка паузы. Если идёт переработка свыше 8 часов обратный отсчёт меняется на прямой. Желательно чтобы были разного цвета в интерфейсе. Каждый клик на кнопку пауза/продолжить фиксируется в sqlite с пометкой действия и таймштампом. В конце дня где-нибудь в базе фиксируется переработка или недоработанные часы. И на скудеющей  рабочий день выходит корректировка (например если прошлый рабочий день была переработка 30 минут, то обратный отсчёт начинается с 7:30, а если наоборот недоработано 40 минут, то отсчёт начинается с 8:40). При том прошлый рабочий день именно день когда была запись с остановкой работы, не обязательно вчера.

Результат положительно удивил. Даже ридми попросил написать. Вот и оно кстати:

# Mistral Work Tracker

## Описание

Mistral Work Tracker — это приложение для отслеживания рабочего времени. Оно позволяет запускать таймер с обратным отсчетом от 8 часов, ставить на паузу и останавливать таймер. Приложение также сохраняет действия (начало, пауза, остановка) в базу данных SQLite и корректирует оставшееся время на следующий день в зависимости от переработки или недоработки.

## Функции

- Обратный отсчет времени от 8 часов.
- Возможность ставить таймер на паузу и продолжать.
- Сохранение действий в базу данных SQLite.
- Корректировка оставшегося времени на следующий день.
- Графический интерфейс с использованием Tkinter.

## Установка

1. Установите необходимые библиотеки:
   ```bash
   pip install pynput
   ```

2. Убедитесь, что у вас установлена библиотека `tkinter`. В большинстве дистрибутивов Python она устанавливается по умолчанию. Если нет, установите её:
   - **Windows и macOS**: Обычно устанавливается вместе с Python.
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get update
     sudo apt-get install python3-tk
     ```
   - **Fedora**:
     ```bash
     sudo dnf install python3-tkinter
     ```
   - **Arch Linux**:
     ```bash
     sudo pacman -S tk
     ```

## Запуск

1. Создайте файл `database.py` и вставьте в него код из [database.py](database.py).
2. Создайте файл `timer.py` и вставьте в него код из [timer.py](timer.py).
3. Создайте файл `interface.py` и вставьте в него код из [interface.py](interface.py).
4. Создайте файл `main.py` и вставьте в него код из [main.py](main.py).
5. Запустите основной файл:
   ```bash
   python main.py
   ```

## Запаковка в исполняемый файл

Для запаковки приложения в исполняемый файл используйте `PyInstaller`:

1. Установите `PyInstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Перейдите в директорию вашего проекта и выполните следующую команду:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. Найдите созданный исполняемый файл в директории `dist`.

## Автор

Этот проект был создан с помощью AI-ассистента [Mistal](https://chat.mistral.ai/chat/) модель Large 2.

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной через [GitHub Issues](https://github.com/lowton/mistral-work-tracket/issues).
