import dotenv
import os

import agents
import postgres_helper


if __name__ == "__main__":
    dotenv.load_dotenv()

    db_helper = postgres_helper.DatabaseHelper()
    db_helper.connect()
    agents.TableMetadataEnrichmentAgent(db_helper).run(os.getenv("DATABASE_SCHEMA"))
    db_helper.disconnect()
