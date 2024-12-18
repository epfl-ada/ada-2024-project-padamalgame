import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
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

def train_linear_regression(data):
    target = 'MovieBoxOffice'
    non_feature = ['MovieGenre', 'MovieBoxOffice', 'wikipedia_id']
    features = data.drop(columns = non_feature).columns.tolist() 
    formula = f"{target} ~ {' + '.join(features)}"

    model = smf.ols(formula=formula, data=data)
    np.random.seed(2)
    results = model.fit()
    print(results.summary())

    return results

def exploratory_plot(data, y):
    # Exclude the target column
    feature_columns = [column for column in data.columns if (column != y and column != 'MovieGenre' and column != 'wikipedia_id')]
    num_features = len(feature_columns)

    # Calculate the number of rows and columns for subplots
    cols = 3  # Fixed number of columns for better visualization
    rows = math.ceil(num_features / cols)

    # Create subplots
    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 5))
    axes = axes.flatten()  # Flatten axes for easy iteration

    for i, column in enumerate(feature_columns):
        ax = axes[i]
        data.plot(kind='scatter', x=column, y=y, ax=ax, grid=True, color='fuchsia', alpha=0.5)
        ax.set_title(f'{column} vs {y}')

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    return

def plot_coefficients(res):
    variables = res.params.index    
    coefficients = res.params.values
    p_values = res.pvalues
    standard_errors = res.bse.values

    l1, l2, l3, l4 = zip(*sorted(zip(coefficients[1:], variables[1:], standard_errors[1:], p_values[1:])))

    plt.errorbar(l1, np.array(range(len(l1))), xerr= 2*np.array(l3), linewidth = 1,
             linestyle = 'none',marker = 'o',markersize= 3,
             markerfacecolor = 'black',markeredgecolor = 'black', capsize= 5)

    plt.vlines(0,0, len(l1), linestyle = '--')

    plt.yticks(range(len(l2)),l2)
    plt.xlabel('coefficients')
    plt.show()

    return


