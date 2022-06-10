# hackIThon 2022
Usti-Nad-Labem data visualization hackaton 2022. Django template project with few simple Plotly/Dash apps

## If you want to build this project for some reason:

1. Add .env file containing:
```
#app settings
DEBUG=1
SECRET_KEY=hackIThon

# database access credentials
ENGINE=django.db.backends.postgresql
DB_NAME=pg-hackithon
POSTGRES_USER=postgres
POSTGRES_PASSWORD=challenge2022
DB_HOST=db
DB_PORT=5432
APP_PORT=8000
```
2. docker-compose build
3. docker-compose up
