import streamlit as st
import requests
import plotly.graph_objects as go

# Set Page Config
st.set_page_config(page_title="Smart ATS", layout="wide")

st.title("🤖 Smart Resume Screening System")
st.markdown("### Full-Stack Python Project: FastAPI + Streamlit")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("Upload Details")
    job_description = st.text_area("Paste Job Description (JD)", height=300)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    analyze_button = st.button("Analyze Resume")

with col2:
    st.header("Analysis Results")
    
    if analyze_button and uploaded_file and job_description:
        # Prepare data for API
        files = {"resume": uploaded_file.getvalue()}
        data = {"job_description": job_description}
        
        with st.spinner("Analyzing... Connecting to FastAPI Backend..."):
            try:
                # Send to Backend
                response = requests.post("http://127.0.0.1:8000/analyze", files=files, data=data)
                result = response.json()
                
                # --- VISUALIZATION 1: Gauge Chart for Match Percentage ---
                score = result['match_percentage']
                
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': "JD Match Score"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 75], 'color': "gray"},
                            {'range': [75, 100], 'color': "lightblue"}],
                    }
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # --- VISUALIZATION 2: Missing Keywords ---
                st.subheader("⚠️ Missing Keywords")
                if result['missing_keywords']:
                    st.write("Consider adding these to your resume:")
                    # Display as tags
                    st.write(", ".join([f"`{word}`" for word in result['missing_keywords']]))
                else:
                    st.success("Great job! No major keywords missing.")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Make sure 'backend.py' is running!")