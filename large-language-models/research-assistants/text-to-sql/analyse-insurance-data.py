import os
import sqlite3
import sys

import dotenv
from langchain_community import utilities
from langchain_community.llms import huggingface_pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models.llms import BaseLLM
from langchain_experimental import sql
import langchain_openai
from langchain_openai import OpenAI
import pandas as pd
import torch
import transformers


class ModelFactory:
    _LLAMA2_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
    _OPENAI_MODEL_NAME = "gpt-3.5-turbo-instruct"

    @classmethod
    def make_model(cls, model_family: str, temperature: float = 0.0001) -> BaseLLM:
        family_to_factory_map = {
            "--llama-2": cls.make_llama_2,
            "--openai": cls.make_openai,
        }
        return family_to_factory_map.get(model_family.lower())(temperature)

    @classmethod
    def make_llama_2(cls, temperature: float = 0.0001) -> HuggingFacePipeline:
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
            cls._LLAMA2_MODEL_NAME,
            token=os.environ.get("HUGGING_FACE_ACCESS_TOKEN"),
            torch_dtype=torch.float16,
            device_map="auto",
        )

        generation_config = transformers.GenerationConfig.from_pretrained(
            cls._LLAMA2_MODEL_NAME
        )
        generation_config.temperature = temperature
        generation_config.repetition_penalty = 1.15

        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            generation_config=generation_config,
        )

        return huggingface_pipeline.HuggingFacePipeline(
            pipeline=pipeline, model_kwargs={"temperature": temperature}
        )

    @classmethod
    def make_openai(cls, temperature: float = 0.0001) -> OpenAI:
        """
        Instantiate the OpenAI model.

        :param temperature: controls the RANDOMNESS of the model's output. A lower
            temperature will result in more predictable output, while a higher
            temperature will result in more random output. The temperature parameter is
            set between 0 and 1, with 0 being the most predictable and 1 being the most
            random.
        :return: the OpenAI model
        """
        return langchain_openai.OpenAI(
            model_name=cls._OPENAI_MODEL_NAME, temperature=temperature
        )


class SQLiteHelper:
    @classmethod
    def load_insurance_table(cls):
        """
        Helper method to extract content from a CSV file and load it into a SQLite table.
        """
        conn = sqlite3.connect("insurance.db")
        df = pd.read_csv("datasets/insurance.csv")
        df.to_sql("insurance", conn, if_exists="replace", index=False)
        conn.close()


dotenv.load_dotenv()

# Instantiate the Large Language Model.
llm = ModelFactory.make_model(sys.argv[1])

SQLiteHelper.load_insurance_table()
db = utilities.SQLDatabase.from_uri("sqlite:///insurance.db")
chain = sql.SQLDatabaseChain.from_llm(llm, db, verbose=True)

question_1 = "What is the highest charge?"
question_2 = "What is the average charge?"
question_3 = "What group the highest average charges belong to, male of female?"
questions = [question_1, question_2, question_3]

for question in questions:
    chain.invoke({"query": question})
