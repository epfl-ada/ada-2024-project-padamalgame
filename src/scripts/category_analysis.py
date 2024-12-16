import pandas as pd
import json

def explode_genres(df):
    """
    Separate the genres by each comma and explode the list into separate rows.
    """
    df['genres'] = df['genres'].str.split(', ')
    df_genres_exploded = df.explode('genres')
    return df_genres_exploded

def load_genre_categories(json_file):
    """
    Load json file containing genre categories.
    """
    with open(json_file, 'r') as file:
        genre_categories = json.load(file)
    return genre_categories
    

def analysis_by_category(df): 
    # Separate the genres and explode the list into separate rows
    df_genres_exploded = explode_genres(df)

    # Group by 'genres' and count the number of movies in each genre
    genre_counts = df_genres_exploded['genres'].value_counts()

    # Load the genre categories from a JSON file
    genre_categories = load_genre_categories('data/genre_categories.json')

    # Map genres to categories
    df_genres_exploded['category'] = df_genres_exploded['genres'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # Count the number of movies in each genre category
    genre_category_counts = df_genres_exploded['category'].value_counts()
    return genre_category_counts, df_genres_exploded


def category_evolution(df): 
    _, df = analysis_by_category(df)
    genre_categories = load_genre_categories('data/genre_categories.json')

    category_evolution = {}
    for category in genre_categories: 
        evolution = df[df['category'] == category]['movie_date']
        category_evolution[category] = evolution

    return category_evolution


