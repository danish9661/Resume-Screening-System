from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
import spacy
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_bytes):
    pdf = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def clean_text(text):
    doc = nlp(text)
    # Remove stopwords and punctuation, lemmatize
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...), 
    job_description: str = Form(...)
):
    # 1. Read and Parse Text
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)
    
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    # 2. Calculate Similarity (Match Percentage)
    # Combine texts to create a common vocabulary for TF-IDF
    documents = [cleaned_resume, cleaned_jd]
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    match_percentage = round(pairwise_similarity[0][0] * 100, 2)

    # 3. Keyword Extraction for Visualization
    # Find words present in JD but missing in Resume
    resume_tokens = set(cleaned_resume.split())
    jd_tokens = set(cleaned_jd.split())
    missing_keywords = list(jd_tokens - resume_tokens)
    
    # Filter for significant words (simple heuristic: common nouns/proper nouns only)
    # In a real app, you'd have a specific list of tech skills to check against
    doc_jd = nlp(job_description)
    important_keywords = [token.text.lower() for token in doc_jd if token.pos_ in ["NOUN", "PROPN"]]
    missing_important = list(set(important_keywords) & set(missing_keywords))

    return {
        "match_percentage": match_percentage,
        "missing_keywords": missing_important[:10], # Top 10 missing
        "resume_length": len(cleaned_resume.split())
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)