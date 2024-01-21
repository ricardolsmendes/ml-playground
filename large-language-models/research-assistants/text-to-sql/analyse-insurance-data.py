import os
import sqlite3
from typing import Any

import dotenv
import langchain
from langchain_community import utilities
from langchain_experimental import sql
import langchain_openai
import pandas as pd
import torch
import transformers


class ModelFactory:
    _LLAMA2_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

    @classmethod
    def make_llama_2(cls, temperature=0) -> Any:
        """
        Instantiate the Llama 2 model.

        :param temperature: controls the RANDOMNESS of the model's output. A lower
            temperature will result in more predictable output, while a higher
            temperature will result in more random output. The temperature parameter is
            set between 0 and 1, with 0 being the most predictable and 1 being the most
            random.
        :return: the Llama 2 model
        """
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            cls._LLAMA2_MODEL_NAME, token=os.environ.get("HUGGING_FACE_ACCESS_TOKEN")
        )

        model = transformers.AutoModelForCausalLM.from_pretrained(
            cls._LLAMA2_MODEL_NAME, token=os.environ.get("HUGGING_FACE_ACCESS_TOKEN")
        )

        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
            max_length=1000,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
        )

        return langchain.HuggingFacePipeline(
            pipeline=pipeline, model_kwargs={"temperature": temperature}
        )

    @classmethod
    def make_openai(cls, temperature=0) -> Any:
        """
        Instantiate the OpenAI model.

        :param temperature: controls the RANDOMNESS of the model's output. A lower
            temperature will result in more predictable output, while a higher
            temperature will result in more random output. The temperature parameter is
            set between 0 and 1, with 0 being the most predictable and 1 being the most
            random.
        :return: the OpenAI model
        """
        return langchain_openai.OpenAI(temperature=temperature)


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
