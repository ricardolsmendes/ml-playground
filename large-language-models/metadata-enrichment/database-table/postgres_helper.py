import os
from typing import Any, Mapping, Optional

import pandas as pd
from pandas import DataFrame
import sqlalchemy
from sqlalchemy import Engine


class DatabaseHelper:

    def __init__(self):
        self._engine: Optional[Engine] = None

    def connect(self) -> None:
        self._engine = sqlalchemy.create_engine(
            "postgresql+psycopg2://"
            f"{os.getenv('DATABASE_USER')}:"
            f"{os.getenv('DATABASE_PASSWORD')}@"
            f"{os.getenv('DATABASE_HOST')}:"
            f"{os.getenv('DATABASE_PORT')}/"
            f"{os.getenv('DATABASE_NAME')}"
        )

    def disconnect(self) -> None:
        self._engine.dispose()

    def _execute_query(self, query: str, params: Mapping[str, Any] = None) -> None:
        con = self._engine.connect()
        con.execute(sqlalchemy.text(query), params)
        con.commit()
        con.close()

    def _read_query_results(
        self, query: str, params: Mapping[str, Any] = None
    ) -> DataFrame:
        return pd.read_sql_query(sql=query, con=self._engine, params=params)

    def list_tables(self, schema: str) -> DataFrame:
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %(schema)s
        -- ORDER BY table_name;
        ORDER BY RANDOM();
        """
        return self._read_query_results(query, {"schema": schema})

    def get_columns_technical_metadata(self, schema: str, table: str) -> DataFrame:
        query = """
        SELECT column_name, data_type, column_default, is_nullable
        FROM information_schema.columns
        WHERE table_schema = %(schema)s
            AND table_name = %(table)s;
        """
        return self._read_query_results(query, {"schema": schema, "table": table})

    def get_sample_data(self, schema: str, table: str, limit: int = 30) -> DataFrame:
        query = f"""
        SELECT *
        FROM {schema}.{table}
        ORDER BY RANDOM()
        LIMIT %(limit)s;
        """
        return self._read_query_results(query, {"limit": limit})

    def set_table_description(self, schema: str, table: str, description: str) -> None:
        query = f"COMMENT ON TABLE {schema}.{table} IS :description;"
        self._execute_query(query, {"description": description})
        print(f"Comment successfully set on table {schema}.{table}.")
