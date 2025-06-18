import streamlit as st

st.title("Webscraper AI") #adds a title 
url = st.text_input("Enter your website URL that needs a scrapping: ") #a text input

#button if clicked on Scrape site to pass
if st.button("Scrape Site"):
    st.write("Scrapping the website")
