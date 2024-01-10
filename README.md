<p align="center">
      <img src="https://i.ibb.co/p45WGzh/dumbbell-sport-5072-1.png" width="200">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/Python-3.10-blue" alt="License">
   <img src="https://img.shields.io/badge/Aiogram-3.1.1-blueviolet">
   <img src="https://img.shields.io/badge/Version-v1.0-blue" alt="Game Version">
   <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License">
</p>

## About

SportBot v2 for choosing training programs, monitoring the implementation of exercises and keeping statistics.

## Documentation

### Features

* Mark the program as completed
* Navigation menu
* Collection of statistics
* Auth user
* Admin panel

### Commands

`manage.py run-bot` Run bot <br>
`manage.py write-programs <path file>` Write data from a file `.csv` <br>
`manage.py create-user-staff-bot <username> <password>` Create a user with the staff role <br>
`manage.py create-superuser <username> <password>` Create a user with the superuser role <br>

### Installation

1. Create file `.env`

```
# Base
DEBUG=[bool]
CORS_ORIGINS=

# Data base
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
BACKUP_PATH=

# Telegram
BOT_TOKEN=
WEBHOOK_SECRET=
BASE_WEBHOOK_URL=
WEBHOOK_PATH_SECURITY=

# Authentication Backend Admin
SECRET_KEY=
```

2. Creation of virtual environments and install requirements

```bash
poetry install
```

3. Run

Run bot
```bash
python3 manage.py run-bot
```

Run admin
```bash
uvicorn src.wsgi:app --reload
```

## Distribute

- In progress


## Developers

- [Oleksii Martseniuk](https://github.com/OleksiiMartseniuk)

## License
Project SportBot is distributed under the MIT license.
