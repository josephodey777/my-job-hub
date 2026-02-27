import streamlit as st
from job_fetcher import fetch_adzuna_jobs
from ai_brain import extract_text_from_pdf, evaluate_job_fit 

st.set_page_config(page_title="My Job Hub", page_icon="💼", layout="wide")

# --- UI UPGRADE: Add Background Graphics via CSS ---
def set_background():
    """Injects custom CSS to create a modern gradient background."""
    st.markdown(
        """
        <style>
        /* Light Mode Gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Dark Mode Gradient (Activates automatically if your computer is in dark mode!) */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Run the background function immediately
set_background()

# Read your resume once when the app loads
my_resume = extract_text_from_pdf("resume.pdf")

# --- MEMORY: Initialize Session State ---
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'jobs_list' not in st.session_state:
    st.session_state.jobs_list = []
# NEW: Create an empty list to hold our favorite jobs
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []

# --- SIDEBAR ---
st.sidebar.header("Search Filters")
search_keyword = st.sidebar.text_input("Job Title / Keyword", value="Developer")
selected_location = st.sidebar.selectbox("Location", ["Calgary", "Canada", "Remote"])

if st.sidebar.button("Search Jobs", type="primary"):
    with st.spinner('Fetching live jobs...'):
        jobs = fetch_adzuna_jobs(keyword=search_keyword, location=selected_location)
        st.session_state.jobs_list = jobs
        st.session_state.selected_job = None 
        
        if jobs:
            st.toast(f"Success! Found {len(jobs)} jobs.", icon="🎉")
        else:
            st.toast("No jobs found.", icon="⚠️")

# --- NEW: Sidebar section to view Saved Jobs ---
st.sidebar.markdown("---")
st.sidebar.header("⭐ My Saved Jobs")

if not st.session_state.saved_jobs:
    st.sidebar.info("You haven't saved any jobs yet.")
else:
    # Loop through our saved jobs and show them in the sidebar
    for idx, s_job in enumerate(st.session_state.saved_jobs):
        with st.sidebar.container(border=True):
            st.write(f"**{s_job['title']}**")
            st.caption(f"🏢 {s_job['company']}")
            st.link_button("Apply ↗", s_job['url'])

# --- MAIN DASHBOARD ---
st.title("💼 My Job Hub")

if st.session_state.jobs_list:
    
    # Metrics Dashboard
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(label="Jobs Found", value=len(st.session_state.jobs_list))
    with metric_col2:
        st.metric(label="Current Keyword", value=search_keyword)
    with metric_col3:
        # UI UPGRADE: Show the count of saved jobs!
        st.metric(label="Saved Jobs", value=len(st.session_state.saved_jobs)) 
        
    st.write("---")
    
    list_col, preview_col = st.columns([0.35, 0.65]) 
    
    # LEFT COLUMN: Job List
    with list_col:
        for index, job in enumerate(st.session_state.jobs_list):
            with st.container(border=True):
                st.markdown(f"#### {job['title']}")
                st.caption(f"🏢 {job['company']} | 📍 {job['location']}")
                if st.button("View Details", key=f"preview_btn_{index}", use_container_width=True):
                    st.session_state.selected_job = job

    # RIGHT COLUMN: Preview Pane
    with preview_col:
        if st.session_state.selected_job:
            job = st.session_state.selected_job
            
            st.header(job['title'])
            st.markdown(f"**{job['company']}** — *{job['location']}*")
            
            # Action Buttons Row
            btn_col1, btn_col2 = st.columns([0.3, 0.7])
            with btn_col1:
                # --- NEW: The Save Job Button ---
                if st.button("⭐ Save Job", use_container_width=True):
                    # Make sure we don't save the same job twice!
                    if job not in st.session_state.saved_jobs:
                        st.session_state.saved_jobs.append(job)
                        st.toast("Added to Saved Jobs!", icon="⭐")
                        st.rerun() # This instantly refreshes the page to update the sidebar!
                    else:
                        st.toast("Already in your saved list.", icon="ℹ️")
            with btn_col2:
                st.link_button("Apply to this Job ↗", job['url'], type="primary") 
            
            st.write(" ") 
            
            # Tabbed Interface
            tab1, tab2, tab3 = st.tabs(["🤖 AI Fit Analysis", "📄 Job Description", "⚙️ Developer Data"])
            
            with tab1:
                st.write("Click below to have Gemini read your resume and score this job.")
                if st.button("Analyze My Fit", icon="✨"):
                    if my_resume:
                        with st.spinner("Gemini is thinking..."):
                            analysis = evaluate_job_fit(my_resume, job['description'])
                            st.info(analysis)
                    else:
                        st.error("Could not read resume.pdf.")
                        
            with tab2:
                st.write(job['description'])
                
            with tab3:
                st.json(job)
                
        else:
            st.info("👈 Select a job from the list on the left to view details and run the AI analysis!")
            
else:
    st.info("Click 'Search Jobs' in the sidebar to load live postings.")