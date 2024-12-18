import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from scripts.category_analysis import *

def plot_sse(features_X, start=2, end=11):
    sse = []
    for k in range(start, end):
        # Assign the labels to the clusters
        kmeans = KMeans(n_clusters=k, random_state=10).fit(features_X)
        sse.append({"k": k, "sse": kmeans.inertia_})

    sse = pd.DataFrame(sse)
    # Plot the data
    plt.plot(sse.k, sse.sse)
    plt.xlabel("K")
    plt.ylabel("Sum of Squared Errors")
    return sse

def plot_silhouette(X, start=2, end=11):
    silhouettes = []

    # Try multiple k
    for k in range(2, 11):
        # Cluster the data and assigne the labels
        labels = KMeans(n_clusters=k, random_state=10).fit_predict(X)
        # Get the Silhouette score
        score = silhouette_score(X, labels)
        silhouettes.append({"k": k, "score": score})
        
    # Convert to dataframe
    silhouettes = pd.DataFrame(silhouettes)

    # Plot the data
    plt.plot(silhouettes.k, silhouettes.score)
    plt.xlabel("K")
    plt.ylabel("Silhouette score")
    return silhouettes

def get_dummy_genre(df):    
    df_genre = df.assign(value=True).pivot_table(
        index='wikipedia_id', 
        columns='category', 
        values='value',
        fill_value=0
    ).reset_index()

    df_transformed = df.drop_duplicates(subset=['wikipedia_id']).merge(df_genre, on='wikipedia_id')
    df_transformed.drop(columns=['MovieGenre', 'category'], inplace=True)

    return df_genre, df_transformed