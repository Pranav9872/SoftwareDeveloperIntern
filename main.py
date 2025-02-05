from src.ingestion import DataIngestion
from src.visualization import DataVisualization

data_ingestion = DataIngestion()
data_ingestion.read_csv("data/sample.csv")
data_ingestion.read_json("data/sample.json")
merged_data = data_ingestion.merge_data()

viz = DataVisualization(merged_data)
viz.plot_bar_chart("Revenue")  # Replace with actual column
