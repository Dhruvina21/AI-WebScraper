import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
    get_soup_from_html,
    get_base_url
)
from parse import parse_with_ollama
from vision import VisionProcessor

st.set_page_config(page_title="AI WebScraper", page_icon="🤖", layout="wide")

st.title("🤖 AI WebScraper with Vision")
st.markdown("*Extract text and analyze images from any website using AI*")

# Initialize vision processor
@st.cache_resource
def get_vision_processor():
    return VisionProcessor()

url = st.text_input("Enter website URL:", placeholder="https://example.com")

col1, col2 = st.columns(2)

with col1:
    scrape_text = st.button("🕷️ Scrape Text Content", use_container_width=True)
    
with col2:
    scrape_vision = st.button("👁️ Scrape with Vision AI", use_container_width=True)

# Text scraping (original functionality)
if scrape_text and url:
    with st.spinner("Scraping website content..."):
        try:
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            
            st.session_state.dom_content = cleaned_content
            st.session_state.scraped_url = url
            
            st.success("✅ Website scraped successfully!")
            
            with st.expander("📄 View Scraped Content"):
                st.text_area("Content", cleaned_content, height=300)
                
        except Exception as e:
            st.error(f"❌ Error scraping website: {str(e)}")

# Vision scraping (new functionality)
if scrape_vision and url:
    with st.spinner("Scraping website with Vision AI..."):
        try:
            # Get HTML content
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            
            # Get soup for image processing
            soup = get_soup_from_html(result)
            base_url = get_base_url(url)
            
            # Process images
            vision_processor = get_vision_processor()
            
            st.info("🔍 Processing images found on the website...")
            vision_results = vision_processor.process_images_from_website(
                soup, 
                base_url=base_url,
                analysis_prompt="describe the main elements and any text visible"
            )
            
            # Store results
            st.session_state.dom_content = cleaned_content
            st.session_state.vision_results = vision_results
            st.session_state.scraped_url = url
            
            st.success("✅ Website scraped with Vision AI!")
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("📄 Text Content"):
                    st.text_area("Scraped Text", cleaned_content, height=300)
            
            with col2:
                with st.expander("🖼️ Vision Analysis Results"):
                    if vision_results:
                        formatted_results = vision_processor.format_vision_results(vision_results)
                        st.markdown(formatted_results)
                    else:
                        st.info("No images found on this website.")
                        
        except Exception as e:
            st.error(f"❌ Error with vision scraping: {str(e)}")

# Content parsing section
if "dom_content" in st.session_state:
    st.markdown("---")
    st.subheader("🧠 AI Content Parsing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        parse_description = st.text_area(
            "Describe what you want to extract from the text:",
            placeholder="e.g., Extract all email addresses, phone numbers, and contact information"
        )
        
    with col2:
        if "vision_results" in st.session_state:
            vision_query = st.text_area(
                "Ask about the images:",
                placeholder="e.g., What products are shown in the images? What text appears in the images?"
            )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Parse Text Content", use_container_width=True):
            if parse_description:
                with st.spinner("Parsing content with AI..."):
                    try:
                        dom_chunks = split_dom_content(st.session_state.dom_content)
                        result = parse_with_ollama(dom_chunks, parse_description)
                        
                        st.subheader("📋 Extracted Information")
                        st.markdown(result)
                        
                    except Exception as e:
                        st.error(f"❌ Error parsing content: {str(e)}")
            else:
                st.warning("Please describe what you want to extract.")
    
    with col2:
        if "vision_results" in st.session_state and st.button("🔍 Query Vision Results", use_container_width=True):
            if vision_query:
                with st.spinner("Analyzing vision results..."):
                    try:
                        vision_processor = get_vision_processor()
                        
                        # Combine all vision results into a single text
                        all_vision_text = ""
                        for result in st.session_state.vision_results:
                            all_vision_text += f"Image: {result['alt_text']}\n"
                            all_vision_text += f"OCR Text: {result['ocr_text']}\n"
                            all_vision_text += f"Analysis: {result['llm_analysis']}\n\n"
                        
                        if all_vision_text:
                            # Use the regular LLM to answer questions about vision results
                            vision_chunks = split_dom_content(all_vision_text)
                            result = parse_with_ollama(vision_chunks, vision_query)
                            
                            st.subheader("🖼️ Vision Analysis Results")
                            st.markdown(result)
                        else:
                            st.info("No vision results to analyze.")
                            
                    except Exception as e:
                        st.error(f"❌ Error analyzing vision results: {str(e)}")
            else:
                st.warning("Please enter a question about the images.")

# Sidebar with information
with st.sidebar:
    st.markdown("## 🔧 Features")
    st.markdown("""
    - **Text Scraping**: Extract and clean text content
    - **Vision AI**: Analyze images and extract text from them
    - **AI Parsing**: Use natural language to extract specific information
    - **OCR**: Extract text from images automatically
    - **Smart Analysis**: Describe and analyze visual content
    """)
    
    st.markdown("## 💡 Tips")
    st.markdown("""
    - Use specific descriptions for better results
    - Try both text and vision modes for comprehensive data
    - Vision mode works best on image-heavy websites
    - OCR can extract text from logos, charts, and graphics
    """)
    
    if "scraped_url" in st.session_state:
        st.markdown("## 📊 Current Session")
        st.info(f"**URL**: {st.session_state.scraped_url}")
        
        if "vision_results" in st.session_state:
            st.success(f"**Images Processed**: {len(st.session_state.vision_results)}")
        
        if "dom_content" in st.session_state:
            content_length = len(st.session_state.dom_content)
            st.success(f"**Content Length**: {content_length:,} characters")