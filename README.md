# AI WebScraper 🤖🕷️

An intelligent web scraping tool that combines the power of Selenium automation with AI-driven content parsing using local LLMs. Extract meaningful information from any website with natural language queries.

## ✨ Features

- **Smart Web Scraping**: Automated browser control with CAPTCHA solving
- **AI-Powered Parsing**: Use natural language to describe what you want to extract
- **Local LLM Integration**: Powered by Ollama for privacy and cost-effectiveness
- **Intelligent Content Chunking**: Handles large websites by splitting content into manageable batches
- **Clean Data Extraction**: Filters out scripts, styles, and unnecessary elements
- **Interactive Web Interface**: User-friendly Streamlit interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Chrome browser (for Selenium)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-WebScraper.git
   cd AI-WebScraper
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv ai
   source ai/bin/activate  # On Windows: ai\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama**
   ```bash
   # Install Ollama from https://ollama.ai/
   ollama pull llama3
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 🔧 How It Works

1. **Enter URL**: Provide the website URL you want to scrape
2. **Scrape Content**: The tool uses Selenium to navigate and extract DOM content
3. **Describe Your Needs**: Use natural language to describe what information you want
4. **AI Parsing**: Ollama processes the content and extracts relevant information
5. **Get Results**: View the extracted data in a clean, structured format

## 📋 Example Use Cases

- **Contact Information**: "Extract all email addresses and phone numbers"
- **Product Details**: "Find product names, prices, and descriptions"
- **News Articles**: "Get article headlines, authors, and publication dates"
- **Social Media**: "Extract usernames, follower counts, and post content"
- **Real Estate**: "Find property prices, addresses, and square footage"

## 🛠️ Technical Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│  Web Scraper    │───▶│   AI Parser     │
│                 │    │   (Selenium)    │    │   (Ollama)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐    ┌─────────────────┐
         │              │  Content Clean  │    │  Batch Process  │
         │              │  & Structure    │    │  & Extraction   │
         │              └─────────────────┘    └─────────────────┘
         │                                              │
         └──────────────────────────────────────────────┘
```

## 📁 Project Structure

```
AI-WebScraper/
├── main.py              # Streamlit web interface
├── scrape.py            # Web scraping functionality
├── parse.py             # AI parsing with Ollama
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .env                # Environment variables (optional)
```

## 🔧 Configuration

### Bright Data Integration
The project uses Bright Data for advanced scraping capabilities:
- CAPTCHA solving
- IP rotation
- Anti-bot detection bypass

Update the `AUTH` variable in `scrape.py` with your Bright Data credentials.

### LLM Models
Currently supports Llama 3 via Ollama. To use different models:
```python
model = OllamaLLM(model="llama3")  # Change to your preferred model
```

## 🚧 Roadmap

### Planned Features
- **Multi-Modal Content Extraction**: Vision AI for images and charts
- **Smart Rate Limiting**: Respectful scraping with robots.txt compliance
- **Export Options**: JSON, CSV, PDF report generation
- **Scraping Dashboard**: Real-time statistics and job management
- **Batch URL Processing**: Handle multiple URLs simultaneously

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Ollama](https://ollama.ai/) for local LLM capabilities
- [Selenium](https://selenium.dev/) for web automation
- [LangChain](https://langchain.com/) for AI integration
- [Bright Data](https://brightdata.com/) for advanced scraping infrastructure

---

**Built with ❤️ and AI** | *Making web scraping intelligent and accessible*
