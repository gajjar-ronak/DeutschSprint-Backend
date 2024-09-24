import pandas as pd
from db.init_db import insert_many, find_one

class VocabService:

    @staticmethod
    def load_excel_to_db(file_path: str):
        """
        This method reads an Excel file with levels and appends the data to MongoDB.
        Batches are inserted in chunks of 50 documents at a time.
        Duplicate German words are not inserted.
        """
        allowed_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]  # Define allowed sheet names
        batch_size = 100  # Set the batch size for inserts
        batch = []  # Initialize an empty list to store vocab entries

        # Load the Excel file and get sheet names
        excel_file = pd.ExcelFile(file_path)
        levels = excel_file.sheet_names  # Get sheet names (A1, A2, B1, etc.)

        for level in levels:
            # Only process the sheet if its name is in the allowed_levels list
            if level in allowed_levels:
                sheet_data = excel_file.parse(level)  # Read each sheet
                for _, row in sheet_data.iterrows():
                    word = row['German']
                    meaning = row['English']

                    # Step 1: Remove '*' from the German word
                    word = word.replace('*', '')

                    # Step 2: Replace consecutive '..' with 'mmen'
                    word = word.replace('..', 'mmen')

                    # Check if the German word already exists in the database
                    existing_entry = find_one("vocabulary", {"word": word})
                    
                    if not existing_entry:  # Proceed only if the word doesn't already exist
                        # Create a dictionary representing the vocabulary entry
                        vocab = {
                            "word": word,
                            "meaning": meaning,
                            "level": level
                        }

                        # Append the vocab entry to the batch
                        batch.append(vocab)

                        # When the batch size reaches 50, insert the batch into MongoDB
                        if len(batch) == batch_size:
                            insert_many("vocabulary", batch)  # Insert the current batch
                            batch = []  # Reset the batch list

        # After looping through all rows, insert any remaining items in the batch
        if batch:
            insert_many("vocabulary", batch)  # Insert the remaining batch

        return {"message": "Data successfully imported to MongoDB for allowed levels"}