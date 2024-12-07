
# WikiBot: An Interactive Wikipedia Chatbot

## Overview
WikiBot is an NLP-powered chatbot designed to fetch and interact with Wikipedia content. Users can input topics, ask questions, and receive concise answers with additional context when needed. The chatbot leverages Python libraries for web scraping, natural language processing, and text similarity analysis. The interface is built using Streamlit for an interactive user experience.

---

## Features
- Retrieves topic-specific content from Wikipedia.
- Provides intelligent responses to user queries using TF-IDF and cosine similarity.
- Allows users to explore more details about specific answers.
- Offers an easy-to-use web-based interface powered by Streamlit.

---

## Technologies Used
- **Python**
- **NLTK**
- **Scikit-learn**
- **BeautifulSoup**
- **Requests**
- **Streamlit**

---

## Installation

### 1. Clone the Repository
```
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment (Optional but Recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Required Packages
```
pip install -r requirements.txt
```

### 4. Download NLTK Data
```
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
```

---

## Usage
To run the WikiBot application, execute the following command:
```
streamlit run wikibot.py
```

Once the application is running, open the displayed URL (usually `http://localhost:8501`) in your browser. 

### Interacting with the Bot
1. Enter a topic to fetch its content from Wikipedia.
2. Ask questions to learn more about the topic.
3. Use the "More Info" button to retrieve additional context about the last query.

---

## Content Source
WikiBot fetches data directly from Wikipedia. All fetched content is publicly available and governed by Wikipedia's terms of use.

---

## Key Technologies
**Web Scraping**: ```BeautifulSoup``` and ```requests``` for retrieving and parsing Wikipedia content.
**Natural Language Processing**: NLTK for text preprocessing and tokenization.
**Machine Learning**: Scikit-learn for TF-IDF vectorization and cosine similarity calculations.
**Web Framework**: Streamlit for building the interactive interface.

---

## Contributing
Contributions are welcome! If you have ideas for improvements or new features, feel free to fork the repository and submit a pull request.

Steps to contribute:
1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes and push them to the branch.
4. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- **Wikipedia** for providing the content source.
- **NLTK** for natural language processing tools.
- **Scikit-learn** for vectorization and similarity calculations.
- **Streamlit** for the interactive web interface.
