import pandas as pd
  
# Get Data from Excel File
def getData(filename):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(filename)

        # Check if required columns exist
        required_columns = {'index', 'text', 'class'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"❌ Missing columns in CSV: {missing_columns}")
            return []

        # Extract Data
        data = []
        for index, row in df.iterrows():
            index += 1  # Make index 1-based
            text = row['text']
            actual_label = row['class']
            data.append((index, text, actual_label))

        return data

    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []