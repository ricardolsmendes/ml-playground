# Usage instructions

## `analyse-insurance-data.py`

1. `cd large-language-models`
2. `touch .env`
3. Set up an OpenAI API key by adding an `OPENAI_API_KEY=<YOUR-KEY>` line to the `.env` file.
4. `python analyse-insurance-data.py`

The expected output is:

```text
YOUR QUESTION IS:
What is the highest charge? What is the average charge? What is the group that spends more, male of female?


> Entering new AgentExecutor chain...
Action: sql_db_list_tables
Action Input:

Observation: insurance, insurance.db
Thought: I should query the schema of the insurance table.
Action: sql_db_schema
Action Input: insurance
Observation: 
CREATE TABLE insurance (
	age INTEGER, 
	sex TEXT, 
	bmi REAL, 
	children INTEGER, 
	smoker TEXT, 
	region TEXT, 
	charges REAL
)

/*
3 rows from insurance table:
age	sex	bmi	children	smoker	region	charges
19	female	27.9	0	yes	southwest	16884.924
18	male	33.77	1	no	southeast	1725.5523
28	male	33.0	3	no	southeast	4449.462
*/
Thought: I should query the highest charge from the insurance table.
Action: sql_db_query
Action Input: SELECT MAX(charges) FROM insurance
Observation: [(63770.42801,)]
Thought: I should query the average charge from the insurance table.
Action: sql_db_query
Action Input: SELECT AVG(charges) FROM insurance
Observation: [(13270.422265141257,)]
Thought: I should query the group that spends more, male or female, from the insurance table.
Action: sql_db_query
Action Input: SELECT sex, SUM(charges) FROM insurance GROUP BY sex ORDER BY SUM(charges) DESC LIMIT 1
Observation: [('male', 9434763.79614)]
Thought: I now know the final answer
Final Answer: The highest charge is $63770.42801, the average charge is $13270.422265141257, and the group that spends more is male.

> Finished chain.

THE ANSWER TO YOUR QUESTION IS:
The highest charge is $63770.42801, the average charge is $13270.422265141257, and the group that spends more is male.
```
