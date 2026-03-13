# Client for Derbit


## 🚀 Тестовое задание

- Клиент для внешнего API для Deribit(https://docs.deribit.com/)

### ✅ Выполненные требования ТЗ:

1. **Клиент для Deribit API**
   - Получение index price для BTC/USD и ETH/USD каждую минуту
   - Сохранение с UNIX timestamp

2. **FastAPI Backend**
   - 3 GET endpoints с обязательным параметром `ticker`
   - Получение всех сохраненных данных по валюте
   - Получение последней цены
   - Фильтрация по дате (формат YYYY-MM-DD)

3. **База данных**
   - PostgreSQL с SQLAlchemy ORM
   - Модель для хранения цен валют

4. **Периодические задачи**
   - Celery для планирования задач
   - Redis как брокер сообщений

## 🛠️ Технологии

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)

## 📁 Структура проекта
```
deribit-api/
├── src/
│ ├── currency/ # Модуль для работы с валютами
│ │ ├── celery_config.py # Конфигурация Celery
│ │ ├── models.py # SQLAlchemy модели
│ │ ├── schemas.py # Pydantic схемы
│ │ ├── router.py # Основной роутер
│ │ └── service.py # Операции с БД
│ ├── main.py # Точка входа FastAPI
│ ├── config.py # Класс для взаимодействия с переменными окружения
│ ├── logger.py # Конфигурация для логирования (logger)
│ ├── utilits.py # Задача celery
│ └── database.py # Настройки БД
├── alembic/ # Миграции БД
│ ├── env.py # Настройка окружения миграций
│ └── script.py.mako № 
├── tests/ # Unit тесты
│ ├── unit/
│ │ └── test_api.py # Файл с тестами
├── .env.example # Шаблон для переменных окружения
├── .gitignore
├── poetry.lock # Конфигурация Poetry
├── pyproject.toml # Зависимости Poetry
└── README.md # Документация
```

## ⚡ Быстрый старт
#### 1. Клонируйте репозиторий, затем войдите в папку проекта
```bash
git clone https://github.com/N1chegons/Deribittask.git
cd Deribittask
```

#### 2. Установите зависимости через Poetry
```bash
poetry install
```

#### 3. Создайте свой .env и измените переменные, исходя из ваших настроек для работы с переменными окружения на основе [.env.example](.env.example). Составляющее файла:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_db
DB_USER=user
DB_PASS=pass

REDIS_URL=redis://localhost:6379/0 < Можете оставить по умолчанию, т.к. запуск будет производиться через Docker с стандартным портом
```

#### 4. Проведите миграции
```bash
alembic revision --autogenerate -m "First Initial"
alembic upgrade head
```

#### 5. Запустите Redis через Docker. Не забудьте запустить Docker Dekstop
```bash
docker run -d -p 6379:6379 --name redis-celery redis:alpine     
```

#### 6. Запустите в отдельном терминале worker celery
```bash
celery -A src.currency.celery_config.celery_app worker --loglevel=info --pool=gevent
```

#### 7. Также в отдельном терминале запустите beat celery
```bash
celery -A src.currency.celery_config.celery_app beat --loglevel=info
```

#### 8. Запустите сервер uvicorn
```bash
uvicorn src.main:app --reload # стандартный запуск
uvicorn src.main:app --reload --port 1000 # если хотите изменить порт 
```



## 📡 API Endpoints
 - Все методы используют GET запросы с обязательным параметром ticker.

### 1. Получение всех данных по валюте
```
GET http://127.0.0.1:8000/ticker/data/?ticker=BTCUSD
```
#### Response:
```
[
  {
    "id": 1,
    "ticker": "BTCUSD",
    "price": 87662.53,
    "timestamp": 1769534255,
    "created_at": "2026-01-27T17:17:36.085877"
  },
  {
    "id": 3,
    "ticker": "BTCUSD",
    "price": 87559.44,
    "timestamp": 1769534311,
    "created_at": "2026-01-27T17:18:31.480640"
  }
]
```

### 2. Получение последней цены
```
GET http://127.0.0.1:8000/ticker/latest_price/?ticker=BTCUSD
```
#### Response:
```
{
  "Последняя цена BTCUSD": 87632.2
}
```

### 3.  Получение цены с фильтром по дате
```
GET http://127.0.0.1:8000/ticker/prices/filtered/?ticker=ETHUSD&date_from=2026-01-27&date_to=2026-01-27
```
#### Параметры:
- date_from (опционально): Начальная дата в формате YYYY-MM-DD
- date_to (опционально): Конечная дата в формате YYYY-MM-DD
- 
#### Response:
```
{
  "Тикер: ": "ETHUSD",
  "Период с: ": "2026-01-27",
  "Период по: ": "2026-01-27",
  "Цена: ": [
    2945.21,
    2942.42,
    2939.98
  ]
}
```

## 🧪 Тестирование
```bash
pytest -s -v
```

## 📝 Design Decisions
#### 1. Архитектура 
Использована модульная архитектура с разделением на слои:
- models.py - SQLAlchemy модели для работы с БД
- schemas.py - Pydantic схемы для валидации данных
- service.py - операции с базой данных
- utilits.py - Celery задачи для фоновых операций

#### 2. Синхронность
- FastAPI для синхронного API
- Request для синхронных HTTP-запросов к Deribit
- Celery с gevent пулом для фоновых задач
- Использую gevent т.к. Celery не поддерживает Windows
- Использую синхронность потому что: Проект не высоконагруженный, первый опыт работы с Celery.

####  3. База данных
- PostgreSQL как основная реляционная БД
- SQLAlchemy с синхронным драйвером psycopg2
- Alembic для управления миграциями

#### 4. Периодические задачи
- Celery Beat для планирования задач
- Redis как брокер сообщений
- Изоляция задач получения цен от основного API

#### 5. Логирование
- Использую logger для логирования API

## 👤 Автор
- Богдан
- GitHub: N1chegons
- Telegram: @Nichegons
- Email: nichegons@gmail.com
