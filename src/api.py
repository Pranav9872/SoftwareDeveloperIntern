from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import numpy as np
import os
from src.ingestion import DataIngestion

app = FastAPI()

# ✅ Step 1: Check if data files exist
csv_file = "data/sample.csv"
json_file = "data/sample.json"

if not os.path.exists(csv_file) or not os.path.exists(json_file):
    raise FileNotFoundError("🚨 ERROR: One or both data files are missing! Check 'data/sample.csv' and 'data/sample.json'.")

# ✅ Step 2: Load and merge data safely
try:
    data_ingestion = DataIngestion()
    data_ingestion.read_csv(csv_file)
    data_ingestion.read_json(json_file)
    merged_data = data_ingestion.merge_data()

    # ✅ Fix: Replace invalid float values (`inf`, `-inf`) with NaN
    merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)

    # ✅ Fix: Convert NaN values to 0 (or another valid value)
    merged_data.fillna(0, inplace=True)

    # ✅ Fix: Ensure all values are JSON serializable
    merged_data = merged_data.astype(str)  # Convert all data to string to avoid JSON errors

except Exception as e:
    raise RuntimeError(f"🚨 ERROR: Failed to load and process data: {e}")

# ✅ Step 3: API Endpoints

@app.get("/")
def root():
    """Root endpoint to inform users about available API routes."""
    return {"message": "Welcome to the API. Use /api/data to fetch data."}

@app.get("/api/data")
def get_all_data():
    """Returns cleaned dataset as JSON."""
    if merged_data.empty:
        raise HTTPException(status_code=404, detail="🚨 No data available!")
    return merged_data.to_dict(orient="records")

@app.get("/api/data/{file_type}")
def get_data_by_type(file_type: str):
    """Dummy endpoint for different file types."""
    return {"message": f"Data for {file_type} requested."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

