import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load our hidden keys
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    """Extracts text from your PDF resume."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def evaluate_job_fit(resume_text, job_description):
    """
    Sends the resume and job description to Gemini and asks for a Fit Score.
    """
    # 1. Define the AI Model we want to use
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 2. Crafting the Prompt (The Instructions)
    prompt = f"""
    You are an expert technical recruiter. I am going to give you my resume and a job description.
    
    Task: Evaluate how well my resume fits this job description.
    
    Please provide your response in exactly this format:
    
    ### **Fit Score: [Insert Number]/100**
    
    **Why:** [Write a 2-3 sentence summary explaining the score, highlighting what matches and what might be missing.]
    
    **Company Overview:** [Write a 1-sentence summary of what this hiring company does based on the job description, if available. If not, say "Company details not provided in description."]
    
    ---
    MY RESUME:
    {resume_text}
    
    ---
    JOB DESCRIPTION:
    {job_description}
    """
    
    try:
        # 3. Sending the prompt to the AI
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing job fit: {e}"