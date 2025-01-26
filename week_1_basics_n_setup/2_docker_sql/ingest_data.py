#!/usr/bin/env python
# coding: utf-8

import os
import argparse 
import pandas as pd
# import psycopg2
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    # url= params.url

  
    # csv_name = 'C:/Users/Dori3n/Desktop/datat-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/files/green_tripdata_2019-10.csv'
    csv_name = 'files/green_tripdata_2019-10.csv'

    # os.system(f'wget {url} -O {csv_name}')

#connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

###taxi zone file
    df_zone = pd.read_csv('C:/Users/Dori3n/Desktop/datat-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/files/taxi_zone_lookup.csv')
    df_zone.to_sql(con=engine, name='taxi_zone', if_exists='replace')

    df_iter= pd.read_csv( csv_name, iterator=True, chunksize=5000,  low_memory=False)
    df = next(df_iter)

    #drop the table
    df.head(0).to_sql(con=engine, name=table_name, if_exists='replace', index=False)
    #get table schema
    # print(pd.io.sql.get_schema(df, 'green_taxi_data')  )

    n = 0
    total_rows = 0
#pushing chunks to postgres sql
    while True:
        try:
            n += 1
            start_time = time()
            df = next(df_iter)
            print(f"Processing chunk {n}: {df.shape[0]} rows")
            total_rows += len(df)
            
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(con=engine, name=table_name, if_exists='append', index=False)
            end_time = time()
            print(f"Inserted chunk {n}... took {end_time - start_time:.3f}s. Total rows so far: {total_rows}")
        
        except StopIteration:
            print(f"All chunks processed. Total rows inserted: {total_rows}")
            break
        except Exception as e:
            print(f"Error in chunk {n}: {e}")
            break

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Ingest csv Data to postgres')
    parser.add_argument("--user", help='username for postgres ')
    parser.add_argument("--password", help='password for postgres ')
    parser.add_argument("--host", help='host for postgres ')
    parser.add_argument("--port", help='port for postgres ')
    parser.add_argument("--db", help='db name for postgres ')
    parser.add_argument("--table_name", help='table name where the results will be written ')
    # parser.add_argument("--url", help='url of csv file')

    args = parser.parse_args()
    main(args)


