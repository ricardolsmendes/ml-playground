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
        columns_technical_metadata = db_helper.get_columns_technical_metadata(
            schema, table
        )
        sample_data = db_helper.get_sample_data(schema, table)
        description = assistant.run(table, columns_technical_metadata, sample_data)
        if description:
            db_helper.set_table_description(schema, table, description)

    db_helper.disconnect()
