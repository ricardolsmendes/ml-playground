# Text-to-SQL Research Assistants powered by Large Language Models

<!--
  DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

<!-- toc -->

- [Insurance Data Assistant](#insurance-data-assistant)
  * [OpenAI (gpt-4o-mini)](#openai-gpt-4o-mini)

<!-- tocstop -->

## Insurance Data Assistant

1. `cd large-language-models/research-assistants/text-to-sql`
2. `touch .env`

### OpenAI (gpt-4o-mini)

1. Set up an OpenAI API key by adding an `OPENAI_API_KEY=<YOUR-KEY>` line to the `.env` file.
2. `python main.py`

The text below brings an example output (formatted to improve readability):

```text
QUESTION:
What is the highest charge?

- query:
SELECT MAX(charges) AS highest_charge FROM insurance;
- result:
[(63770.42801,)]
- answer:
The highest charge is 63770.43.


QUESTION:
What is the average charge?

- query:
SELECT AVG(charges) AS average_charge FROM insurance;
- result:
[(13270.422265141257,)]
- answer:
The average charge is approximately 13,270.42.


QUESTION:
What group the highest average charges belong to, male of female?

- query:
SELECT sex, AVG(charges) AS average_charges
FROM insurance
GROUP BY sex
ORDER BY average_charges DESC
LIMIT 10;
- result:
[('male', 13956.751177721893), ('female', 12569.578843835347)]
- answer:
The group with the highest average charges is male, with an average charge of approximately 13956.75.
```

[<< back](..)
