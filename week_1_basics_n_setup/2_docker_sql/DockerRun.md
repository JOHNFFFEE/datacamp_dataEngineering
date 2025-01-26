//running postgres

winpty docker run -it \
 -e POSTGRES_USER=postgres \
 -e POSTGRES_PASSWORD=postgres \
 -e POSTGRES_DB=ny_taxi \
 -v /c/Users/Dori3n/Desktop/datat-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
 -p 5433:5432 \
 --network=pg-network \
 --name=pg-database \
 postgres:17-alpine

//running pgAdmin

winpty docker run -it \
 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
 -e PGADMIN_DEFAULT_PASSWORD=root \
 -p 8080:80 \
 --network=pg-network \
 --name=pg-database2 \
 dpage/pgadmin4

//updated DockerFile - Together
docker build -t green_taxi_ingest:v01 .

//run the build - -- read csv but need to
winpty docker run -it \
 --network=pg-network \
 -v /c/Users/Dori3n/Desktop/datat-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/files:/app/files \
 green_taxi_ingest:v01 \
 --user postgres \
 --password postgres \
 --host host.docker.internal \
 --port 5433 \
 --db ny_taxi \
 --table_name green_taxi_data

//we can run the docker compose
docker-compose up
docker-compose down
