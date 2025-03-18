import dotenv
import os

import assistant
import postgres_helper


if __name__ == "__main__":
    dotenv.load_dotenv()
    schema = os.getenv("DATABASE_SCHEMA")

    assistant = assistant.MetadataEnrichmentAssistant()

    db_helper = postgres_helper.DatabaseHelper()
    db_helper.connect()

    table_df = db_helper.list_tables(schema)
    tables = table_df["table_name"].tolist()

    for table in tables[:3]:
        table_info = db_helper.get_table_info(schema, table)
        sample_data = db_helper.get_sample_data(schema, table)
        description = assistant.run(table, table_info, sample_data)
        db_helper.set_table_description(schema, table, description)

    db_helper.disconnect()
