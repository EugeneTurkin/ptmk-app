# ptmk-app

CLI для взаимодействия с базой данных.

## Установка и запуск

Для установки и запуска необходим Python 3.11.* и Docker.

### Создание виртуального окружения

Прежде чем начать работу, **необходимо** создать и активировать виртуальное окружение.

#### Создание окружения
```
python -m venv .venv
```

#### Активация окружения

Windows
```PowerShell
PS C:\> .venv\Scripts\Activate.ps1
```
```cmd.exe
C:\> .venv\Scripts\activate.bat
```
POSIX
```bash
$ source .venv/bin/activate
```

### Установка зависимостей

```PowerShell
python -m pip install -r requirements.txt
```

### Запуск базы данных в контейнере Docker

```PowerShell
docker compose -f .\envs\docker-compose.yml up -d
```

### Помощь по использованию приложения

```
python app.py -h
```

### Генерация данных

Перед использованием некоторых функций приложения **необходимо** сгенерировать файлы фикстур.
```PowerShell
python app.py 0
```
