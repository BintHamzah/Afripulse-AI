
# AfriPulse AI – Weekly Africa Startup & VC Digest

AfriPulse AI is an **AI-powered news summarizer** that curates the top **Africa-focused startup and venture capital news** each week — automatically.
It reads business news from multiple sources, summarizes insights, and saves them as a **weekly digest** in Markdown format.

---

## 🧰 Tech Stack

* **Language:** Python 3.12.6
* **AI Stack:** LangChain, OpenAI API
* **Data:** NewsAPI
* **Dashboard:** Streamlit
* **Automation:** GitHub Actions


## Setup Instructions

### Clone the repo

```bash
git clone https://github.com/binthamzah/afripulse-ai.git
cd afripulse-ai
```

### Create & activate virtual environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add your `.env` file

Create a file named `.env` in the project root and add:

```
NEWS_API_KEY=your_api_key_here
```

---

## Run Locally

Generate the weekly digest manually:

```bash
python -m src.main.py
```

View it with the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

---

## Debugging in Jupyter

If you prefer, you can open and debug logic in Jupyter Lab:

```bash
jupyter lab
```

---

## Automating Weekly Runs

This repo includes a preconfigured **GitHub Action** that runs weekly (Friday, 9 AM UTC).
You can view and manage it under:
`.github/workflows/weekly-digest.yml`


## Author

**Fatimah Hamzah (@binthamzah)**
Passionate about AI, QA, and automation — building tools that make information accessible and insightful for Africa’s tech ecosystem.

