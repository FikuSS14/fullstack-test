# Fullstack test

Тестовое задание: веб-приложение для управления пользователями с бэкендом на Flask и фронтендом на vanilla JavaScript.

---

## Структура проекта

```
fullstack_test/
├── backend/
│   ├── app.py              # Flask приложение
│   └── requirements.txt    # Зависимости Python
├── frontend/
│   └── index.html          # Фронтенд (Bootstrap + vanilla JS)
└── README.md               # Эта инструкция
```
---

## Быстрый старт

### Установка зависимостей
```bash
cd backend
pip install -r requirements.txt
```
---

### Запуск бэкенда

#### Открыть терминал в папке `backend`

```bash
cd backend
```

#### Создать виртуальное окружение
```bash
Windows:
python -m venv venv
venv\Scripts\activate
```
```bash
Mac / Linux:
python3 -m venv venv
source venv/bin/activate
```
---

#### Запустить сервер
```bash
python app.py
```
---

### Запуск фронтенда

Открыть файл frontend/index.html

### Остановка приложения
Бэкенд: нажмите Ctrl + C в терминале, где запущен Flask.

Фронтенд: просто закройте вкладку браузера.

### Примечания
Бэкенд проверен flake8 и black — соответствует PEP 8.

Валидация email на фронте и бэкенде.

### Скриншоты работы 

Главная страница с таблицей
![Главная страница](screenshots/01_main_page.png)

Модальное окно с деталями пользователя

![Детали пользователя](screenshots/03_main_page.png)

Форма добавления пользователя (открытая)
![Форма добавления](screenshots/04_user_details.png)

Успешное добавление пользователя
![Успешное добавление](screenshots/05_success_add.png)

Ошибка валидации на фронте
![Ошибка валидации email](screenshots/06_validation_error.png)

Ошибка 409 (email уже существует)
![Ошибка дубликат email](screenshots/07_duplicatee_email_error.png)

Поиск/фильтрация по таблице
![Поиск по таблице](screenshots/08_search_filter.png)

Пустой результат поиска
![Пустой результат поиска](screenshots/09_empty_search.png)

Ответ API в браузере (JSON)

![API ответ JSON](screenshots/10_api_json_response.png)

Ошибка 404 (пользователь не найден)

![404 Not Found](screenshots/11_404_error.png)
