# -*- coding: utf-8 -*-

# Required libraries
import requests
from bs4 import BeautifulSoup
import nltk
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

class WikiBot:
    def __init__(self):
        """Initialize the chatbot with necessary data and flags."""
        self.topic_set = False
        self.topic_title = None
        self.paragraphs = []
        self.sentences = []
        self.paragraph_indices = []
        self.current_response_index = None
        self.punctuation_removal = str.maketrans('', '', punctuation)
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def fetch_wikipedia_content(self, topic: str) -> str:
        """Fetch content from Wikipedia for the given topic."""
        topic = '_'.join(topic.title().split())
        url = f'https://en.wikipedia.org/wiki/{topic}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            self.topic_title = soup.find('h1').string
            
            # Extract paragraphs while handling inline tags
            self.paragraphs = [
                p.get_text(separator=' ', strip=True)  # Ensure spaces between inline elements
                for p in soup.find_all('p')
            ]
            
            self.sentences = []
            self.paragraph_indices = []

            for i, paragraph in enumerate(self.paragraphs):
                sentences = nltk.sent_tokenize(paragraph)
                self.sentences.extend(sentences)
                self.paragraph_indices.extend([i] * len(sentences))

            self.topic_set = True
            return f"Topic set to '{self.topic_title}'. Let's chat!"
        except requests.exceptions.RequestException as e:
            return f"Network error: {e}. Please check your connection."
        except Exception as e:
            return f"Couldn't fetch the topic. Error: {e}. Try a different topic!"

    def preprocess_text(self, text: str) -> list[str]:
        """Preprocess text by removing punctuation, stopwords, and lemmatizing."""
        words = nltk.word_tokenize(text.lower().translate(self.punctuation_removal))
        return [self.lemmatizer.lemmatize(word) for word in words if word not in self.stopwords]

    def handle_user_query(self, query: str) -> str:
        """Handle user queries by finding the most relevant response."""
        self.sentences.append(query)
        vectorizer = TfidfVectorizer(tokenizer=self.preprocess_text)
        tfidf_matrix = vectorizer.fit_transform(self.sentences)
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        self.sentences.pop()  # Remove user query after vectorization

        best_match_index = similarity_scores.argsort()[0, -1]
        best_match_score = similarity_scores[0, best_match_index]

        if best_match_score > 0:
            self.current_response_index = best_match_index
            return self.sentences[best_match_index]
        else:
            return "I'm sorry, I couldn't find relevant information."

    def provide_more_info(self) -> str:
        """Provide more information about the last discussed topic."""
        if self.current_response_index is not None:
            paragraph_index = self.paragraph_indices[self.current_response_index]
            return self.paragraphs[paragraph_index]
        else:
            return "Please ask a question first!"

# Streamlit App
def main():
    st.title("WikiBot: Your Interactive Wikipedia Chatbot")
    st.write("Type a topic below, and I'll fetch information from Wikipedia for you.")

    # Persistent bot instance
    if 'bot' not in st.session_state:
        st.session_state.bot = WikiBot()

    bot = st.session_state.bot  # Retrieve the bot

    # Input section for the topic
    topic = st.text_input("Enter a topic:", "")
    if st.button("Fetch Wikipedia Content"):
        if topic:
            result = bot.fetch_wikipedia_content(topic)
            if bot.topic_set:
                st.success(result)
            else:
                st.error(result)  # Display error if fetching fails
        else:
            st.error("Please enter a topic.")

    # Once the topic is set, allow user to ask questions
    if bot.topic_set:
        st.write(f"Topic: **{bot.topic_title}**")
        query = st.text_input("Ask a question:", "")
        if st.button("Submit Query"):
            if query:
                response = bot.handle_user_query(query)
                st.write(f"**WikiBot:** {response}")
            else:
                st.error("Please enter a question.")

        # Provide more information
        if st.button("More Info"):
            more_info = bot.provide_more_info()
            st.write(f"**More Info:** {more_info}")


# Run the Streamlit app
if __name__ == "__main__":
    main()
