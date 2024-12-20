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
    """
    Classifies the sentiment of the given text using the provided classifier.
    Args:
        text (str): The text to be classified.
        classifier (callable): A function or model that takes a sentence as input and returns a list of dictionaries with 'score' keys.
    Returns:
        dict: A dictionary with the average sentiment scores for each emotion category:
            - "sadness": Average score for sadness.
            - "joy": Average score for joy.
            - "love": Average score for love.
            - "anger": Average score for anger.
            - "fear": Average score for fear.
            - "surprise": Average score for surprise.
    """
    # Split the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize logits storage
    all_logits = []

    # Get the logits for each sentence
    for sentence in sentences:
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
    """
    Perform sentiment analysis on a series of texts using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    Args:
        texts (pd.Series): A pandas Series containing text data to analyze.
    Returns:
        pd.DataFrame: A DataFrame containing the sentiment scores for each text. The scores include:
            - 'neg': Negative sentiment score
            - 'neu': Neutral sentiment score
            - 'pos': Positive sentiment score
            - 'compound': Compound sentiment score, which is a normalized, weighted composite score.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiments = texts.apply(lambda t: analyzer.polarity_scores(t))
    return pd.DataFrame(sentiments.tolist())


def BERT_sentiment_analysis(texts, model_name = "bhadresh-savani/distilbert-base-uncased-emotion"):
    """
    Perform sentiment analysis on a list of texts using a BERT-based model.
    Args:
        texts (list of str): A list of texts to analyze.
        model_name (str, optional): The name of the pre-trained BERT model to use for sentiment analysis. 
                                    Default is "bhadresh-savani/distilbert-base-uncased-emotion".
    Returns:
        pd.DataFrame: A DataFrame containing the sentiment scores for each text.
    """
    classifier = pipeline("text-classification", model=model_name, return_all_scores=True)
    sentiments = [classify_text(text, classifier) for text in texts]
    return pd.DataFrame(sentiments)


def textblob_sentiment_analysis(texts):
    """
    Perform sentiment analysis on a series of texts using TextBlob.
    Args:
        texts (pd.Series): A pandas Series containing text data to analyze.
    Returns:
        pd.DataFrame: A DataFrame with two columns, 'polarity' and 'subjectivity', representing the sentiment analysis results for each text.
    """
    sentiments = texts.apply(lambda t: {"polarity" : TextBlob(t).sentiment.polarity,
                                        "subjectivity" : TextBlob(t).sentiment.subjectivity})
    return pd.DataFrame(sentiments.tolist())


def sentiment_analysis(df, algorithms, column_name = 'MoviePlot'):  
    """
    Perform sentiment analysis on a specified column of a DataFrame using multiple algorithms.
    Args:
        df (pandas.DataFrame): The input DataFrame containing movie data.
        algorithms (list): A list of sentiment analysis algorithms to apply. Each algorithm should be a function that takes a pandas Series as input and returns a pandas Series.
        column_name (str, optional): The name of the column in the DataFrame to perform sentiment analysis on. Default is 'MoviePlot'.
    Returns:
        pandas.DataFrame: A DataFrame with the original columns 'MovieBoxOffice', 'MovieGenre', 'wikipedia_id', and additional columns for each algorithm's sentiment analysis results.
    """
    box_office = df.MovieBoxOffice
    genre = df.MovieGenre
    id = df.wikipedia_id
    data = [box_office, genre, id]
    for algo in algorithms: 
        data.append(algo(df[column_name]))
    return pd.concat(data, axis=1)


def plot_correlation(df):
    """
    Plots the correlation between categories and their correlation values with significance indication.
    Args:
        df (pandas.DataFrame): DataFrame containing the following columns:
            - 'Category': The category names.
            - 'Correlation': The correlation values.
            - 'Significant': Boolean indicating if the correlation is significant.
    The function creates a bar plot where each bar represents the correlation value of a category.
    The bars are colored based on the significance of the correlation (orange for significant, grey for not significant).
    The correlation values are displayed as text on the bars.
    A vertical dashed line is drawn at the zero correlation mark.
    The plot is saved as 'book-movie_plot_correlation.jpg' and displayed.
    """
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
    plt.savefig('book-movie_plot_correlation.jpg')
    plt.show()
    return