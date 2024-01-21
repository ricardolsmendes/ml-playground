import sqlite3

import dotenv
from langchain_community import utilities
from langchain_experimental import sql
import langchain_openai
import pandas as pd


dotenv.load_dotenv()

# Utility block to extract content from a CSV file and load it into a SQLite table.
conn = sqlite3.connect("insurance.db")
df = pd.read_csv("datasets/insurance.csv")
df.to_sql("insurance", conn, if_exists="replace", index=False)
conn.close()

db = utilities.SQLDatabase.from_uri("sqlite:///insurance.db")
# Instantiate the OpenAI model.
# Pass the "temperature" parameter which controls the RANDOMNESS of the model's output.
# A lower temperature will result in more predictable output, while a higher temperature
# will result in more random output. The temperature parameter is set between 0 and 1,
# with 0 being the most predictable and 1 being the most random.
llm = langchain_openai.OpenAI(temperature=0)

chain = sql.SQLDatabaseChain.from_llm(llm, db, verbose=True)

questions = (
    "What is the highest charge?"
    " What is the average charge?"
    " What is the group that spends more, male of female?"
)
print(f"\nYOUR QUESTIONS:\n{questions}")

result = chain.invoke({"query": questions})
print(f"\nAND THE ANSWERS:\n{result.get('result')}\n")
