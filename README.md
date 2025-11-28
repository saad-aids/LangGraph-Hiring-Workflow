# LangGraph-Hiring-Workflow
Conditional AI Screening System using LangGraph and Streamlit


# 🤖 LangGraph Conditional AI Hiring Workflow

An AI-powered application built with **LangGraph** and **Streamlit** to automate the initial screening of job candidates based on their resume and a job description.

The system implements a **conditional workflow** that scores a candidate and automatically routes them into one of three distinct interview processes: **One Interview**, **Two Interviews**, or **Rejection**.

## ✨ Features

* **Conditional Routing:** Uses LangGraph's conditional edges to route applications based on a calculated weighted score.
* **Interactive UI:** Built with Streamlit for easy, manual **PDF file uploads** (Resume and Job Description).
* **State Management:** Utilizes a `TypedDict` state object to manage the flow of data (text, scores, recommendation) between nodes.
* **Modular Design:** Follows a clear structure (Load -> Extract -> Score -> Route -> Report) as taught in advanced workflow courses.
* **Simulated LLM:** Includes logic for LLM nodes (`extract_info`, `generate_final_report`), but uses simulation if no API key is provided, keeping the focus on the LangGraph flow.

## 🛠️ Prerequisites

Make sure you have Python (3.9+) and `pip` installed.

## 🚀 Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/saad-aids/LangGraph-Hiring-Workflow.git](https://github.com/saad-aids/LangGraph-Hiring-Workflow.git)
    cd LangGraph-Hiring-Workflow
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **(Optional) Setup Gemini API Key:**
    If you wish to use the actual LLM nodes instead of the simulation, set your Gemini API key in your environment variables. The simulation mode is on by default (`llm = None` in `app.py`).

## 💡 Usage

To launch the Streamlit application:

```bash
streamlit run app.py
