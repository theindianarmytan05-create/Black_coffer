# 🧠 Blackcoffer NLP & Text Analytics Project

## 📋 Project Overview

This project is based on a **data extraction and NLP analysis assignment** provided by **Blackcoffer Consulting Pvt. Ltd.**
The goal was to **extract article text from given URLs, perform text analysis, compute linguistic and sentiment metrics, and generate predictive insights** including clustering and anomaly detection.

---

## 🧾 Problem Statement

The assignment included the following tasks:

### 1️⃣ **Data Extraction**

* Input file: `Input.xlsx` containing article URLs (Netclan product articles).
* Extract **only the article title and content**, ignoring headers, footers, and ads.
* Save each extracted article as a `.txt` file in the `Articles/` folder using `URL_ID` as filename.
* Python tools used: **Selenium** (with `Drivers/chromedriver`), **BeautifulSoup**, **Requests**.

### 2️⃣ **Text Analysis (NLP)**

The **objective of text analysis** is to extract sentiment, readability, complexity, and personal pronoun metrics from textual data.

**Text Analysis Methodology:**

#### **1. Sentiment Analysis**

Sentiment analysis determines whether a piece of text is **positive, negative, or neutral**. The approach is tailored for financial and general textual content.

**Steps:**

**1.1 Cleaning using Stop Words Lists**

* Text is cleaned using the stopwords provided in the `StopWords/` folder to remove common non-informative words.

**1.2 Creating a dictionary of Positive and Negative words**

* Positive and Negative word lists are stored in `Master dictionary/`.
* Words are included in the dictionary only if not present in the stopwords.

**1.3 Extracting Derived Variables**

* Text is tokenized using **NLTK**.
* Variables calculated:

| Metric                 | Calculation                                                                                      |
| :--------------------- | :----------------------------------------------------------------------------------------------- |
| **Positive Score**     | +1 for each word in Positive Dictionary, summed across text                                      |
| **Negative Score**     | +1 for each word in Negative Dictionary, summed, then multiplied by -1                           |
| **Polarity Score**     | `(Positive Score - Negative Score)/((Positive Score + Negative Score) + 1e-6)` → Range: -1 to +1 |
| **Subjectivity Score** | `(Positive Score + Negative Score)/((Total Words after cleaning) + 1e-6)` → Range: 0 to +1       |

---

#### **2. Readability Analysis**

* **Average Sentence Length** = Total words / Total sentences
* **Percentage of Complex Words** = Complex words / Total words
* **FOG Index** = 0.4 * (Average Sentence Length + Percentage of Complex Words)

---

#### **3. Average Number of Words Per Sentence**

* Formula: `Total words / Total sentences`

#### **4. Complex Word Count**

* Words with **more than two syllables**.

#### **5. Word Count**

* Count of cleaned words after removing stopwords and punctuation.

#### **6. Syllable Count per Word**

* Count vowels in each word.
* Handle exceptions (e.g., words ending with “es” or “ed” not counted as extra syllables).

#### **7. Personal Pronouns**

* Count occurrences of `I`, `we`, `my`, `ours`, `us` using regex.
* Special care taken to exclude `US` (country).

#### **8. Average Word Length**

* Formula: `Sum of characters in all words / Total number of words`

---

### 3️⃣ **EDA, Clustering & Anomaly Detection**

* **Exploratory Data Analysis (EDA)** performed on all NLP metrics (`EDA.ipynb`).
* **Clustering:** KMeans used to group articles based on sentiment, readability, and style.
* **Predicted article type:** Inferred as `News`, `Blog`, or `Report` based on cluster characteristics.
* **Anomaly Detection:** IsolationForest identified unusually complex, long, or subjective articles.

**Output columns added:**

* `Cluster` → numeric cluster ID
* `Predicted_Type` → inferred article type (`News`, `Blog`, `Report`)
* `Anomaly` → `Normal` or `Anomalous`

---

## 🧩 Project Structure

```
Blackcoffer_NLP_Project/
│
├── Input.xlsx                        # Given input URLs
├── Output.xlsx                        # NLP metrics output
├── Articles/                          # Extracted article text files (<URL_ID>.txt)
├── StopWords/                         # Stopword lists for text preprocessing
├── Master dictionary/                 # Positive and negative word lexicons
├── Drivers/                           # Chrome driver for Selenium
├── text_analysis.py                    # Web scraping + NLP metric computation
├── EDA.ipynb                           # EDA, clustering, and anomaly detection
├── Blackcoffer_Clustered_Typed_Anomalies.csv  # Final output file with clusters and anomalies
└── requirements.txt                   # Python dependencies
```

---

## ⚙️ How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Run text extraction & NLP metrics**

```bash
python text_analysis.py
```

* Saves extracted articles in `Articles/`
* Computes NLP metrics and saves `Output.xlsx`

3. **Run EDA + Clustering + Anomaly Detection**

```bash
jupyter notebook EDA.ipynb
```

* Generates clusters and predicted article types
* Marks anomalies
* Saves `Blackcoffer_Clustered_Typed_Anomalies.csv`

---

## 🧮 Technologies Used

| Category          | Tools / Libraries                                      |
| :---------------- | :----------------------------------------------------- |
| Language          | Python 3.11                                            |
| Web Scraping      | Selenium, BeautifulSoup, Requests                      |
| NLP               | NLTK, TextBlob, Regex                                  |
| Data Manipulation | Pandas, NumPy                                          |
| Visualization     | Matplotlib, Seaborn                                    |
| Machine Learning  | Scikit-learn (KMeans, IsolationForest, StandardScaler) |

---

## 📊 Key Insights

* **Clusters**:

  * Blogs → Higher subjectivity, positive sentiment
  * Reports → Higher Fog index, complex sentences
  * News → Neutral polarity, moderate complexity

* **Anomalies**: ~5% articles with unusually high complexity or subjectivity

---

## 🧑‍💼 About the Assignment

* **Provider:** Blackcoffer Consulting Pvt. Ltd.
* **Timeline:** 6 days
* **Submission:** Python script (`.py`), Excel output, and instructions

---

## 🏁 Summary

This project demonstrates a **full NLP and ML pipeline** for article analysis:

* **Data extraction → Text preprocessing → Sentiment & readability metrics → Clustering → Anomaly detection**
* Uses only Python and standard libraries
* Outputs actionable insights for article classification and quality monitoring

---
