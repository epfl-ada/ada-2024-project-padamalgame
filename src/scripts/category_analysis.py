import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def explode_MovieGenre(df):
    """
    Separate the MovieGenre column by each comma and explode the list into separate rows.
    Args:
        df (pandas.DataFrame): The input DataFrame containing a 'MovieGenre' column with genres separated by commas.
    Returns:
        pandas.DataFrame: A DataFrame with each genre in the 'MovieGenre' column separated into individual rows.
    """
    df.loc[:, 'MovieGenre'] = df['MovieGenre'].str.split(', ')
    df_MovieGenre_exploded = df.explode('MovieGenre')
    return df_MovieGenre_exploded


def load_genre_categories(json_file):
    """
    Load genre categories from a JSON file.
    Args:
        json_file (str): The path to the JSON file containing genre categories.
    Returns:
        dict: A dictionary containing genre categories.
    """
    with open(json_file, 'r') as file:
        genre_categories = json.load(file)
    return genre_categories

    
def analysis_by_category(df, path): 
    """
    Analyze the movie data by category.
    Args:
        df (pandas.DataFrame): The DataFrame containing movie data.
        path (str): The path to the JSON file containing genre categories.
    Returns:
        tuple: A tuple containing:
            - genre_category_counts (pandas.Series): A Series with the count of movies in each genre category.
            - df_MovieGenre_exploded (pandas.DataFrame): The DataFrame with the 'MovieGenre' column exploded and a new 'MovieCategory' column.
    """
    # 1. Explode the 'MovieGenre' column in the DataFrame.
    df_MovieGenre_exploded = explode_MovieGenre(df)

    # 2. Group the data by 'MovieGenre' and counts the number of movies in each genre.
    genre_counts = df_MovieGenre_exploded['MovieGenre'].value_counts()

    # 3. Load the genre categories from the specified JSON file.
    genre_categories = load_genre_categories(path)

    # 4. Map each 'MovieGenre' to a broader category based on the loaded genre categories.
    df_MovieGenre_exploded['MovieCategory'] = df_MovieGenre_exploded['MovieGenre'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # 5. Count the number of movies in each genre category.
    genre_category_counts = df_MovieGenre_exploded['MovieCategory'].value_counts()

    return genre_category_counts, df_MovieGenre_exploded


def category_evolution(df): 
    """
    Analyzes the evolution of movie categories over the years.
    Args:
        df (pandas.DataFrame): A DataFrame containing movie data with at least two columns:
                               'MovieCategory' and 'MovieYear'.
    Returns:
        dict: A dictionary where the keys are movie categories (as defined in the genre_categories.json file)
              and the values are pandas Series containing the years in which movies of those categories were released.
    """
    genre_categories = load_genre_categories('../data/genre_categories.json')

    category_evolution = {}
    for category in genre_categories: 
        evolution = df[df['MovieCategory'] == category]['MovieYear']
        category_evolution[category] = evolution

    return category_evolution


def category_correlation(coef, df, col1, col2): 
    """
    Calculate the correlation between two columns for each category in the DataFrame.
    Args:
        coef (str): The type of correlation coefficient to use ('pearson' or 'spearman').
        df (pd.DataFrame): The DataFrame containing the data.
        col1 (str): The name of the first column to correlate.
        col2 (str): The name of the second column to correlate.
    Returns:
        pd.DataFrame: A DataFrame containing the correlation, p-value, and significance for each category.
    """
    category_stats = {}
    categories= df['MovieCategory'].unique()

    for category in categories : 
        df_cat = df[df['MovieCategory'] == category]
        if len(df_cat[col1]) > 2: 
            if coef == 'pearson': 
                res = stats.pearsonr(df_cat[col1], df_cat[col2])
                category_stats[category]= res
            elif coef == 'spearman': 
                res = stats.spearmanr(df_cat[col1], df_cat[col2])
                category_stats[category]= res

    category_stats_df = pd.DataFrame.from_dict(
        category_stats, 
        orient='index', 
        columns=['Correlation', 'P-value']
    ).reset_index()
    category_stats_df.rename(columns={'index': 'Category'}, inplace=True)
    category_stats_df['Significant'] = category_stats_df['P-value'].apply(lambda x : (x < 0.05))
    
    return category_stats_df.sort_values(by=['Correlation']).reset_index()


def plot_category_correlation(df, title): 
    """
    Plots the correlation of different categories with a bar plot.
    Args:
        df (pandas.DataFrame): DataFrame containing the data to plot. It must have the columns 'Category', 'Correlation', and 'Significant'.
        title (str): The title of the plot.
    The function creates a bar plot where each bar represents the correlation of a category. 
    The bars are colored based on the 'Significant' column, with 'orange' for significant correlations and 'grey' for non-significant correlations. 
    The correlation values are displayed as text on the bars. A vertical dashed line is drawn at x=0 to indicate the zero correlation line.
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
            x=row['Correlation'], 
            y=i, 
            s=f"{row['Correlation']:.2f}", 
            va='center', 
            ha='right' if row['Correlation'] < 0 else 'left', 
            color='black', 
            fontsize=10
    )
    
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title(f'{title}')
    plt.xlabel('Correlation')
    plt.ylabel('Category')
    plt.legend(title='Significance', loc='upper right')

    plt.tight_layout()
    plt.show()