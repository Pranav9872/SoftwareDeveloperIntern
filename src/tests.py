import pytest
from src.ingestion import DataIngestion

def test_csv_ingestion():
    ingestion = DataIngestion()
    ingestion.read_csv("data/test.csv")
    assert not ingestion.data[0].empty
