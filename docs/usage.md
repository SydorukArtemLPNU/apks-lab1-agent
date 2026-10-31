# Використання застосунку hello_app

## Вимоги

- Python ≥ 3.10 (`python3 --version`, на Windows — `python --version` або `py -3 --version`).
- Git. Глобально нічого не встановлюється: усі залежності — у локальному `.venv`.

## Структура

```
src/hello_app/__init__.py   # версія пакета
src/hello_app/core.py       # greet(name), add(a, b) — чисті функції
src/hello_app/__main__.py   # main(argv): CLI з аргументом --name
tests/test_core.py          # test_BasicAddition, test_greet_*
tests/test_main.py          # перевірка виводу main()
requirements.txt            # runtime-залежності (немає)
requirements-dev.txt        # pytest, pyinstaller, pyyaml
pytest.ini                  # pythonpath = src, testpaths = tests
run.sh / run.bat            # запуск з вихідних кодів
ci.sh / ci.bat              # повний цикл: venv → залежності → тести → exe → smoke test
.github/workflows/ci.yml    # GitHub Actions: Windows, Linux, macOS
```

## Запуск з вихідних кодів

```bash
./run.sh                 # Hello, World!
./run.sh --name Lab      # Hello, Lab!
```

Windows: `run.bat`, `run.bat --name Lab`.

## Збірка і тести

```bash
./ci.sh                  # Linux / macOS
```

```bat
ci.bat                   :: Windows
```

Скрипт по черзі виконує кроки (кожен з заголовком `==> step: ...`):

1. перехід у корінь проєкту;
2. вибір інтерпретатора: змінна `PYTHON`, інакше `python3`, інакше `python`;
3. створення `.venv`, якщо його немає (повторний запуск його перевикористовує);
4. `pip install -r requirements-dev.txt` всередині `.venv`;
5. `pytest -v --junitxml=reports/junit.xml`;
6. видалення старого `dist/` і збірка PyInstaller `--onefile` → `dist/hello` (`dist\hello.exe`);
7. smoke test: виконуваний файл має надрукувати `Hello, World!`;
8. `==> CI OK` — успіх. Будь-яка помилка зупиняє скрипт з ненульовим кодом.

Результати (ігноруються Git): `.venv/`, `build/`, `dist/hello`, `reports/junit.xml`.

Інший інтерпретатор: `PYTHON=python3.12 ./ci.sh`.

## Лише тести

```bash
.venv/bin/python -m pytest -v          # Windows: .venv\Scripts\python.exe -m pytest -v
```

## CI (GitHub Actions)

`.github/workflows/ci.yml` запускається на `push` і `pull_request` у `develop`/`master`
та вручну (`workflow_dispatch`). Одна job `build-test` з матрицею
`ubuntu-latest`, `windows-latest`, `macos-latest` лише викликає `ci.sh` / `ci.bat`,
тому локальний і CI-запуск ідентичні. Артефакт `hello-<os>` містить `dist/` і
`reports/junit.xml`.

## Перевірка агентом

```bash
python3 tools/check.py            # повна перевірка (включно зі збіркою)
python3 tools/check.py --static   # без запуску ci.sh
```

## Типові проблеми

| Симптом | Причина | Рішення |
|---------|---------|---------|
| `ModuleNotFoundError: No module named 'hello_app'` | `src` не в `PYTHONPATH` | запускати через `run.sh`/`run.bat` або `PYTHONPATH=src` |
| `./ci.sh: Permission denied` | втрачено біт виконання | `git update-index --chmod=+x ci.sh run.sh` |
| `ImportError: attempted relative import` у exe | відносний імпорт у `__main__.py` | лише `from hello_app.core import greet` |
