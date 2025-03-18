from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, TableEnvironment, StreamTableEnvironment
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Duration


# Writes aggregated data to PostgreSQL.
def create_events_aggregated_sink(t_env):
    table_name = 'longest_streaks'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
        PULocationID INT,
        DOLocationID INT,
        streak_length BIGINT,
        PRIMARY KEY (PULocationID, DOLocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name

# This function creates a Kafka source table in PyFlink.
def create_events_source_kafka(t_env):
    table_name = "green_trips "
    source_ddl = f"""
        CREATE TABLE {table_name} (
        lpep_pickup_datetime TIMESTAMP(3),
        lpep_dropoff_datetime TIMESTAMP(3),
        PULocationID INT,
        DOLocationID INT,
        passenger_count INT,
        trip_distance DOUBLE,
        tip_amount DOUBLE,
        event_watermark AS lpep_dropoff_datetime,
        WATERMARK for event_watermark as event_watermark - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name


def log_aggregation():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000) # Enable checkpoints every 10 seconds
    env.set_parallelism(3) # Set parallelism to 3

    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    watermark_strategy = (
        WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(5))  #Allows late events up to 5 seconds.
        .with_timestamp_assigner(
            # This lambda is your timestamp assigner:
            #   event -> The data record
            #   timestamp -> The previously assigned (or default) timestamp
            lambda event, timestamp: event[2]  # We treat the second tuple element as the event-time (ms).
        )
    )
    try:
        #This query groups events into 1-minute tumbling windows.
        source_table = create_events_source_kafka(t_env)
        aggregated_table = create_events_aggregated_sink(t_env)

        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
            SELECT
                PULocationID,
                DOLocationID,
                COUNT(*) AS streak_length
            FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(event_watermark), INTERVAL '5' MINUTE)
        )
        GROUP BY PULocationID, DOLocationID;
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))


if __name__ == '__main__':
    log_aggregation()
