# 🚀 Software Developer Intern - Technical Assessment

## 📌 Overview
This project is a **data ingestion, visualization, and REST API application**. It reads data from multiple formats (CSV, JSON, PPTX, PDF), processes and merges the data, and provides interactive visualizations. The project also exposes a **FastAPI-based REST API** to fetch the processed data.

---

## 🔧 Setup Instructions

### **1️⃣ Clone the Repository**
To get started, clone this repository to your local machine:
```bash
cd ~/Documents
git clone https://github.com/Pranav9872/SoftwareDeveloperIntern.git
cd SoftwareDeveloperIntern
pip install -r requirements.txt
uvicorn src.api:app --reload
http://127.0.0.1:8000/docs
