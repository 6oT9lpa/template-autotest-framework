# Autotest Framework Template

Шаблон фреймворка для UI-автотестов на Python, `pytest` и `Selenium WebDriver`.

Проект уже содержит базовую архитектуру для разработки автотестов: управление браузером, конфигурацию, загрузку тестовых данных, Page Object, элементы интерфейса, явные ожидания и логирование. Его можно использовать как стартовую основу для нового тестового проекта и постепенно расширять под конкретное приложение.

## Содержание

- [Возможности](#возможности)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Структура проекта](#структура-проекта)
- [Запуск тестов](#запуск-тестов)
- [Как писать тесты](#как-писать-тесты)
- [Page Object](#page-object)
- [Элементы интерфейса](#элементы-интерфейса)
- [Ожидания](#ожидания)
- [Тестовые данные](#тестовые-данные)
- [Логирование](#логирование)
- [Как расширять шаблон](#как-расширять-шаблон)
- [Рекомендации по разработке](#рекомендации-по-разработке)
- [Решение частых проблем](#решение-частых-проблем)

## Возможности

- запуск UI-тестов через `pytest`;
- работа с браузерами `Chrome`, `Edge` и `Firefox`;
- централизованная настройка проекта через `data/config.json`;
- единый объект браузера через `Browser`;
- фабрики браузеров для удобного добавления новых драйверов;
- базовый Page Object слой;
- обертки над Selenium-элементами: `Button`, `Input`, `Text`, `Image`;
- явные ожидания через `Waiter`;
- загрузка тестовых данных из JSON-файлов;
- логирование в консоль и файл;
- smoke-тест для проверки, что основные модули фреймворка импортируются и конфигурация читается корректно.

## Требования

- Python `3.10+`;
- установленный браузер Google Chrome, Microsoft Edge или Mozilla Firefox;
- доступ в интернет при первом запуске, если Selenium Manager будет загружать подходящий драйвер автоматически;
- Windows, Linux или macOS.

Зависимости проекта описаны в [requirements.txt](requirements.txt):

```txt
pytest==9.0.3
selenium==4.43.0
```

## Быстрый старт

### 1. Создать виртуальное окружение

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Проверить настройки

Откройте [data/config.json](data/config.json) и укажите нужный базовый URL и браузер:

```json
{
  "base_url": "https://demoqa.com/",
  "browser": "firefox",
  "implicit_wait": 0,
  "explicit_wait": 10
}
```

### 4. Запустить тесты

```bash
pytest
```

Для подробного вывода:

```bash
pytest -v
```

## Структура проекта

```text
.
├── data/
│   ├── config.json              # Основная конфигурация фреймворка
│   ├── browser_config.json      # Тонкая настройка браузеров
│   └── test_data.json           # Тестовые данные
├── framework/
│   ├── core/
│   │   ├── browser.py           # Единая точка доступа к WebDriver
│   │   ├── browser_factories/   # Фабрики браузеров Chrome/Edge/Firefox
│   │   ├── logger.py            # Настройка логирования
│   │   ├── settings.py          # Загрузка .json
│   │   └── singleton.py         # Singleton metaclass
│   ├── elements/
│   │   ├── base_element.py      # Базовая обертка над Selenium WebElement
│   │   ├── button.py            # Элементы кнопок
│   │   ├── input.py             # Элементы поля ввода
│   │   ├── text.py              # Элементы текста
│   │   ├── image.py             # Элементы картинок
│   │   └── element_factory.py   # Фабрика элементов
│   ├── models/
│   │   ├── browser_config.py    # Модель конфигурации браузеров
│   │   └── config.py            # Модель конфигурации
│   ├── pages/
│   │   └── base_page.py         # Базовый класс Page Object
│   └── utils/
├── tests/
│   ├── conftest.py              # Pytest-фикстуры
│   ├── test_framework_smoke.py  # Smoke-тест фреймворка
├── pytest.ini                   # Настройки pytest
├── requirements.txt             # Python-зависимости
└── README.md
```

Конфигурация читается через `ConfigManager`:

```python
from framework.core.settings import ConfigManager

config = ConfigManager().config
print(config.base_url)
```

## Запуск тестов

Запуск всех тестов:

```bash
pytest
```

Запуск с подробным выводом:

```bash
pytest -v
```

Запуск конкретного файла:

```bash
pytest tests/test_framework_smoke.py
```

Запуск конкретного теста:

```bash
pytest tests/test_framework_smoke.py::test_framework_smoke_imports_and_config
```

Остановиться после первой ошибки:

```bash
pytest -x
```

Показать `print` и вывод логов в консоли:

```bash
pytest -s
```

## Как писать тесты

Фикстура `browser` определена в [tests/conftest.py](tests/conftest.py). Она создает браузер перед тестом и закрывает его после завершения теста:

```python
def test_example(browser):
    browser.get("https://example.com/")
    assert "Example" in browser.title
```

Для тестов через Page Object лучше не работать с Selenium напрямую. Вместо этого тест должен описывать пользовательский сценарий, а детали локаторов и действий должны жить в page-классах:

```python
from framework.core.browser import Browser
from framework.core.settings import ConfigManager


def test_example_page_is_opened(browser):
    Browser().open(ConfigManager().config.base_url)

    page = ExamplePage()

    assert page.is_opened()
```

## Page Object

Все страницы наследуются от `BasePage`. Каждый page-класс должен определить `unique_element` - элемент, по которому можно понять, что нужная страница действительно открыта.

Пример страницы:

```python
from selenium.webdriver.common.by import By

from framework.elements import ElementFactory
from framework.elements.base_element import BaseElement
from framework.pages.base_page import BasePage


class ExamplePage(BasePage):
    title = ElementFactory.text((By.CSS_SELECTOR, "h1"), "Заголовок Example Domain")
    more_info_link = ElementFactory.button((By.CSS_SELECTOR, "a"), "Ссылка More information")

    @property
    def unique_element(self) -> BaseElement:
        return self.title

    def open_more_info(self) -> None:
        self.more_info_link.click()
```

Пример теста для этой страницы:

```python
from framework.core.browser import Browser
from framework.core.settings import ConfigManager


def test_example_page_title(browser):
    Browser().open(ConfigManager().config.base_url)

    page = ExamplePage()

    assert page.is_opened()
    assert page.title.normalized_text() == "Example Domain"
```

## Элементы интерфейса

Элементы находятся в пакете `framework.elements`.

### `BaseElement`

Базовый класс для всех элементов. Умеет:

- искать видимый элемент;
- искать присутствующий в DOM элемент;
- искать кликабельный элемент;
- кликать с повторной попыткой при `StaleElementReferenceException`;
- получать текст;
- получать атрибуты;
- проверять видимость.

Пример:

```python
from selenium.webdriver.common.by import By

from framework.elements import BaseElement


title = BaseElement((By.CSS_SELECTOR, "h1"), "Главный заголовок")

assert title.is_displayed()
assert title.text() == "Example Domain"
```

### `Button`

Элемент для кнопок и кликабельных контролов:

```python
submit_button.click()
assert submit_button.is_enabled()
```

### `Input`

Элемент для полей ввода:

```python
search_input.clear_and_type("selenium")
search_input.press_enter()
```

### `TextElement`

Элемент для текста. Дополнительно умеет возвращать нормализованный текст:

```python
assert message.normalized_text() == "Saved successfully"
```

### `ElementFactory`

Фабрика помогает создавать элементы единообразно:

```python
from selenium.webdriver.common.by import By

from framework.elements import ElementFactory


login = ElementFactory.input((By.ID, "login"), "Поле логина")
submit = ElementFactory.button((By.CSS_SELECTOR, "button[type='submit']"), "Кнопка входа")
title = ElementFactory.text((By.CSS_SELECTOR, "h1"), "Заголовок страницы")
```

## Ожидания

Явные ожидания реализованы в `framework.utils.waiter.Waiter`.

Основные методы:

- `Waiter.visible(locator, timeout=None)` - дождаться видимого элемента;
- `Waiter.clickable(locator, timeout=None)` - дождаться кликабельного элемента;
- `Waiter.present(locator, timeout=None)` - дождаться присутствия элемента в DOM;
- `Waiter.is_visible(locator, timeout=None)` - вернуть `True` или `False` вместо исключения;
- `Waiter.until(condition, timeout=None)` - выполнить произвольное ожидание Selenium.

Если `timeout` не передан, используется `explicit_wait` из [data/config.json](data/config.json).

Пример:

```python
from selenium.webdriver.common.by import By

from framework.utils.waiter import Waiter


loader = (By.CSS_SELECTOR, ".loader")
assert Waiter.is_visible(loader, timeout=3)
```

## Тестовые данные

Тестовые данные хранятся в [data/test_data.json](data/test_data.json).

Пример:

```json
{
  "user": {
    "email": "user@example.com",
    "password": "password"
  }
}
```

Получить данные можно через `TestDataManager`:

```python
from framework.core.settings import TestDataManager


test_data = TestDataManager()
email = test_data.get("user")["email"]
```

`JsonDataLoader` кэширует прочитанные JSON-файлы, поэтому повторные обращения не читают файл с диска заново.

## Логирование

Логирование настраивается в `framework.core.logger` и использует стандартный модуль Python `logging`.

По умолчанию логи:

- выводятся в консоль;
- записываются в `logs/framework.log`;
- ротируются при достижении размера `max_bytes`;
- не попадают в git, потому что папка `logs/` добавлена в [.gitignore](.gitignore).

Пример строки в логе:

```text
2026-04-28 15:45:00 | INFO     | tests | [test_framework_smoke.py:7] Test started: Smoke Framework
```

## Как расширять шаблон

### Добавить новую страницу

1. Создайте файл в `framework/pages/` или в отдельном пакете страниц вашего проекта.
2. Наследуйте класс от `BasePage`.
3. Опишите локаторы через `ElementFactory`.
4. Реализуйте `unique_element`.
5. Добавьте методы, отражающие действия пользователя на странице.

### Добавить новый тип элемента

1. Создайте класс в `framework/elements/`.
2. Унаследуйте его от `BaseElement`.
3. Добавьте методы, специфичные для элемента.
4. При необходимости добавьте метод создания в `ElementFactory`.
5. Экспортируйте класс в `framework/elements/__init__.py`.

Пример:

```python
from framework.elements.base_element import BaseElement


class Checkbox(BaseElement):
    def check(self) -> None:
        if not self.find_element().is_selected():
            self.click()

    def uncheck(self) -> None:
        if self.find_element().is_selected():
            self.click()
```

### Добавить новый браузер

1. Создайте новый файл фабрики в `framework/core/browser_factories/`.
2. Унаследуйте его от `DriverFactory`.
3. Реализуйте метод `create`.
4. Зарегистрируйте фабрику в `BrowserFactory._factories` в `framework/core/browser_factories/browser_factory.py`.
5. Укажите имя браузера в `data/config.json`.

### Добавить новые тестовые данные

Для простых данных можно расширять `data/test_data.json`. Если проект растет, лучше разделить данные по нескольким JSON-файлам и добавить отдельный менеджер или метод загрузки.

## Рекомендации по разработке

- Держите тесты короткими: сценарий должен читаться как пользовательская история.
- Не размещайте локаторы в тестах. Локаторы должны жить в Page Object или элементах.
- Используйте явные ожидания вместо `time.sleep`.
- Оставляйте `implicit_wait` равным `0`, если нет осознанной причины менять его.
- Называйте элементы по смыслу: `"Кнопка входа"`, `"Поле email"`, `"Заголовок профиля"`.
- Не смешивайте проверки бизнес-логики и технические детали Selenium в одном тесте.
- Выносите повторяющиеся пользовательские действия в методы страниц.
- Храните чувствительные данные вне репозитория: в переменных окружения, секретах CI или локальных `.env`-файлах.
- Добавляйте smoke-тесты на ключевые модули фреймворка после расширения архитектуры.

## Решение частых проблем

### `Unsupported browser`

Проверьте значение `browser` в [data/config.json](data/config.json). Сейчас доступны:

```json
"browser": "chrome"
```

или:

```json
"browser": "edge"
```

или:

```json
"browser": "firefox"
```

### Браузер не запускается

Проверьте, что нужный браузер установлен в системе. Также убедитесь, что версия Selenium актуальна и у процесса есть доступ к загрузке драйвера через Selenium Manager.

### Элемент не находится

Проверьте:

- корректность локатора;
- открыта ли нужная страница;
- не находится ли элемент внутри `iframe`;
- достаточно ли значения `explicit_wait`;
- не появляется ли элемент только после дополнительного пользовательского действия.

### Тесты запускаются не из той папки

В [pytest.ini](pytest.ini) уже указано:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

Запускайте `pytest` из корня проекта, где находится `pytest.ini`.

### Логи не появляются

Проверьте настройки блока `logging` в [data/config.json](data/config.json). Если блок отсутствует, используются значения по умолчанию. Логи пишутся в `logs/framework.log`, а папка создается автоматически.

## Минимальный сценарий развития проекта

1. Настроить `base_url` и нужный браузер в `data/config.json`.
2. Создать page-классы для основных страниц приложения.
3. Описать элементы через `ElementFactory`.
4. Добавить тестовые данные в `data/test_data.json`.
5. Написать первые smoke-тесты пользовательских сценариев.
6. Постепенно расширять элементы, утилиты и фикстуры под реальные потребности проекта.
