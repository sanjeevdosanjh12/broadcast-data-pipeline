import pandas as pd
import re

def process_event_terms(raw_event_string: str, team_map: dict, blacklist: list) -> str:
    """
    Cleans an event string, maps aliases using a dictionary, 
    and filters out blacklisted terms.
    """
    # Standardize delimiters (v, vs, @, -) into a clean pipe '|'
    clean_term = re.sub(r'\s+(v|vs|@|-)\s+|:|\/', ' | ', str(raw_event_string), flags=re.IGNORECASE)
    
    # Split into individual parts based on the new delimiter
    parts = [part.strip() for part in clean_term.split('|') if part.strip()]
    
    final_terms = []
    
    # Iterate through the parts and apply the Dictionary Map and Blacklist
    for part in parts:
        lookup_key = part.lower()
        
        # O(1) Hash Map Lookup: Map aliases to official names
        mapped_value = team_map.get(lookup_key, part)
        
        # Blacklist Cleaner: Remove unwanted terms using exact-word matching
        for bad_word in blacklist:
            pattern = r'\b' + re.escape(bad_word) + r'\b'
            mapped_value = re.sub(pattern, '', mapped_value, flags=re.IGNORECASE).strip()
            
        # Clean up any residual double spaces
        mapped_value = re.sub(r'\s+', ' ', mapped_value).strip()
        
        if mapped_value:
            final_terms.append(mapped_value)
            
    # Remove duplicates while preserving order
    seen = set()
    deduped_terms = [x for x in final_terms if not (x in seen or seen.add(x))]
    
    return " | ".join(deduped_terms)


def run_pipeline(input_csv: str, output_csv: str):
    """
    Simulates loading data from S3, transforming it, and saving the output.
    """
    print(f"Loading data from {input_csv}...")
    
    # Simulate our Dictionary and Blacklist (Normally loaded from a separate DB)
    master_dictionary = {
        "barca": "FC Barcelona",
        "man utd": "Manchester United",
        "chennai super kings": "CSK"
    }
    master_blacklist = ["TBC", "Friendly", "Test"]

    # In a real environment, this reads the CSV file using Pandas
    # df = pd.read_csv(input_csv)
    
    # For demonstration, creating a mock DataFrame
    data = {
        "Start Time": ["2026-06-15 14:00:00", "2026-06-16 20:00:00"],
        "End Time": ["2026-06-15 17:00:00", "2026-06-16 23:00:00"],
        "Raw Event": ["Barca vs Real Madrid", "Man Utd v Arsenal - TBC Friendly"],
        "Source": ["Node", "Node"]
    }
    df = pd.DataFrame(data)

    print("Processing and cleaning event data...")
    # Apply our cleaning function to the 'Raw Event' column
    df['Cleaned Term'] = df['Raw Event'].apply(
        lambda x: process_event_terms(x, master_dictionary, master_blacklist)
    )

    print(f"Data cleaned successfully. Exporting to {output_csv}...")
    # df.to_csv(output_csv, index=False)
    
    # Print the result to the console for the reviewer to see
    print("\n--- Final Output ---")
    print(df[['Start Time', 'Cleaned Term', 'Source']])


if __name__ == "__main__":
    # Simulate an AWS S3 automated trigger
    run_pipeline("s3://input-bucket/raw_schedule.csv", "s3://output-bucket/cleaned_schedule.csv")
