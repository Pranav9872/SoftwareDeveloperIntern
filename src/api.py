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

    # ✅ Fix: Convert NaN values to 0
    merged_data.fillna(0, inplace=True)

    # ✅ Fix: Convert all numerical columns to safe values
    for col in merged_data.select_dtypes(include=[np.number]).columns:
        merged_data[col] = merged_data[col].astype(float)  # Ensure all numbers are floats
        merged_data[col] = np.where(
            merged_data[col] > 1e308, 1e308, merged_data[col]
        )  # Cap large numbers
        merged_data[col] = np.where(
            merged_data[col] < -1e308, -1e308, merged_data[col]
        )  # Cap small numbers

    # ✅ Debugging: Print column data types and first rows
    print("DEBUG: Column data types after cleaning:\n", merged_data.dtypes)
    print("DEBUG: First 5 rows after cleaning:\n", merged_data.head())

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

    # ✅ Ensure JSON-safe output
    return merged_data.astype(str).to_dict(orient="records")

@app.get("/api/data/{file_type}")
def get_data_by_type(file_type: str):
    """Dummy endpoint for different file types."""
    return {"message": f"Data for {file_type} requested."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


