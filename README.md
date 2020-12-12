# Productivity24x7
Repository for the Service Oriented Application Development Project.

**Group ID 15**

## About

We wanted to make a simple API for keeping track of events and tasks in a single place. By adding support for WebHooks and OAuth, we wanted to make our services easily consumable.

## Setting the project

* Run command `git clone https://github.com/ketan-lambat/Productivity24x7` to clone the project locally.
* Create a virtual environment `venv`.
* Activate the virtual environment.
* Install dependencies.

To create virtual environment and install requirements run following commands
```shell script
virtualenv --python 3.8 venv
```

To activate the environment use following commands:

#### Window

```shell script
.\env\Scripts\activate
```
#### Ubuntu/Linux

```shell script
source env/bin/activate
```

Install the dependencies by running:
```bash
pip install -r requirements.txt
```

## Running the server

```shell script
cd productivity24x7
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

You need to run migration commands (1 & 2) every time any Models are updated. (If you are pulling updates from GitHub, then only run second migration command. Hence, anyone making any changes to Models must make migrations and then push to source control.)

## Features

- Support for OAuth2
- Support for JWT
- Support for WebHooks
- GitHub Authentication
- Sync events from Google Calendar

## Models

- **Events**
- **Tasks**
- **Tags**

## Team Members:

1. **Ketan Lambat** (S20180010081)
2. **Sai Kshitij** (S20180010117)
3. **Ram Nad** (S20180010145)
4. **Shardul Gedam** (S20180010161) 
5. **Shikhar Varshney** (S20180010163)
