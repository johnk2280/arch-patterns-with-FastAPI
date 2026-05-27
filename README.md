# Architecture Patterns with FastAPI

Практическая реализация архитектурных паттернов из книги [Architecture Patterns with Python](https://www.cosimini.com/) (Harry Percival, Bob Gregory) на Python с использованием **FastAPI**.

## Цель

Построить приложение на FastAPI, следуя паттернам:
- **Domain Model** — богатая доменная модель с бизнес-логикой
- **Repository Pattern** — абстракция над хранением данных
- **Unit of Work** — атомарные транзакции
- **Service Layer** — оркестрация use cases
- **Dependency Injection** через FastAPI

## Стек

- Python 3.14
- FastAPI
- Pydantic v2
- pytest + pytest-asyncio
- Ruff (линтер + форматтер)
- Pyright (type checker, strict mode)
- Polyfactory (фабрики для тестов)

## Структура

```
├── main.py                         # точка входа FastAPI
├── pyproject.toml                  # конфигурация проекта
├── src/
│   ├── domain/
│   │   ├── base.py                 # базовый DomainModel
│   │   └── models/
│   │       ├── __init__.py
│   │       └── batch.py            # модель Batch (партия товара)
│   └── tests/
│       └── unit/domain/
│           └── test_batch.py       # тесты доменной логики
```

## Статус

Проект на начальной стадии. Реализована базовая доменная модель `Batch`.
Предстоит реализовать: `OrderLine`, `OutOfStock`, аллокацию, Repository, Unit of Work, Service Layer и REST API.

## Запуск

```bash
# установка зависимостей
uv sync

# запуск тестов
pytest

# линтинг
ruff check src/

# проверка типов
pyright
```

## Запуск приложения

```bash
fastapi dev main.py
```
