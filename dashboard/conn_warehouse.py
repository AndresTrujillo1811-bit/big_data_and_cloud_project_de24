import duckdb
from pathlib import Path

# Fixed path to DuckDB file
FILES_SHARE_PATH = Path("/mnt/data/job_ads.duckdb")

def get_duckdb_connection():
    db_path = FILES_SHARE_PATH # Use the fixed path for Azure
    print(f"🔗 Connecting to DuckDB at: {db_path}")
    db_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists
    con = duckdb.connect(database=str(db_path)) # Connect to the DuckDB database
    return con


def get_job_list(query: str = "SELECT * FROM staging.job_ads"): # Getting job rows 
    con = get_duckdb_connection()
    df = con.execute(query).fetchdf()
    con.close()
    return df
