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
            f"{os.getenv('DATABASE_HOST')}/"
            f"{os.getenv('DATABASE_NAME')}"
        )

    def disconnect(self) -> None:
        self._engine.dispose()

    def execute_query(self, query: str, params: Mapping[str, Any] = None) -> DataFrame:
        return pd.read_sql_query(sql=query, con=self._engine, params=params)

    def list_tables(self, schema: str) -> DataFrame:
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %(schema)s
        -- ORDER BY table_name;
        ORDER BY RANDOM()
        LIMIT 6;
        """
        return self.execute_query(query, {"schema": schema})

    def get_table_info(self, schema: str, table_name: str) -> DataFrame:
        query = """
        SELECT column_name, data_type, column_default, is_nullable
        FROM information_schema.columns
        WHERE table_schema = %(schema)s
            AND table_name = %(table_name)s;
        """
        return self.execute_query(query, {"schema": schema, "table_name": table_name})

    def get_sample_data(
        self, schema: str, table_name: str, limit: int = 30
    ) -> DataFrame:
        query = f"""
        SELECT *
        FROM {schema}.{table_name}
        ORDER BY RANDOM()
        LIMIT %(limit)s;
        """
        return self.execute_query(query, {"limit": limit})

    def set_table_description(
        self, schema: str, table_name: str, description: str
    ) -> None:
        pass
