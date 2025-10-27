import dlt
import requests
import json
from pathlib import Path
import os

# Path for data warehouse in DuckDB
db_path = str(Path(__file__).parents[1] / "duckdb_warehouse/job_ads.duckdb")

# Occupation fields
occupations = ("apaJ_2ja_LuF", "9puE_nYg_crq", "ScKy_FHB_7wT")
params = {"limit": 100, "occupation-field": occupations}
dlt.config["load.truncate_staging_dataset"] = True


# Extract
def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode("utf8"))


@dlt.resource(write_disposition="append")
def jobads_resource(params):
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    limit = params.get("limit", 100)
    offset = 0

    while True:
        page_params = dict(params, offset=offset)
        data = _get_ads(url_for_search, page_params)
        hits = data.get("hits", [])
        if not hits:
            break
        for ad in hits:
            yield ad
        if len(hits) < limit or offset > 1900:
            break
        offset += limit


# Load
def run_pipeline(query, table_name, occupation_fields):
    pipeline = dlt.pipeline(
        pipeline_name="Jobads_big_cloud",
        destination=dlt.destinations.duckdb(db_path),
        dataset_name="staging",
    )

    for occupation_field in occupation_fields:
        params = {"q": query, "limit": 100, "occupation-field": occupation_field}
        load_info = pipeline.run(
            jobads_resource(params=params), table_name=table_name
        )
        print(f"Occupation field: {occupation_field}")
        print(load_info)
        
        
@dlt.source
def jobads_source():
    return jobads_resource(params)        


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    table_name = "job_ads"
    query = ""

    # "Data/IT", "Kultur, media & design", "Hotell,restaurang,storhushåll"
    occupation_fields = ("apaJ_2ja_LuF", "9puE_nYg_crq", "ScKy_FHB_7wT")
    run_pipeline(query, table_name, occupation_fields)
