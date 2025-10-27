import duckdb
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
load_dotenv(Path(__file__).parents[1] / ".env")

def get_duckdb_connection():
    # Read DUCKDB_PATH from .env or fallback
    db_path = os.getenv("DUCKDB_PATH")

    if not db_path:
        db_path = Path(__file__).parents[1] / "duckdb_warehouse" / "job_ads.duckdb"

    # ✅ Convert Path to string (important!)
    db_path = str(db_path)

    print(f"🔗 Connecting to DuckDB at: {db_path}")

    # ✅ Ensure parent directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # ✅ Connect to the database file
    con = duckdb.connect(database=db_path)
    return con


def get_job_list(query: str = "SELECT * FROM staging.job_ads"):
    con = get_duckdb_connection()
    df = con.execute(query).fetchdf()
    con.close()
    return df
