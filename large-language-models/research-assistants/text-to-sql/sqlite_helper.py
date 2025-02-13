import sqlite3

import pandas as pd


class SQLiteHelper:
    @classmethod
    def load_table(cls, name: str) -> None:
        """
        Helper method to extract content from a CSV file and load it into a SQLite table.
        """
        conn = sqlite3.connect(f"{name}.db")
        df = pd.read_csv(f"datasets/{name}.csv")
        df.to_sql(name, conn, if_exists="replace", index=False)
        conn.close()
