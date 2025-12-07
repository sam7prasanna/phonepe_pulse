📊 PhonePe Transaction Insights – Data Analytics Project

This project analyzes PhonePe Pulse (2018–2024) data to uncover insights into transaction behavior, user engagement, device usage, insurance trends, and market expansion opportunities. A complete Streamlit dashboard and MySQL-backed ETL pipeline were built as part of the solution.

🚀 Tech Stack
   1. Python, Pandas, Plotly, Streamlit
   2. MySQL (Data Storage & SQL Analysis)
   3. JSON Parsing & ETL
   4. VS Code + Jupyter Notebook

📁 Project Workflow
1. Data Extraction - Parsed 35,000+ JSON files from PhonePe Pulse dataset.
2. Data Transformation - Cleaned & standardized state names
   Built DataFrames for:
   -> Aggregated (transaction, user, insurance)
   -> Map-level (district insights)
   -> Top-level (top states/districts/pincodes)
3. Load into MySQL - Created and populated 9 analytical tables:
   -> aggregated_transaction
   -> aggregated_user
   -> aggregated_insurance
   -> map_transaction
   -> map_user
   -> map_insurance
   -> top_transaction
   -> top_use
   r-> top_insurance
5. Analysis & Insights - Performed SQL + Python visualization for 5 business case studies.

🧠 Business Case Studies (5 Scenarios)
1️⃣ Transaction Dynamics
   -> Year-wise & quarter-wise trend analysis
   -> State performance & category distribution

2️⃣ Device Dominance & User Engagement
   -> Registered users by device
   -> App opens (engagement levels)

3️⃣ Insurance Penetration
   -> State-wise insurance growth
   -> High/low penetration markets

4️⃣ Market Expansion Analysis
   -> Top performing states
   -> Underpenetrated regions for expansion

5️⃣ User Engagement Strategy
   -> User growth by state & district
   -> Pincode-level hotspots
   -> App-open based engagement scoring

Includes:
   -> India maps (transaction amount/count)
   -> Device usage charts
   -> Insurance penetration visuals
   -> District-level registered user analysis
   -> Top states/districts/pincodes

▶ How to Run the Project
   1. Clone the PhonePe Pulse dataset
   2. Run ETL notebook analysis.ipynb
   3. Start MySQL and load tables
   4. Run Streamlit app

📄 Folder Structure
phonepe-project/
│── app.py
│── pulse_Df.ipynb
│── README.md

📝 Key Takeaways
   1. Built a complete ETL → SQL → Visualization → Dashboard workflow
   2. Delivered meaningful business insights for PhonePe’s growth
   3. Demonstrated strong analytical and technical capabilities
