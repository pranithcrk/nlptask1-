# Install required libraries:
# pip install requests beautifulsoup4 nltk

import requests
from bs4 import BeautifulSoup
import nltk as nltk
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# Replace 'your_health_website_url' with the actual URL of the health-related website you want to scrape
base_url = 'https://www.healthline.com/'



# Function to get the text content from a webpage
def get_page_content(url):
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        status_code = response.status_code
        print(f"Status Code: {status_code}")
        text_content = soup.get_text()
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

# Function to get all the links from a webpage
def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        status_code = response.status_code
        print(f"Status Code: {status_code}")
        # Adjust the HTML structure based on the website you're scraping
        links = soup.find_all('a', href=True)

        # Use a list comprehension to create the new list of links with the base URL
        new_links = ['https://www.healthline.com' + link['href'] for link in links]

        return new_links
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

def scrape_website(base_url, max_pages=100):
    visited_urls = set()
    pages_to_visit = [base_url]
    pages_scraped = 0
    text_collection = []

    while pages_to_visit and pages_scraped < max_pages:
        current_url = pages_to_visit.pop(0)

        # Skip already visited URLs
        if current_url in visited_urls:
            continue

        # Get text content from the current page
        text_content = get_page_content(current_url)
        print(f"Scraping {current_url}")
        text_collection.append(text_content)

        # Save or process the text content as needed
        # For example, you can save it to a file or process it further

        # Mark the current URL as visited
        visited_urls.add(current_url)

        # Get all links from the current page
        page_links = get_all_links(current_url)

        # Add new links to the list of pages to visit
        pages_to_visit.extend(page_links)

        # Update the counter for scraped pages
        pages_scraped += 1

    # Return the list of text content after scraping all pages
    return text_collection

# Start scraping (scrape up to 100 pages)
result_text_collection = scrape_website(base_url, max_pages=100)

def scrape_and_calculate_statistics(urls_and_texts):
    all_statistics = []
    total_statistics = {
        "num_sentences": 0,
        "num_words": 0,
        "avg_word_length": 0,
        "lexical_diversity": 0,
        "percent_stop_words": 0,
        "noun_count": 0,
    }

    for url, text1 in urls_and_texts:
        # Skip if text1 is None (indicating an issue with fetching the page content)
        if text1 is None:
            print(f"Skipping {url} due to missing page content.")
            continue
        original_sentence = sent_tokenize(text1)
        text1_clean= re.sub(r'[^\w\s]', '', text1 ) # Remove punctuation

        # Tokenize the text
        sentences = sent_tokenize(text1_clean.lower())
        words = word_tokenize(text1_clean.lower())



        # Remove stop words and calculate the percentage of stop words
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        percent_stop_words = (len(words) - len(filtered_words)) / len(words) * 100 if len(words) > 0 else 0

        # Calculate NLP statistics
        num_sentences = len(original_sentence)
        num_words = len(words)

        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / num_words if num_words > 0 else 0

        # Calculate lexical diversity
        lexical_diversity = len(set(words)) / num_words if num_words > 0 else 0

        # Calculate the frequency distribution of words
        fdist = FreqDist(filtered_words)
        common_words = fdist.most_common(5)  # Get the 5 most common words

        # # Remove stop words and calculate the percentage of stop words
        # stop_words = set(stopwords.words('english'))
        # filtered_words = [word for word in words if word.lower() not in stop_words]
        # percent_stop_words = (len(words) - len(filtered_words)) / len(words) * 100 if len(words) > 0 else 0

        # Part of Speech tagging
        pos_tags = pos_tag(filtered_words)
        noun_count = sum(1 for word, pos in pos_tags if pos in ['NN', 'NNS'])

        # Store the results in a file
        with open('nlp_statistics.txt', 'a') as file:
            file.write(f"URL: {url}\n")
            file.write(f"Number of Sentences: {num_sentences}\n")
            file.write(f"Number of Words: {num_words}\n")
            file.write(f"Average Word Length: {avg_word_length:.2f}\n")
            file.write(f"Lexical Diversity: {lexical_diversity:.2%}\n")
            file.write(f"Common Words: {common_words}\n")
            file.write(f"Percentage of Stop Words: {percent_stop_words:.2f}%\n")
            file.write(f"Noun Count: {noun_count}\n")
            file.write("\n")  # Add a separator between entries

        statistics = {
            "url": url,
            "num_sentences": num_sentences,
            "num_words": num_words,
            "avg_word_length": avg_word_length,
            "lexical_diversity": lexical_diversity,
            "common_words": common_words,
            "percent_stop_words": percent_stop_words,
            "noun_count": noun_count,
        }

        all_statistics.append(statistics)

        total_statistics["num_sentences"] += statistics["num_sentences"]
        total_statistics["num_words"] += statistics["num_words"]
        total_statistics["avg_word_length"] += statistics["avg_word_length"]
        total_statistics["lexical_diversity"] += statistics["lexical_diversity"]
        total_statistics["percent_stop_words"] += statistics["percent_stop_words"]
        total_statistics["noun_count"] += statistics["noun_count"]

        num_pages = len(urls_and_texts)
        if num_pages > 0:
            total_statistics["avg_word_length"] /= num_pages
            total_statistics["lexical_diversity"] /= num_pages
            total_statistics["percent_stop_words"] /= num_pages

    return all_statistics,total_statistics


def write_aggregated_results_to_file(filename, total_statistics):
    with open(filename, 'w') as file:
        file.write("Aggregated Results\n")
        file.write("==================\n")
        file.write(f"Average Number of Sentences: {total_statistics['num_sentences']}\n")
        file.write(f"Average Number of Words: {total_statistics['num_words']}\n")
        file.write(f"Average Average Word Length: {total_statistics['avg_word_length']:.2f}\n")
        file.write(f"Average Lexical Diversity: {total_statistics['lexical_diversity']:.2%}\n")
        file.write(f"Average Percentage of Stop Words: {total_statistics['percent_stop_words']:.2f}%\n")
        file.write(f"Average Noun Count: {total_statistics['noun_count']}\n")

# Assuming result_text_collection is a list of text content
text_collection_size = len(result_text_collection)
urls = [f"{base_url}{i}" for i in range(1, text_collection_size + 1)]

# Combine URLs and corresponding text content into a list of tuples
urls_and_texts = list(zip(urls, result_text_collection))

# Call the function with the list of tuples
all_statistics,total_stats = scrape_and_calculate_statistics(urls_and_texts)
write_aggregated_results_to_file('aggregated_results.txt', total_stats)

print(all_statistics)
