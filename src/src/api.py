from fastapi import FastAPI
import uvicorn
import pandas as pd
from src.ingestion import DataIngestion

app = FastAPI()

data_ingestion = DataIngestion()
data_ingestion.read_csv("data/sample.csv")  # Replace with actual file
data_ingestion.read_json("data/sample.json")
merged_data = data_ingestion.merge_data()

@app.get("/api/data")
def get_all_data():
    return merged_data.to_dict(orient="records")

@app.get("/api/data/{file_type}")
def get_data_by_type(file_type: str):
    return {"message": f"Data for {file_type} requested."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
