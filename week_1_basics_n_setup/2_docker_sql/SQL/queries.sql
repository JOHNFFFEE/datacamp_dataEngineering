--q3

SELECT 
    COUNT(*) AS trip_count,
    CASE 
        WHEN trip_distance <= 1 THEN 'Up to 1 mile'
        WHEN trip_distance > 1 AND trip_distance <= 3 THEN '1-3 miles'
        WHEN trip_distance > 3 AND trip_distance <= 7 THEN '3-7 miles'
        WHEN trip_distance > 7 AND trip_distance <= 10 THEN '7-10 miles'
        ELSE 'Over 10 miles'
    END AS distance_range
FROM green_taxi_data
WHERE (DATE(lpep_pickup_datetime) >= '2019-10-01'
  AND DATE(lpep_pickup_datetime) < '2019-11-01')
  or ( DATE(lpep_dropoff_datetime) >= '2019-10-01'
  AND DATE(lpep_dropoff_datetime) < '2019-11-01' )

  

GROUP BY distance_range
ORDER BY trip_count DESC;



--q4
SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS longest_trip_distance
FROM  green_taxi_data
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY longest_trip_distance DESC
LIMIT 1;


--q5
SELECT 
    SUM(total_amount) AS sum_t,
    gr."PULocationID",
    tz."Zone"
FROM green_taxi_data AS gr
JOIN taxi_zone AS tz
ON  gr."PULocationID" = tz."LocationID"
JOIN taxi_zone AS tz2
ON  gr."DOLocationID" = tz2."LocationID"
WHERE DATE_TRUNC('DAY', lpep_pickup_datetime) = '2019-10-18'
GROUP BY  gr."PULocationID", tz."Zone"
HAVING SUM(total_amount) >= 13000
ORDER BY sum_t DESC;


--q6
SELECT tz."Zone",  max(tip_amount) as max_tip
FROM green_taxi_data gr
JOIN taxi_zone AS tz
ON  gr."DOLocationID" = tz."LocationID"
where gr."PULocationID"=74  --"East Harlem North"
and DATE(lpep_pickup_datetime) between '2019-10-01' and '2019-10-31'
group by tz."Zone"
order by max_tip desc
LIMIT 1;