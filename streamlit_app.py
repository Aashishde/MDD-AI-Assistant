import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import openai

# UI config
st.set_page_config(page_title="MDD AI Assistant", layout="wide")
st.markdown("<h2 style='color:#6c63ff;'>🤖 MDD AI Assistant (v2.5)</h2>", unsafe_allow_html=True)

# Inputs
website = st.text_input("🌐 Enter Company Website (e.g., https://fideltech.com)", "")
focus_area = st.text_input("🎯 Focus Area (e.g., Cybersecurity, Cloud, AI)", "")
leadership_note = st.text_input("📝 Leadership Remarks (Optional)", "")
supporting_links = st.text_area("🔗 Supporting Links (Optional)")

# OpenAI Key from secrets (assumed set in Streamlit Cloud or local .streamlit/secrets.toml)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Helper to extract clean website content
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs if len(p.get_text()) > 40)
        return text[:3000]  # limit token size
    except Exception as e:
        return "Error scraping website"

# Prompt builder
def build_prompt(text, focus, links, note):
    prompt = f'''
You are a business analyst at Accenture creating an M&A company profile. Based on the content below, generate a professional summary with the following sections. Tailor the insights toward the focus area: "{focus}".

Content to analyze:
{text}

Supporting links (if any): {links}

Instructions:
- Use bullet points, third-person tone.
- Include proper sections: Overview, Products & Services, Locations, Customers, Revenue/Funding, Top News, Leadership, Strategic Fit.
- Highlight relevance to Accenture.
- If Leadership Remarks are available, include in the summary.

Leadership Note: {note}

Start summary below:
'''
    return prompt

# Button trigger
if st.button("🚀 Generate Company Summary"):
    if not website:
        st.warning("Please enter a valid company website.")
    else:
        with st.spinner("🌐 Scraping Company Website..."):
            text = scrape_website(website)
            st.success("Website scraped successfully!")

        prompt = build_prompt(text, focus_area, supporting_links, leadership_note)

        with st.spinner("🤖 Generating summary with AI..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "You are a senior M&A analyst."},
                              {"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=1000
                )
                summary = response['choices'][0]['message']['content']
                st.markdown("### 📄 AI-Generated Company Summary")
                st.text_area("Summary Output", summary, height=400)
            except Exception as e:
                st.error("Failed to generate summary. Check API key or try again.")