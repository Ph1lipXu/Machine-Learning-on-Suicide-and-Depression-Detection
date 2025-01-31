import os
import csv

def saveToCSV(data, response, rows, outputDirectory):
    """
    Save data along with gpt-response & confidence level to a CSV file.

    Parameters:
    - data: Original data (list of lists or tuples).
    - LLM_response: List of labels classified by LLM (e.g., ["suicide", "depression", "teenager"]).
    - rows: Number of rows to process
    - confidence: Confidence level of how confidence the LLM make this decision
    - outputDirectory: Directory where the CSV file will be saved.
    """

    # Ensure the output directory exists
    os.makedirs(outputDirectory, exist_ok=True)

    # Create Header and New Data List
    newData = [["Index", "text", "actual_label", "LLM_response", "confidence"]]

    # Append Suitability, Confidence, and Keyword to Each Row
    for i in range(rows):
        try:
            llm_label = LLM_response[i][0] if i < len(LLM_response) else "N/A"
            confidence = LLM_response[i][1] if i < len(LLM_response) else "N/A"

            newRow = [
                data[i][0],  # Index
                data[i][1],  # Text
                data[i][2],  # label
                llm_label,   # LLM-classified Label
                confidence,   # Confidence Level
            ]
            newData.append(newRow)
        except IndexError:
            print(f"Warning: Missing data at row {i}. Skipping.")
            continue

    # Write to CSV File
    path = os.path.join(outputDirectory, 'data.csv')
    try:
        with open(path, mode='w', encoding='utf-8', newline='') as file:
            csv.writer(file).writerows(newData)
        print(f"✅ Data successfully saved to {path}")
    except Exception as e:
        print(f"❌ Error writing to CSV: {e}")