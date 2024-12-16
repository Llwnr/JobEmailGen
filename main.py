import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def create_streamlit_app(chain: Chain, portfolio: Portfolio, clean_text):
    st.title('📧Job Email generator')
    url_input = st.text_input("Enter URL: ", 'https://fusemachines.applytojob.com/apply/IoruBvS4E2')
    submit_btn = st.button("Generate cold email")

    if submit_btn:
        if (url_input == ''):
            st.warning("No URL provided")
            return
        
        try:
            loader = WebBaseLoader([url_input])
            portfolio.load_portfolio()

            page_data = clean_text(loader.load().pop().page_content)
            job_res = chain.extract_jobs(page_data)

            links = portfolio.query_links(job_res['skills'])
            email = chain.generate_email(job_res, links)
            st.write(email)
        except Exception as e:
            st.error("An error occured:", e)

create_streamlit_app(Chain(), Portfolio(), clean_text)
    