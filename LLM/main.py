import os
import time
from utilities.retrieve import getData
from utilities.gpt import askGPT
from utilities.export import saveToCSV

# Supress Warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Curlm already closed!")

# Variables
directory = "data/"
files = [f for f in os.listdir(directory) if f.endswith('.csv')]
GPT = True
NUM = 0

# Text-Based Menu UI
print("\nSelect File to Analyze:\n")
for i, file in enumerate(files, 1):
    print(f"{i}: {file}")
choice = int(input("\nEnter Corresponding Number: ")) - 1
print("\n")
filename = os.path.join(directory, files[choice])
outputDirectory = os.path.join("output", os.path.splitext(files[choice])[0])
os.makedirs(outputDirectory, exist_ok = True)

# Get Data
data = getData(filename)

# Iterate Entire Dataset
if NUM == 0:
    NUM = len(data)

# Fetch GPT Response
response = []
if(GPT):
    for i in range(0, NUM):
        try:
            # Ask GPT and Parse Response
            response = askGPT(data[i][1])
            parsedResponse = response.split("\n")

            # Safely Extract Suitability, Confidence, and Keyword
            if len(parsedResponse) >= 3:
                LLM_response = parsedResponse[0].strip()  # Extract the first part ('suicide'/'depression'/'teenager')
                confidence = parsedResponse[1].strip()   # Extract the second part (0-1 confidence score)
                print(f"Processed Abstract {i+1}: llm_response ={LLM_response}, Confidence={confidence}")
            else:
                # Default values for unexpected response formats
                LLM_response = "Error"
                confidence = "0.0"

            # Ensure Suitability is not an Error Message
            if "too many messages in a row" in LLM_response or "ip:" in LLM_response:
                response.append(["Error", "0.0"])
            else:
                response.append([LLM_response, confidence])

            time.sleep(2)  # Delay for 2 second

        except Exception as e:
            print(f"Error Processing Abstract {i+1}: {str(e)}")
            response.append(["Error", "0.0"])
        
        # Calculate Progress
        progress = round(((i + 1) / NUM) * 100)
        bar = 50
        fill = int(bar * progress // 100)
        bar = '█' * fill + '-' * (bar - fill)

        print(f'Processing: |{bar}| {progress}% Complete')

    print("Processing Complete!\n")

    # Save Data to CSV File
    saveToCSV(data, response, NUM, outputDirectory)