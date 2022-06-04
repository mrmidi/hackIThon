# hackIThon 2022
Usti-Nad-Labem data visualization hackaton 2022. Django template project with few simple Plotly/Dash apps

## If you want to build this project for some reason:
Docker required for backend DB setup!

1. clone repository: git clone https://github.com/mrmidi/hackIThon.git
2. Go to directory: cd hackIThon
3. Run postgress docker image: docker run -d --name pg-hackithon -e POSTGRES_PASSWORD=challenge2022 -e PGDATA=/var/lib/posgresql/data/pgdata -e POSTGRES_DB=hackithon -v /Users/mrmidi/POSTGRES:/var/lib/postgresql/data -p 5432:5432 postgres
4. Run redis docker image: docker run -d --name redis -p 6379:6389 redis
5. Create virtual envirement: python -m venv venv
6. Activate it: source venv/bin/activate
7. Install python requirements: pip install -r requirements.txt
8. Create database tables: python manage.py makemigrations, python manage.py migrate
9. Run server: python manage.py runserver 0.0.0.0:8000
10. You are amazing! Why did you just did it?! :)

### TODO make docker compose file and docker file for quick auto-deploying
