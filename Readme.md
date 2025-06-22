# 🛍️ Retail Customer Segmentation Dashboard

A complete end-to-end **Data Engineering + Machine Learning** project that segments online retail customers based on purchasing behavior and presents insights via an interactive **Streamlit dashboard**.

---

## 🔍 Overview

This project demonstrates the modern data workflow:

- 📐 Dimensional modeling using ER diagrams and star schema
- 🔄 ETL pipeline loading into PostgreSQL
- 🤖 Unsupervised ML clustering with `KMeans`
- 📊 Visualized insights using Streamlit, Plotly & Matplotlib
- 🐳 Dockerized app for easy local and cloud deployment

---

## 📁 Project Structure

---

## 🚀 Features

- 📦 Star schema design for analytical efficiency
- 🔄 Fast ETL with SQLAlchemy and bulk inserts
- 🤖 Customer segmentation using scikit-learn `KMeans`
- 📊 Dashboard with charts, filters, and CSV downloads
- 🐳 Easy-to-deploy Docker container

---

## 🧠 Tech Stack

| Component     | Tools Used                             |
|---------------|-----------------------------------------|
| Data Storage  | PostgreSQL                              |
| ETL Pipeline  | Python, Pandas, SQLAlchemy              |
| ML Modeling   | scikit-learn, NumPy                     |
| Dashboard     | Streamlit, Plotly, Matplotlib, Seaborn  |
| Container     | Docker                                  |

---

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/retail-ml-app.git
cd retail-ml-app

### 2. Build the Docker image

```bash
docker build -t retail-ml-app .

### 3. Run the App

```bash
docker run -p 8501:8501 --rm retail-ml-app

Then visit: http://localhost:8501

📊 Dashboard Highlights
	•	✅ Segment Filter: Choose from Top Spenders, Average Buyers, etc.
	•	📈 KPI Metrics: Avg. revenue, basket size, and unique products
	•	📊 Charts:
	•	Bar: Segment-wise customer count
	•	Pie: Revenue share by segment
	•	Scatter: Basket size vs. revenue
	•	📋 Data Table: Filtered customer info + CSV download

🧠 ML Model Details
	•	Model: KMeans clustering (unsupervised)
	•	Features:
	•	Total revenue per customer
	•	Total invoices
	•	Avg. basket size
	•	Number of unique products
	•	Output: Customers grouped into clusters, then labeled as business-friendly segments

📄 License

MIT License — Use freely for learning, showcasing, and non-commercial purposes.

⸻

🙌 Acknowledgements
	•	Online Retail Dataset - UCI ML Repository
	•	Inspired by real-world data workflows from modern data engineering and analytics stacks