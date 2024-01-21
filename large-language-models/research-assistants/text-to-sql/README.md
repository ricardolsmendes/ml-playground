# Text-to-SQL Research Assistants powered by Large Language Models

## Insurance Data Analyser

1. `cd large-language-models/research-assistants/text-to-sql`
2. `touch .env`
3. Set up an OpenAI API key by adding an `OPENAI_API_KEY=<YOUR-KEY>` line to the `.env` file.
4. `python analyse-insurance-data.py`

The text below brings an example output (formatted to improve readability):

```text
YOUR QUESTIONS:
What is the highest charge? What is the average charge? What is the group that spends
more, male of female?


> Entering new SQLDatabaseChain chain...
What is the highest charge? What is the average charge? What is the group that spends
more, male of female?

SQLQuery:SELECT MAX(charges) AS "highest charge", AVG(charges) AS "average charge",
sex AS "group", SUM(charges) AS "total charges" FROM insurance GROUP BY sex ORDER BY
"total charges" DESC LIMIT 1

SQLResult: [(62592.87309, 13956.751177721893, 'male', 9434763.79614)]

Answer:The highest charge is 62592.87309, the average charge is 13956.751177721893, and
the group that spends more is male.
> Finished chain.

AND THE ANSWERS:
The highest charge is 62592.87309, the average charge is 13956.751177721893, and the
group that spends more is male.
```

[<< back](..)
