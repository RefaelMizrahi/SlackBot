
import os
import logging
import json
logger = logging.getLogger('SupportBotSigg')
baseDir = [os.path.dirname(os.path.abspath(__file__))][-1]
def save_to_file(fileData, filename,filePath=baseDir,writeMethod="w+"):

    try:
        file = f"{filePath}/{filename}"
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            writeMethod = 'w+' # make a new file if not
        with open(file, writeMethod) as dataFile:
            json_string = f"\"{fileData}\""
            dataFile.write(json_string)
            print(
    f"Successfully saved file: {filename} to local path: {filePath}.")
    except Exception:
        print("E", f"Failed to save file: {filename} to local path: {filePath}.",
{"filename": filename, "filesPath": filePath, "fileData": f"{fileData}"})
        
def update_ticket(json_file_path, key, value):
    # Read the JSON file
    with open(f"{json_file_path}.json", "r+") as file:
        try:
            data = json.load(file)
            print(data)
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON data:", exc_info=True)
            data = {}
    
    if isinstance(data, dict):
        # Update the JSON object
        data[key] = value
        
        # Write the updated JSON object back to the file
        with open(f"{json_file_path}.json", "a+") as file:
            json.dump(data, file)
        
        logger.info("Successfully updated a ticket")
    else:
        logger.error("The JSON data is not a dictionary, but the ticket will still be updated")
        
        # Update the JSON object as a dictionary
        data = {key: value}
        
        # Write the updated JSON object back to the file
        with open(f"{json_file_path}.json", "a+") as file:
            json.dump(data, file)
        
        logger.info("Successfully updated a ticket (fallback approach)")