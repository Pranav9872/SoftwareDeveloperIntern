from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np  # Import numpy to handle NaN and Infinity values
from src.ingestion import DataIngestion

app = FastAPI()

# Load and merge data
data_ingestion = DataIngestion()
data_ingestion.read_csv("data/sample.csv")  
data_ingestion.read_json("data/sample.json")
merged_data = data_ingestion.merge_data()

# ✅ Clean the data to avoid JSON serialization errors
merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinite values
merged_data.dropna(inplace=True)  # Drop NaN values

@app.get("/api/data")
def get_all_data():
    """Returns cleaned dataset as JSON."""
    return merged_data.to_dict(orient="records")

@app.get("/api/data/{file_type}")
def get_data_by_type(file_type: str):
    """Dummy endpoint for different file types."""
    return {"message": f"Data for {file_type} requested."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
