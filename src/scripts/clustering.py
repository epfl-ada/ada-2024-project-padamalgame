import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from src.scripts.category_analysis import *
import plotly.express as px


def plot_sse(features_X, start=2, end=11, title="Elbow Plot"):
    """
    Plots the Sum of Squared Errors (SSE) for a range of k values to help determine the optimal number of clusters using the Elbow Method.
    Args:
        features_X (array-like or DataFrame): The input data to be clustered.
        start (int, optional): The starting value of k (number of clusters). Default is 2.
        end (int, optional): The ending value of k (number of clusters). Default is 11.
        title (str, optional): The title of the plot. Default is "Elbow Plot".
    Returns:
        DataFrame: A DataFrame containing the k values and their corresponding SSE.
    """
    # Assign the labels to the clusters
    sse = []
    for k in range(start, end):
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
    """
    Generate dummy variables for a specified column in a DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        column_name (str): The name of the column for which to create dummy variables. 
                        Default is 'MovieCategory'.
    Returns:
        tuple: A tuple containing two DataFrames:
            - df_dummies (pd.DataFrame): A DataFrame with the dummy variables.
            - df_transformed (pd.DataFrame): The original DataFrame merged with the dummy variables,
                                            with the specified column dropped.
    """
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
    """
    Plots a 2D scatter plot for clustering results using Plotly.
    Args:
        df (pandas.DataFrame): DataFrame containing the data to be plotted. 
                            It must have columns 'Dimension 1', 'Dimension 2', 'Label', 'MovieName', and 'Genre'.
        title (str): The title of the plot.
        name (str): The name of the file to save the plot as an HTML file.
    """
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
    fig.write_html(name +'.html')
    fig.show()
    return


def count_values_in_lists(series):
    """
    Count the most frequent values in a series of lists.
    Args:
        series (pd.Series): A pandas Series where each element is a list of values.
    Returns:
        list: A list of the top 5 most frequent values in the series of lists.
    """
    all_values = [item for sublist in series for item in sublist]
    return pd.Series(all_values).value_counts()[:5].index.tolist()  


def analysis_by_cluster(df, name):
    """
    Perform analysis on clusters within the given DataFrame and save the results to an HTML file.
    Args:
        df (pandas.DataFrame): The input DataFrame containing movie data with a 'Cluster' column.
        name (str): The name of the output HTML file (without extension).
    Returns:
        pandas.DataFrame: A DataFrame containing the analysis results for each cluster, including average box office,
                        average rating, box office variance, rating variance, genres list, and cluster size.
    """
    # Group the DataFrame by the 'Cluster' column and calculate the mean and standard deviation
    cluster_success = df.groupby('Cluster')[['MovieBoxOffice', 'MovieRating']].mean()
    cluster_success_std = df.groupby('Cluster')[['MovieBoxOffice', 'MovieRating']].std()

    # Count the occurrences of genres within each cluster and determine their size
    cluster_genres = df.groupby('Cluster').Genres.apply(count_values_in_lists)
    cluster_size = df.groupby('Cluster').size()
    cluster_analysis = pd.concat([cluster_success, cluster_success_std, cluster_genres, cluster_size], axis=1)
    cluster_analysis.columns = ['Average Box Office', 'Average Rating', 'Box Office Variance', 'Rating Variance', 'GenresList', 'ClusterSize']

    html_table = cluster_analysis.to_html(classes="table table-striped", index=False)

    # Save the results to an HTML file
    with open((name +".html"), "w") as file:
        file.write(html_table)

    return cluster_analysis