# Лабораторна робота №1 — AI-агент для автоматизації розробки та CI/CD

**Дисципліна:** Автоматизоване проєктування комп'ютерних систем
**Студент:** Сидорук Артем Васильович, група КІ-404
**Варіант:** 2 (№20 у списку групи) — Python, venv + скрипт запуску, pytest

## Опис

Репозиторій містить AI-агента `build-engineer` для **Claude Code** (CLI),
який з порожнього репозиторію генерує кросплатформний застосунок
**Hello World** на Python, систему складання (venv + `ci.sh`/`ci.bat` +
PyInstaller), юніт-тести pytest і GitHub Actions для Windows, Linux і macOS.

| Гілка        | Вміст |
|--------------|-------|
| `develop`    | лише агент: manifest, skills, commands, `tools/check.py`, документація |
| `feature/hello-python` | результат запуску агента: код, тести, скрипти, CI, журнал AI |
| `master`     | фінальний результат після перевірки та злиття |

## Структура агента

```
CLAUDE.md                                 # імпортує manifest для кожної сесії
.claude/
├── agents/build-engineer.md              # manifest агента (subagent Claude Code)
├── commands/                             # commands (slash-команди)
│   ├── git-init.md
│   ├── create-project.md
│   ├── create-build.md
│   ├── create-actions.md
│   ├── check.md
│   └── init-project.md                   # orchestrator
├── skills/
│   ├── project-scaffold/SKILL.md
│   ├── build-and-test/SKILL.md
│   └── github-actions/SKILL.md
└── settings.json                         # дозволи: заборона push/reset/rebase, читання .env
tools/check.py                            # детермінована перевірка для команди check
docs/architecture.md                      # архітектура агента
```

## Запуск агента

Потрібні: Git, Python ≥ 3.10, [Claude Code](https://docs.claude.com/claude-code) (`claude --version`).

1. Клонувати репозиторій і перейти на `develop`: `git switch develop`.
2. Створити гілку: `git switch -c feature/hello-python`.
3. Запустити Claude Code в корені репозиторію: `claude`.
4. Виконати оркестратор `/init-project` (або окремі команди `/git-init`,
   `/create-project`, `/create-build`, `/create-actions`, `/check`).
   Без інтерактивного режиму: `claude -p "/init-project"`.
5. Переглянути зміни, закомітити, запушити гілку й відкрити PR у `develop`.

`/init` у Claude Code — вбудована команда (генерує `CLAUDE.md`), тому
оркестратор називається `/init-project`.

Детальніше — [docs/architecture.md](docs/architecture.md).

## Project

Застосунок `hello_app` (пакет у `src/hello_app/`) друкує привітання.

| Дія | Linux / macOS | Windows |
|-----|---------------|---------|
| Запуск з вихідних кодів | `./run.sh` → `Hello, World!` | `run.bat` |
| Запуск з аргументом | `./run.sh --name Lab` → `Hello, Lab!` | `run.bat --name Lab` |
| Збірка + тести + exe | `./ci.sh` → `dist/hello` | `ci.bat` → `dist\hello.exe` |

Скрипти самі створюють `.venv` (лише локально, без глобальних пакетів).
Детальна інструкція — [docs/usage.md](docs/usage.md).
