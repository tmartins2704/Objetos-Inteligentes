# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pandas as pd
from configs import BQ_DATASET, BQ_TABLE, PROJECT_ID
from google.cloud import bigquery
from utils_vertex import get_text_response

client = bigquery.Client()


def run_query(sql: str) -> pd.DataFrame:
    try:
        result_query = client.query(sql)
        result_query.result()
    except Exception as e:
        print("Error running the query: {}".format(e))
        return None
    return result_query.to_dataframe()


def get_table_schema(project_id: str, dataset_id: str, table_id: str) -> pd.DataFrame:
    client = bigquery.Client(project_id)
    dataset = client.dataset(dataset_id)
    table = dataset.table(table_id)
    table = client.get_table(table)
    schema = table.schema

    rows = []
    for field in schema:
        rows.append(
            {
                "column_name": field.name,
                "column_type": field.field_type,
                "column_description": field.description,
            }
        )

    return json.dumps(rows)


schema = get_table_schema(PROJECT_ID, BQ_DATASET, BQ_TABLE)

def get_answer(question: str) -> dict:
    with open("./prompts/table_to_text.txt", "r") as f:
        response_prompt = f.read()

    with open("./prompts/text_to_sql.txt", "r") as f:
        sql_prompt = f.read()

    table_path = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    sql_prompt = sql_prompt.format(schema, table_path, question)
    sql = get_text_response(sql_prompt)
    sql = sql.replace("```sql", "").replace("```", "").replace('"""', "")

    df = run_query(sql)
    response_prompt = response_prompt.format(sql, df, question)
    final_response = get_text_response(response_prompt)
    sql = f"```sql\n{sql}\n```"
    return {"table": df, "response": final_response, "query": sql}
