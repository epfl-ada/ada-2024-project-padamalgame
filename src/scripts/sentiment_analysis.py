import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import math

def classify_text(text, classifier):
    # Split the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize logits storage
    all_logits = []

    for sentence in sentences:
        # Get the logits for each sentence
        results = classifier(sentence)
        logits = [score['score'] for score in results[0]]
        all_logits.append(logits)

    # Average logits over all sentences
    avg_logits = np.mean(all_logits, axis=0)
    
    # Get the final label based on the average logits
    return {"sadness": avg_logits[0],
             "joy": avg_logits[1],
             "love" : avg_logits[2],
             "anger" : avg_logits[3],
             "fear" : avg_logits[4],
             "surprise" : avg_logits[5],}

def vader_sentiment_analysis(texts):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = texts.apply(lambda t: analyzer.polarity_scores(t))
    return pd.DataFrame(sentiments.tolist())

def BERT_sentiment_analysis(texts, model_name = "bhadresh-savani/distilbert-base-uncased-emotion"):
    classifier = pipeline("text-classification", model=model_name, return_all_scores=True)
    sentiments = [classify_text(text, classifier) for text in texts]
    return pd.DataFrame(sentiments)

def textblob_sentiment_analysis(texts):
    sentiments = texts.apply(lambda t: {"polarity" : TextBlob(t).sentiment.polarity,
                                        "subjectivity" : TextBlob(t).sentiment.subjectivity})
    return pd.DataFrame(sentiments.tolist())

def sentiment_analysis(df, algorithms, column_name = 'MoviePlot'):  
    box_office = df.MovieBoxOffice
    genre = df.MovieGenre
    id = df.wikipedia_id
    data = [box_office, genre, id]
    for algo in algorithms: 
        data.append(algo(df[column_name]))
    return pd.concat(data, axis=1)


def plot_correlation(df):
    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df,
        y='Category',
        x='Correlation',
        hue='Significant',
        palette={True: 'orange', False: 'grey'},
        dodge=False
    )
    for i, row in df.iterrows():
        plt.text(
            row['Correlation'],  # X-coordinate
            i,  # Y-coordinate
            f"{row['Correlation']:.2f}",  # Text: rounded correlation value
            va='center',  # Align text vertically
            ha='right' if row['Correlation'] < 0 else 'left',  # Align text based on the value
            color='black'
        )

    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title('Spearman Correlation')
    plt.xlabel('Correlation')
    plt.ylabel('Category')
    plt.legend(title='Significance', loc='lower right')

    plt.tight_layout()
    plt.show()
    plt.savefig('book-movie_plot_correlation.png')
    return

