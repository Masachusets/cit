# Учёт техники (Equipment Inventory)

Веб-приложение для учёта и управления оборудованием на предприятии.

## Стек технологий
- Python 3.11+
- Litestar (ASGI web framework)
- SQLAlchemy (ORM)
- advanced-alchemy
- Alembic (миграции)
- HTMX (интерактивность без JS)
- TailwindCSS + DaisyUI (стили)
- Jinja2 (шаблоны)
- SQLite/PostgreSQL (БД)

## Возможности
- CRUD для оборудования
- Привязка к сотруднику или подразделению
- Валидация инвентарного номера
- Модальные формы для создания/редактирования
- Удаление с подтверждением и мгновенным обновлением таблицы
- Поиск, фильтрация, пагинация

## Быстрый старт
1. Клонируй репозиторий:
   ```bash
   git clone ...
   cd ...
   ```
2. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Применяй миграции (создай БД и структуру):
   ```bash
   litestar --app src.app.main:app database make-migrations
   litestar --app src.app.main:app database upgrade
   ```
4. Запусти приложение:
   ```bash
   litestar --app src.app.main:app run  
   # или с hot-reload:
   litestar --app src.app.main:app run   --reload
   ```
5. Открой в браузере: [http://localhost:8000/equipments](http://localhost:8000/equipments)

## Структура проекта
- `src/app/database/models/` — модели SQLAlchemy
- `src/app/domain/equipments/` — сервисы, контроллеры, DTO
- `src/app/templates/` — Jinja2-шаблоны
- `src/app/static/` — стили, JS, статика

## Разработка
- Используй hot-reload: `litestar run --reload`
- Для тестов: `pytest`

## Контакты
Вопросы и баги — в Issues или напрямую автору.
