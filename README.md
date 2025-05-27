
## 📌 О проекте

Этот проект представляет собой API для расчёта бонусов

---

### Что не успел реализовать

Несмотря на общую завершённость базовой логики, некоторые аспекты остались незавершёнными или требуют доработки:
* ❌ **Документация** — не хватает подробной документации по API и бизнес-логике, что усложняет понимание системы.
* ❌ **Добавление правил и стратегий** — нет возможности динамически добавлять новые правила и стратегии через API, с бизнес-логикой их создания и обновления.
* ❌ **Праздники** - обновление данных о праздниках в коллекции `holidays` не реализовано, поэтому необходимо вручную добавлять праздники. Можно использовать сторонние API или библиотеки для автоматического получения актуальных дат.
* ❌ **Тестирование** — не успел покрыть код unit-тестами, хотя их наличие сильно упростило бы отладку и валидацию бизнес-логики.
* ❌ **Линтеры и форматирование** — не добавлены pre-commit хуки с `black`, `ruff` или `flake8` для единообразия стиля.
* ❌ **Docker** — можно доработать `Dockerfile` и `docker-compose` для более тонкой настройки (например, оптимизация сборки, multistage).
* ❌ **Оптимизация запросов к MongoDB** — стоит внедрить индексы и рефакторить работу с коллекциями с учётом реальных объёмов и требований к производительности.

---

### Что получилось хорошо

Тем не менее, были реализованы ключевые аспекты системы, которые обеспечивают гибкость и расширяемость:

* ✅ **Гибкая система правил** — бизнес-правила легко комбинируются, порядок применения задаётся явно, есть возможность их включать/отключать.
* ✅ **Конфигурируемые формулы и условия** — всё задаётся через данные (например, из MongoDB) и может быть изменено без пересборки приложения.
* ✅ **Лёгкое расширение**:

  * Можно **добавить обработчик для кастомных формул** расчета бонуса.
  * Можно **создавать кастомные условия** с любой логикой.
  * Возможна реализация **составных условий** с логическими операторами `AND`, `OR`, `NOT` — архитектура позволяет это легко расширить.

Пример:

```json
{
  "type": "composite",
  "operator": "and",
  "items": [
    {"type": "is_weekend"},
    {"type": "customer_status", "config": {"value": "vip"}}
  ]
}
```
---

## Установка и запуск

### Требования

* Установлены Docker и Docker Compose.

### Настройка переменных окружения

Создайте файл `.env.dev` в корне проекта со следующим содержимым:

```env
MONGO_URI=mongodb://admin:admin@mongo:27017/?authSource=admin
MONGO_DB_NAME=bonus
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin
MONGO_INITDB_AUTH_MECHANISM=SCRAM-SHA-256
```

### Запуск проекта

Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

После запуска сервис будет доступен по адресу:

```
http://localhost:8000/docs
```

---

## Структура данных в MongoDB

При запуске контейнера `init-mongo` база данных автоматически заполняется демонстрационными данными. Ниже приведена структура коллекций.

### Коллекция `rules`

Содержит все правила начисления бонусов. Каждое правило описывает:

* `code` — уникальный код правила
* `name` — человекочитаемое название
* `description` — описание логики
* `type` — тип правила: `base` (базовое) или `modifier` (модификатор)
* `conditions` — список условий применения правила
* `formula` — формула расчёта бонуса

#### Пример: базовое правило начисления

```json
{
  "code": "base_rate",
  "name": "Базовое начисление",
  "description": "1 бонус за каждые $10",
  "type": "base",
  "conditions": [],
  "formula": {
    "type": "fixed_per_amount",
    "config": {
      "per_amount": 10,
      "bonus": 1
    }
  }
}
```

#### Пример: модификатор для выходных и праздников

```json
{
  "code": "holiday_weekend",
  "name": "x2 бонусов в выходные и праздники",
  "type": "modifier",
  "conditions": [
    {
      "type": "holiday_weekend",
      "items": [
        {"type": "is_weekend"}
      ]
    }
  ],
  "formula": {
    "type": "multiplier",
    "config": {
      "multiplier": 2.0
    }
  }
}
```

#### Пример: модификатор для VIP-клиентов

```json
{
  "code": "vip_boost",
  "name": "VIP +40%",
  "type": "modifier",
  "conditions": [
    {
      "type": "customer_status",
      "config": {"value": "vip"}
    }
  ],
  "formula": {
    "type": "percent",
    "config": {
      "percent": 40
    }
  }
}
```

---

### Коллекция `holidays`

Содержит список праздничных дат, которые участвуют в правилах.

#### Пример:

```json
{
  "date": "2025-03-08T00:00:00",
  "name": "Международный женский день"
}
```

---

### Коллекция `strategies`

Определяет порядок применения правил. Каждая стратегия может включать несколько правил, упорядоченных по полю `order`.

#### Пример:

```json
{
  "name": "Default Strategy",
  "description": "Стандартная схема начисления бонусов",
  "enabled": true,
  "is_default": true,
  "rules": [
    {"rule_id": "<base_rate_id>", "order": 1, "enabled": true},
    {"rule_id": "<holiday_bonus_id>", "order": 2, "enabled": true},
    {"rule_id": "<vip_boost_id>", "order": 3, "enabled": true}
  ]
}
```

---

## Добавление пользовательских условий и формул

Система бонусов поддерживает расширение через регистрацию собственных **условий** (`Condition`) и **формул** (`Formula`). Ниже описано, как это сделать.

---

### 🔧 Интерфейсы

#### Условие (`ConditionI`)

Все условия наследуются от `ConditionI`:

```python
from abc import ABC, abstractmethod

class ConditionI(ABC):
    @abstractmethod
    def evaluate(self, context: object) -> bool:
        raise NotImplementedError
```

#### Формула (`FormulaI`)

Все формулы наследуются от `FormulaI`:

```python
from abc import ABC, abstractmethod

class FormulaI(ABC):
    @abstractmethod
    def calculate(self, value: float) -> float:
        raise NotImplementedError
```

---

### 🧩 Пример: добавление нового условия

Чтобы добавить условие, создайте класс, реализующий `ConditionI`, и зарегистрируйте его через декоратор `@condition_registry`.

```python
from app.domain.conditions.condition_context import ConditionContext
from app.domain.conditions.register import condition_registry
from app.interfaces.condition_interface import ConditionI

@condition_registry("customer_status")
class CustomerStatusCondition(ConditionI):
    def __init__(self, value: str):
        self.value = value

    def evaluate(self, context: ConditionContext) -> bool:
        return context.input_data.get("customer_status") == self.value
```

Другие примеры:

* `IsHolidayCondition` — проверка, является ли день праздником
* `IsHolidayWeekendCondition` — проверка на выходной или праздник

---

### 🧮 Пример: добавление новой формулы

Формулы реализуют `FormulaI` и регистрируются через `@formula_registry`.

```python
from app.interfaces import FormulaI
from app.domain.formulas.register import formula_registry

@formula_registry("fixed_per_amount")
class FixedPerAmountFormula(FormulaI):
    def __init__(self, per_amount: float, bonus: float):
        self.per_amount = per_amount
        self.bonus = bonus

    def calculate(self, value: float) -> float:
        if self.per_amount <= 0:
            return 0
        return (value // self.per_amount) * self.bonus
```

Другие примеры:

* `MultiplierFormula` — умножает значение на коэффициент
* `PercentFormula` — добавляет процент от значения

---

### ⚙️ Регистрация происходит автоматически

Благодаря декораторам `@condition_registry` и `@formula_registry`, новые классы будут автоматически добавлены в систему при импорте модуля.

---

### 📁 Где хранить

* Условия: `app/domain/conditions/`
* Формулы: `app/domain/formulas/`
* Реестр: `app/domain/conditions/register.py`, `app/domain/formulas/register.py`

---
