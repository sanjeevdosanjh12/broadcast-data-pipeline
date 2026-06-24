# Automated Broadcast Data Pipeline

An ETL (Extract, Transform, Load) data processing pipeline designed to ingest, clean, and standardize messy broadcast scheduling data (Monitoring Node Schedule). 

## 📌 Project Overview
Within the Node Schedule, raw schedule data from our Clients is often highly unstructured. Events come in with inconsistent delimiters (e.g., `v`, `vs`, `@`, `-`), undocumented internal jargon, and shorthand team aliases.

This Python pipeline utilizes **Pandas** and **Regular Expressions** to programmatically clean this data. It cross-references incoming events against a master dictionary for O(1) alias mapping, filters out blacklisted strings, and standardizes the output for downstream ingestion.

## 🛠️ Tech Stack & Concepts
* **Language:** Python 3
* **Data Science Libraries:** `pandas`
* **Techniques Used:** Regex string manipulation, Hash Map (Dictionary) lookups, List Comprehensions, Lambda functions.
* **Cloud Architecture Context:** While this script processes local CSVs/Mock Dataframes for demonstration, the architecture is designed to be deployed as a serverless function (e.g., AWS Lambda) triggered by files dropping into an **Amazon S3** bucket.

## ⚙️ Core Logic Flow
1. **Extraction:** Loads the raw, inconsistent schedule data.
2. **Regex Standardization:** Normalizes varied delimiters into a standardized format.
3. **Dictionary Mapping:** Cross-references split terms against a master dictionary to convert shorthands (e.g., "Barca") to official names (e.g., "FC Barcelona").
4. **Blacklist Filtering:** Utilizes exact-word regex matching to safely remove internal jargon (e.g., "TBC", "Friendly") without corrupting partial word matches.
5. **Deduplication & Output:** Formats the final clean string and prepares it for automated routing.
