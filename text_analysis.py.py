import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from nltk.tokenize import word_tokenize, sent_tokenize
import pyphen

# ----------------------------
# Scraper Class
# ----------------------------
class ArticleScraper
    def __init__(self, driver_path, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def extract_article(self, url):
        try:
            self.driver.get(url)
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            if articles:
                return " ".join([a.text for a in articles])
            main_elements = self.driver.find_elements(By.TAG_NAME, "main")
            if main_elements:
                return " ".join([p.text for p in main_elements[0].find_elements(By.TAG_NAME, "p")])
            return " ".join([p.text for p in self.driver.find_elements(By.TAG_NAME, "p")])
        except Exception as e:
            print(f"Failed to extract {url}: {e}")
            return ""

    def close(self):
        self.driver.quit()


# ----------------------------
# Text Analyzer Class
# ----------------------------
class TextAnalyzer:
    def __init__(self, master_dict_folder, stopwords_folder):
        self.positive_words = self._load_words(os.path.join(master_dict_folder, "positive-words.txt"))
        self.negative_words = self._load_words(os.path.join(master_dict_folder, "negative-words.txt"))
        self.stopwords_set = self._load_stopwords(stopwords_folder)
        self.syllable_dic = pyphen.Pyphen(lang='en')

    def _load_words(self, filepath):
        words = set()
        for enc in ["utf-8", "ISO-8859-1"]:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            words.add(line.lower())
                return words
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Cannot read file: {filepath} with supported encodings")

    def _load_stopwords(self, folder):
        """Load all stopwords files in folder."""
        stopwords_set = set()
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            for enc in ["utf-8", "ISO-8859-1"]:
                try:
                    with open(filepath, "r", encoding=enc) as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                stopwords_set.add(line.lower())
                    break
                except UnicodeDecodeError:
                    continue
        return stopwords_set

    def count_syllables(self, word):
        hyphens = self.syllable_dic.inserted(word)
        return max(1, hyphens.count('-') + 1)

    def analyze(self, text):
        sentences = sent_tokenize(text)
        words = [w for w in word_tokenize(text) if w.isalpha()]
        words_clean = [w for w in words if w.lower() not in self.stopwords_set]

        positive_score = sum(1 for w in words_clean if w.lower() in self.positive_words)
        negative_score = sum(1 for w in words_clean if w.lower() in self.negative_words)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(words_clean) + 0.000001)

        avg_sentence_length = len(words_clean) / (len(sentences) + 0.000001)
        complex_words = [w for w in words_clean if self.count_syllables(w) > 2]
        percentage_complex_words = len(complex_words) / (len(words_clean) + 0.000001)
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        avg_words_per_sentence = len(words_clean) / (len(sentences) + 0.000001)
        complex_word_count = len(complex_words)
        word_count = len(words_clean)
        syllables_per_word = sum(self.count_syllables(w) for w in words_clean) / (len(words_clean) + 0.000001)

        pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
        personal_pronouns = len(pronouns)
        avg_word_length = sum(len(w) for w in words_clean) / (len(words_clean) + 0.000001)

        return {
            "POSITIVE SCORE": positive_score,
            "NEGATIVE SCORE": negative_score,
            "POLARITY SCORE": polarity_score,
            "SUBJECTIVITY SCORE": subjectivity_score,
            "AVG SENTENCE LENGTH": avg_sentence_length,
            "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
            "FOG INDEX": fog_index,
            "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
            "COMPLEX WORD COUNT": complex_word_count,
            "WORD COUNT": word_count,
            "SYLLABLE PER WORD": syllables_per_word,
            "PERSONAL PRONOUNS": personal_pronouns,
            "AVG WORD LENGTH": avg_word_length
        }

# ----------------------------
# File Handler Class
# ----------------------------
class FileHandler:
    @staticmethod
    def save_article(article_text, folder, url_id):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, f"{url_id}.txt"), "w", encoding="utf-8") as f:
            f.write(article_text)


# ----------------------------
# Main Execution
# ----------------------------
def main():
    INPUT_FILE = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\Input.xlsx"
    MASTER_DICT_FOLDER = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\MasterDictionary"
    STOPWORDS_FOLDER = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\StopWords"
    ARTICLES_FOLDER = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\Articles"
    OUTPUT_FILE = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\Output.xlsx"
    CHROME_DRIVER_PATH = r"C:\Users\khann\OneDrive\Desktop\Black_coffer Project\Project\drivers\chromedriver.exe"

    # Initialize objects
    scraper = ArticleScraper(CHROME_DRIVER_PATH)
    analyzer = TextAnalyzer(MASTER_DICT_FOLDER, STOPWORDS_FOLDER)

    # Load input
    df_input = pd.read_excel(INPUT_FILE)
    results = []

    for _, row in df_input.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]
        print(f"Processing {url_id}: {url}")
        article_text = scraper.extract_article(url)
        FileHandler.save_article(article_text, ARTICLES_FOLDER, url_id)
        metrics = analyzer.analyze(article_text)
        result_row = row.to_dict()
        result_row.update(metrics)
        results.append(result_row)

    # Save output
    pd.DataFrame(results).to_excel(OUTPUT_FILE, index=False)
    print(f"Analysis completed. Output saved to {OUTPUT_FILE}")

    # Close driver
    scraper.close()

if __name__ == "__main__":
    main()