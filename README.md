# SQL Query Assistant

A Streamlit-based assistant that lets you ask natural language questions about your MySQL database and get direct answers—no SQL knowledge required.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3100/)
[![LangChain](https://img.shields.io/badge/LangChain-0052CC?logo=langchain&logoColor=white)](https://python.langchain.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21F?logo=huggingface&logoColor=black)](https://huggingface.co/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)

---

## Features

- **Natural language to SQL conversion**: Ask questions like "How many Nike t-shirts are in stock?" and get answers instantly.
- **Semantic similarity retriever**: Uses `all-MiniLM-L6-v2` for understanding your queries.
- **Few-shot example selector**: Employs ChromaDB to select relevant examples for better SQL generation.
- **Final answer returned**: You get the answer, not just the SQL query.
- **Optional FastAPI support**: (Commented in code) for API-based deployments.

---

## Project Description

SQL Query Assistant bridges the gap between business users and complex databases. By leveraging advanced language models and semantic retrieval, it allows anyone to query a MySQL database using plain English. The system interprets your question, finds relevant examples, generates the appropriate SQL, executes it, and returns the final answer—all through a simple Streamlit interface. This makes data access fast, intuitive, and accessible to non-technical users.

---

## 📽️ Demo

   ### Check the media folder

(Video) soon.....

---

## Database Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hussin-sobhy/sql_chatbot.git
   cd sql_chatbot
   ```

2. **Run MySQL locally:**
   - Make sure MySQL is installed and running on your machine.
   - Import the database schema and data:
     ```bash
     mysql -u <username> -p < init_db.sql
     ```
     Replace `<username>` with your MySQL username (usually `root`). You'll be prompted to enter your MySQL password.

   ⚠️ **Note:**
   No need to manually create the database — the `init_db.sql` file already includes:
   ```sql
   CREATE DATABASE atliq_tshirts;
   USE atliq_tshirts;
   ```

3. **Set environment variables:**
   - Copy `.env.example` to `.env` and fill in the required values:
     - `DATABASE_URL` (e.g., `mysql+pymysql://user:password@localhost/atliq_tshirts`)
     - `GOOGLE_API_KEY` (for language model access)

---

## Environment Setup (Anaconda)

1. **Create and activate a new environment:**
   ```bash
   conda create -n sql_chatbot python=3.10
   conda activate sql_chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

1. **Start the Streamlit app:**
   ```bash
   streamlit run main.py
   ```

2. **Ask your questions!**

---

## License

MIT License. See [LICENSE](LICENSE) for details. 