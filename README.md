# Лабораторна робота №1 — AI-агент для автоматизації розробки та CI/CD

**Дисципліна:** Автоматизоване проєктування комп'ютерних систем
**Студент:** Сидорук Артем Васильович, група КІ-404
**Варіант:** 2 (№20 у списку групи) — Python, venv + скрипт запуску, pytest

## Опис

Репозиторій містить AI-агента `build-engineer` для GitHub Copilot (VS Code),
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
.github/
├── agents/build-engineer.agent.md        # manifest агента
├── prompts/                              # commands
│   ├── git-init.prompt.md
│   ├── create-project.prompt.md
│   ├── create-build.prompt.md
│   ├── create-actions.prompt.md
│   ├── check.prompt.md
│   └── init.prompt.md                    # orchestrator
└── skills/
    ├── project-scaffold/SKILL.md
    ├── build-and-test/SKILL.md
    └── github-actions/SKILL.md
tools/check.py                            # детермінована перевірка для команди check
docs/architecture.md                      # архітектура агента
```

## Запуск агента

1. Відкрити репозиторій (гілка `develop`) у VS Code з розширенням GitHub Copilot.
2. Створити гілку: `git switch -c feature/hello-python`.
3. Відкрити Copilot Chat, вибрати агента **build-engineer**.
4. Виконати оркестратор: `/init` (або окремі команди `/git-init`,
   `/create-project`, `/create-build`, `/create-actions`, `/check`).
5. Переглянути зміни, закомітити, запушити гілку й відкрити PR у `develop`.

Детальніше — [docs/architecture.md](docs/architecture.md).
