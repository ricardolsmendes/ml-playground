import dotenv

import assistant
import sqlite_helper


def run_insurance_assistant() -> None:
    table_name = "insurance"
    sqlite_helper.SQLiteHelper.load_table(table_name)
    insurance_assistant = assistant.Assistant(
        f"sqlite:///{table_name}.db", "gpt-4o-mini", "openai"
    )

    questions = [
        "What is the highest charge?",
        "What is the average charge?",
        "What group the highest average charges belong to, male of female?",
    ]

    for question in questions:
        insurance_assistant.run(question)
        print()


if __name__ == "__main__":
    dotenv.load_dotenv()
    run_insurance_assistant()
