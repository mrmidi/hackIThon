docker run -d --name pg-hackithon -e POSTGRES_PASSWORD=challenge2022 -e PGDATA=/var/lib/posgresql/data/pgdata -e POSTGRES_DB=hackithon -v /Users/mrmidi/POSTGRES:/var/lib/postgresql/data 
-p 5432:5432 postgres
