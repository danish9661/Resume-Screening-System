# Resume Screening System (ATS)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22%2B-red)
![Spacy](https://img.shields.io/badge/NLP-Spacy-orange)

A Full-Stack NLP application designed to automate the initial screening of candidates. This system parses resumes (PDFs), compares them against Job Descriptions (JDs) using Cosine Similarity, and visualizes the match percentage and missing keywords via an interactive dashboard.



## **Architecture**

This project follows a decoupled **Client-Server Architecture**:

1.  **Backend (FastAPI):**
    * Exposes REST API endpoints.
    * Handles PDF parsing using `pypdf`.
    * Performs NLP tasks (Tokenization, Lemmatization) using `Spacy`.
    * Calculates Match Score using `Scikit-Learn` (TF-IDF & Cosine Similarity).

2.  **Frontend (Streamlit):**
    * Provides a user-friendly interface for file uploads.
    * Consumes the FastAPI endpoints.
    * Visualizes results using `Plotly` gauge charts.



## **Tech Stack**

* **Language:** Python 3.x
* **Backend Framework:** FastAPI, Uvicorn
* **Frontend Framework:** Streamlit
* **NLP & ML:** Spacy, Scikit-learn, NLTK
* **Data Processing:** Pandas, PyPDF
* **Visualization:** Plotly



## **Project Structure**

```bash
Smart-ATS/
│
├── backend.py        # The FastAPI server logic (Logic Layer)
├── frontend.py       # The Streamlit dashboard (Presentation Layer)
├── requirements.txt  # List of dependencies
└── README.md         # Project documentation
```

## **Installation & Setup**
1. Clone the Repository
   ```bash
   git clone [https://github.com/yourusername/smart-ats.git](https://github.com/yourusername/smart-ats.git)
   cd smart-ats
   ```
2. Create a Virtual Environment (Optional but Recommended)
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
    (Note: If you don't have a requirements file yet, run the following manually):
    ```bash
    pip install fastapi uvicorn streamlit spacy scikit-learn plotly pypdf python-multipart requests
    ```
4. Download NLP Model
    ```bash
    python -m spacy download en_core_web_sm
    ```
## **How to Run**
Since this is a full-stack application, you need to run the Backend and Frontend in two separate terminal windows.
1. Start the Backend Server \
    Open your first terminal and run:
    ```bash
    python backend.py
    ```
    You should see: INFO: Uvicorn running on http://127.0.0.1:8000
2. Start the Frontend Interface \
    Open a second terminal and run:
    ```bash
    streamlit run frontend.py
    ```
    This will automatically open your web browser at http://localhost:8501



## **API Endpoints**
The backend exposes the following Swagger documentation at
```bash
 http://127.0.0.1:8000/docs
```
#### POST /Analyze
Analyzes a resume against a job description.\
* **Request Body:**
  * resume: PDF File (Binary)

  * job_description: String 

* **Response (JSON):**
```bash
{
  "match_percentage": 78.5,
  "missing_keywords": ["sql", "docker", "aws"],
  "resume_length": 450
}
```

## **Future Improvements**
* Database Integration: Use SQLite/PostgreSQL to save candidate profiles and scores.

* Advanced NLP: Implement Named Entity Recognition (NER) to extract specific names, emails, and phone numbers.









