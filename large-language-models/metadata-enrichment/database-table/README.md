# Table Metadata Enrichment Assistants powered by Large Language Models

<!--
  DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

<!-- toc -->

- [Table Description Generation Assistant](#table-description-generation-assistant)
  * [OpenAI (gpt-4o-mini)](#openai-gpt-4o-mini)

<!-- tocstop -->

## Table Description Generation Assistant

1. `cd large-language-models/metadata-enrichment/database-table`
2. `touch .env`
3. Set up Postgres connection parameters by adding the following lines to the `.env` file:
   - `DATABASE_USER=<REDACTED>`
   - `DATABASE_PASSWORD=<REDACTED>`
   - `DATABASE_HOST=<REDACTED>`, e.g., localhost
   - `DATABASE_PORT=<REDACTED>`, e.g., 5432
   - `DATABASE_NAME=<REDACTED>`
   - `DATABASE_SCHEMA=<REDACTED>`

### OpenAI (gpt-4o-mini)

1. Set up an OpenAI API key by adding an `OPENAI_API_KEY=<REDACTED>` line to the `.env` file.
2. `python main.py`

The text below brings example output regarding tables from [The MONDIAL
Database](https://www.dbis.informatik.uni-goettingen.de/Mondial):

```text
Table: provpops
Description: Table Description: This table contains demographic information about various provinces, including their geographical location and population sizes over different years. The data is crucial for understanding population trends and regional distributions across several countries.

1. In 2011, the province of Veszprém in Hungary had a population of 351,898.
2. The Gambella province in Ethiopia recorded a population of 385,997 in 2012.
3. Pando, a province in Bolivia, had a population of 110,436 in 2012.


Use the above description? (y/n/r): y
Comment successfully set on table public.provpops.



Table: river
Description: This table contains information about various rivers, lakes, seas, and their geographical attributes. Each entry provides details regarding the name of the water body, its associated river or sea, geographical measurements such as length and area, sources of the water body, elevations, and nearby mountains.

Here are three examples of data from the table:

1. The Limmat is a river that flows for 36.3 kilometers and is fed by a source located at coordinates (47.23, 8.64), with a source elevation of 406 meters. It does not have any related lakes but has an estuary at (47.50, 8.24) with an elevation of 328 meters.

2. The Potomac River, which is 652 kilometers long, flows into the Atlantic Ocean. Its source is at (39.2, -79.5) with an elevation of 933 meters, and its estuary is located at (38.00, -76.25), reaching sea level.

3. The Moskwa, stretching 502 kilometers, is associated with the Oka River and features a source located at (55.49, 35.40). It has an estuary at (55.07, 38.85) with an elevation of 100 meters, but it does not connect to any lakes or seas.


Use the above description? (y/n/r): r
Retrying...



Table: river
Description: The table stores geographical features related to various water bodies including rivers, lakes, and seas, providing details such as their lengths, areas, sources, elevation, and surrounding mountains. This information is valuable for studying hydrology, environmental science, and geography.

Here are three examples of data from the table:

1. The Limmat is a river with a length of 36.3 kilometers and it flows into the Aare. The source coordinates are approximately (47.23, 8.64) and it has a source elevation of 406 meters.

2. The Potomac River is a notable water body that stretches 652 kilometers long and meets the Atlantic Ocean. It originates from (39.2, -79.5) at an elevation of 933 meters, flowing through the Appalachian Mountains.

3. The Euphrat, spanning 2736 kilometers, has its source located at (38.8, 38.75) with an elevation of 820 meters. It is a significant river that feeds into the water systems in the region.


Use the above description? (y/n/r): y
Comment successfully set on table public.river.



Table: geo_river
Description: The table contains information about rivers, including their names, the countries they flow through, and the provinces or regions within those countries. It serves as a geographic reference for understanding river locations and their administrative affiliations.

Here are three examples of data from the table:

1. The Loire is a river located in France, specifically in the Centre-Val de Loire province.
2. The Spree flows through Germany and is situated in the Sachsen province.
3. The Dnepr river can be found in Russia, within the Smolenskaya province.


Use the above description? (y/n/r): n
Content rejected by user.
```

[<< back](..)
