# FROM python:3.9.1
# RUN pip install pandas sqlalchemy psycopg2
# WORKDIR /app
# COPY ingest_data.py ingest_data.py
# ENTRYPOINT [ "python", "ingest_data.py" ]



# Use a lightweight Python base image
FROM python:3.9-alpine

# Install system dependencies required for psycopg2 and other libraries
RUN apk add --no-cache gcc musl-dev libpq libpq-dev python3-dev

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python libraries
RUN pip install pandas sqlalchemy psycopg2-binary

# Set the working directory
WORKDIR /app

# Create necessary directories inside the container
RUN mkdir -p /app/files

# Copy the script into the container
COPY ingest_data.py ingest_data.py
#copy csvs - not downloading them
COPY files/green_tripdata_2019-10.csv /app/files/

# Set the default command
ENTRYPOINT [ "python", "ingest_data.py" ]




#  container_name: postgres
#     image: postgres:17-alpine
#     environment:
#       POSTGRES_USER: 'postgres'
#       POSTGRES_PASSWORD: 'postgres'
#       POSTGRES_DB: 'ny_taxi'
#     ports:
#       - '5433:5432'
#     volumes:
#       - vol-pgdata:/var/lib/postgresql/data


# winpty docker run -it \
#     -e POSTGRES_USER=postgres \
#     -e POSTGRES_PASSWORD=postgres \
#     -e POSTGRES_DB=ny_taxi \
#     -v /c/Users/Dori3n/Desktop/datat-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
#     -p 5433:5432 \
#     --network=pg-network \
#     --name=pg-database \
#     postgres:17-alpine


# winpty docker run -it \
#   -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
#   -e PGADMIN_DEFAULT_PASSWORD=root \
#   -p 8080:80 \
#   --network=pg-network \
#   --name=pg-database2 \
#    dpage/pgadmin4


#  winpty docker run -it \
#   --network=pg-network \
#   green_taxi_ingest:v01 \ 
#     --user=postgres \
#     --password=postgres \
#     --host=localhost \
#     --port=5433 \
#     --db=ny_taxi \
#     --table_name=green_taxi_data 



   
