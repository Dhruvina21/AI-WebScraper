import requests
import base64
import easyocr
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import os
import tempfile
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class VisionProcessor:
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['en'])
        self.llm = OllamaLLM(model="llama3.2-vision:11b")  # Vision-capable model
        
    def extract_images_from_soup(self, soup):
        """Extract all image URLs from BeautifulSoup object"""
        images = []
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                # Handle relative URLs
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    # This would need the base URL, we'll handle this in the main function
                    pass
                images.append({
                    'src': src,
                    'alt': alt,
                    'element': str(img)
                })
        return images
    
    def download_image(self, url):
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
            return None
    
    def extract_text_from_image(self, image):
        """Extract text from image using OCR"""
        try:
            # Convert PIL image to numpy array
            img_array = np.array(image)
            
            # Use EasyOCR to extract text
            results = self.ocr_reader.readtext(img_array)
            
            # Combine all text
            extracted_text = ' '.join([result[1] for result in results if result[2] > 0.5])
            return extracted_text
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""
    
    def analyze_image_with_llm(self, image, prompt="Describe what you see in this image"):
        """Analyze image using vision-capable LLM"""
        try:
            # Save image temporarily
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                image.save(tmp_file.name)
                
                # Convert image to base64
                with open(tmp_file.name, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
                
                # Create prompt for vision model
                vision_prompt = ChatPromptTemplate.from_template(
                    "Analyze this image and {prompt}. Be specific and detailed."
                )
                
                # Note: This is a simplified example. 
                # Actual implementation depends on the vision model you're using
                response = f"Image analysis: {prompt} (OCR extracted: {self.extract_text_from_image(image)})"
                
                # Clean up temp file
                os.unlink(tmp_file.name)
                
                return response
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"Could not analyze image: {str(e)}"
    
    def process_images_from_website(self, soup, base_url="", analysis_prompt=""):
        """Process all images from a website"""
        images = self.extract_images_from_soup(soup)
        results = []
        
        for i, img_info in enumerate(images[:5]):  # Limit to first 5 images
            print(f"Processing image {i+1}/{min(len(images), 5)}")
            
            # Handle relative URLs
            img_url = img_info['src']
            if img_url.startswith('/') and base_url:
                img_url = base_url.rstrip('/') + img_url
            
            # Download and process image
            image = self.download_image(img_url)
            if image:
                # Extract text using OCR
                ocr_text = self.extract_text_from_image(image)
                
                # Analyze with LLM if prompt provided
                llm_analysis = ""
                if analysis_prompt:
                    llm_analysis = self.analyze_image_with_llm(image, analysis_prompt)
                
                results.append({
                    'url': img_url,
                    'alt_text': img_info['alt'],
                    'ocr_text': ocr_text,
                    'llm_analysis': llm_analysis,
                    'size': image.size
                })
        
        return results
    
    def format_vision_results(self, vision_results):
        """Format vision processing results for display"""
        if not vision_results:
            return "No images found or processed."
        
        formatted_results = []
        for i, result in enumerate(vision_results, 1):
            formatted_result = f"""
**Image {i}:**
- URL: {result['url']}
- Alt Text: {result['alt_text']}
- Size: {result['size']}
- OCR Text: {result['ocr_text']}
- Analysis: {result['llm_analysis']}
---
"""
            formatted_results.append(formatted_result)
        
        return "\n".join(formatted_results)