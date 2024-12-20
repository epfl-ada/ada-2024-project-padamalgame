import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from src.scripts.category_analysis import *
import plotly.express as px

def plot_sse(features_X, start=2, end=11, title = "Elbow Plot"):
    sse = []
    for k in range(start, end):
        # Assign the labels to the clusters
        kmeans = KMeans(n_clusters=k, random_state=0).fit(features_X)
        sse.append({"k": k, "sse": kmeans.inertia_})

    sse = pd.DataFrame(sse)
    # Plot the data
    plt.plot(sse.k, sse.sse)
    plt.xlabel("K")
    plt.ylabel("Sum of Squared Errors")
    plt.title(title)
    return sse

def get_dummy(df, column_name='MovieCategory'):    
    df_dummies = df.assign(value=True).pivot_table(
        index='wikipedia_id', 
        columns=column_name, 
        values='value',
        fill_value=0
    ).reset_index()

    df_transformed = df.drop_duplicates(subset=['wikipedia_id']).merge(df_dummies, on='wikipedia_id')
    df_transformed.drop(columns=[column_name], inplace=True)

    return df_dummies, df_transformed

def plot_clustering(df, title, name):
    fig = px.scatter(
        df,
        x='Dimension 1',
        y='Dimension 2',
        color='Label',
        hover_data={
            'MovieName': True,
            'Genre': True,
            'Dimension 1': False,
            'Dimension 2': False
        },
        title=title
    )
    fig.update_layout(width=600,height=600)
    # Show the plot
    fig.write_html(name +'.html')
    fig.show()
    return

def count_values_in_lists(series):
    all_values = [item for sublist in series for item in sublist]
    return pd.Series(all_values).value_counts()[:5].index.tolist()  

def analysis_by_cluster(df, name):

    cluster_success = df.groupby('Cluster')[['MovieBoxOffice', 'MovieRating']].mean()
    cluster_success_std = df.groupby('Cluster')[['MovieBoxOffice', 'MovieRating']].std()
    cluster_genres = df.groupby('Cluster').Genres.apply(count_values_in_lists)
    cluster_size = df.groupby('Cluster').size()
    cluster_analysis = pd.concat([cluster_success, cluster_success_std, cluster_genres, cluster_size], axis=1)
    cluster_analysis.columns = ['Average Box Office', 'Average Rating', 'Box Office Variance', 'Rating Variance', 'GenresList', 'ClusterSize']

    html_table = cluster_analysis.to_html(classes="table table-striped", index=False)

    with open((name +".html"), "w") as file:
        file.write(html_table)

    return cluster_analysis