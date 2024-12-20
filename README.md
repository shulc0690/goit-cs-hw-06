# goit-cs-hw-06
Cтворення вебзастосунку, який взаємодіє з сервером за допомогою сокетів та здатний зберігати інформацію у базі даних MongoDB

Перед початком роботи:
1. Версія **Python: >=3.11**
2. Cтворюємо віртуальне середовище (Python: >=3.11) `.env`: `python -m venv .env`
3. Активуємо (відповідно до своєї ОС): `.env\Scripts\activate`
4. Інсталюємо залежності: `pip install -r requirements.txt`
5. По завершенню роботи деактивовуємо: `.env\Scripts\deactivate`


### Робота з HTTP-сервером:

Створення вебдодатку на Python без використання вебфреймворків.
Робота з маршрутизацією та обробкою статичних ресурсів.

### Робота із Сокетами:

Реалізація простого Socket-сервера для обробки даних.
Використання протоколу UDP або TCP для взаємодії між вебдодатком і сервером.

### Використання Docker:

Створення Docker-контейнера для вебдодатку та Socket-сервера.
Створення Dockerfile та написання docker-compose.yaml для автоматизації розгортання.

### Робота з MongoDB:

Збереження даних у базі даних MongoDB.
Створення записів у форматі, що має значення для реального застосування.