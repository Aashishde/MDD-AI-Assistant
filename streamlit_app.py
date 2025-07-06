import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- UI ---
st.set_page_config(page_title="MDD AI Assistant", layout="wide")
st.title("🤖 MDD-AI Assistant for M&A Team")

st.markdown("""
This assistant helps generate one-page company profiles for M&A research.
Just enter the company website and optional focus area, and the AI will summarize the key details.
""")

# --- Input Fields ---
company_website = st.text_input("🔗 Company Website (e.g., https://www.fideltech.com)")
focus_area = st.text_input("🎯 Focus Area (e.g., Cybersecurity, Cloud, AI) (optional)")
supporting_links = st.text_area("📎 Supporting Links (PDFs, Case Studies, YouTube, etc.) (optional)")
leadership_remarks = st.text_area("💬 Leadership Remarks (optional)")

if st.button("🚀 Generate Company Summary"):
    if not company_website:
        st.warning("Please enter a valid company website URL.")
    else:
        # --- Simulate scraping from website ---
        st.subheader("🌐 Scraping Company Website...")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(company_website, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.title.string if soup.title else "No title found"
            meta_desc = ""
            for tag in soup.find_all("meta"):
                if tag.get("name") == "description":
                    meta_desc = tag.get("content")
                    break

            st.success("Website scraped successfully!")
            
            # --- Mock Summary Output ---
            st.subheader("📄 AI-Generated Company Summary (Demo)")
            st.markdown(f"""
            ### 🏢 Company: {company_website}
            **Focus Area:** {focus_area or 'General'}

            **Overview:**
            - {title_tag}
            - {meta_desc or 'No meta description found'}
            - Based on website analysis, company appears to be in the {focus_area or 'technology'} space.

            **Leadership Remarks:**
            > {leadership_remarks or 'No remarks provided'}

            **Supporting Links:**
            {supporting_links or 'No supporting links provided'}
            """)

        except Exception as e:
            st.error(f"Failed to scrape the website. Error: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Created by Aashish Dey • MDD AI Assistant v1.0 • June 2025")
