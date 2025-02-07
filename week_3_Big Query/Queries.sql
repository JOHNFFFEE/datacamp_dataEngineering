--load data to external table  (remains in buckets unsing +Add)
--then querying it
SELECT count(*) FROM `promptgen.nyc_yellow_taxi_2024.yellow_taxi` ;  --20332093


-- create non partioned table from external table
create or replace table `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` as 
select * from `promptgen.nyc_yellow_taxi_2024.yellow_taxi`  ;

--count rows count from regular table
SELECT count(*) FROM `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi`  --20332093

--estimations on tables
select distinct PULocationID from `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` ;  --155mb
select distinct PULocationID from `promptgen.nyc_yellow_taxi_2024.yellow_taxi` ;    --0b

select PULocationID from `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` ;  --155.12mb
select PULocationID,DOLocationID  from `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` ;  --310.24mb

select count(*) from `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` 
where fare_amount = 0;  --8333 


--non partitioned table
select distinct VendorID
from `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi` 
where tpep_dropoff_datetime between  '2024-03-01' and '2024-03-15' ; --estimated 310.24mb


--partitioned table
CREATE OR REPLACE TABLE `promptgen.nyc_yellow_taxi_2024.optimized_taxi_data`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `promptgen.nyc_yellow_taxi_2024.yellow_taxi`;

--partitioned table
select distinct VendorID
from `promptgen.nyc_yellow_taxi_2024.optimized_taxi_data`
where tpep_dropoff_datetime between  '2024-03-01' and '2024-03-15' ; --estimated 26.84mb, much faster than regular tables


SELECT count(*) from  `promptgen.nyc_yellow_taxi_2024.regular_yellow_taxi`  --0mb
--BigQuery does not scan the entire table.Instead, it reads metadata (precomputed row counts), which is extremely efficient.