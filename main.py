import streamlit as st
from scrape import scrape_website
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)

st.title("Webscraper AI") #adds a title 
url = st.text_input("Enter your website URL that needs a scrapping: ") #a text input

#button if clicked on Scrape site to pass
if st.button("Scrape Site"):
    st.write("Scrapping the website")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content
    #expander text box to allow us view more content
    with st.expander("View DOM content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
    


