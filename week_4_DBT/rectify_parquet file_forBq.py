
#pip install pandas pyarrow fastparquet


import pandas as pd

for i in range(1, 13):  # Loop from 1 to 12
    file_path = rf"your_parquet_path\nyc\fhv_2019-{i:02d}.parquet"
    output_path = rf"your_parquet_path\nyc\fhv_2019-{i:02d}_fixed.parquet"
    
    # Load the Parquet file
    df = pd.read_parquet(file_path)

    # Convert columns to float
    df["PUlocationID"] = df["PUlocationID"].astype(float)
    df["DOlocationID"] = df["DOlocationID"].astype(float)
    df["SR_Flag"] = df["SR_Flag"].astype(float)

    # Save back as a Parquet file
    df.to_parquet(output_path, engine="pyarrow")

    print(f"Processed: {file_path} → {output_path}")  # Confirmation message
