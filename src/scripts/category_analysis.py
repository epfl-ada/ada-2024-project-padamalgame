import pandas as pd
import json

def explode_MovieGenre(df):
    """
    Separate the MovieGenre by each comma and explode the list into separate rows.
    """
    df['MovieGenre'] = df['MovieGenre'].str.split(', ')
    df_MovieGenre_exploded = df.explode('MovieGenre')
    return df_MovieGenre_exploded

def load_genre_categories(json_file):
    """
    Load json file containing genre categories.
    """
    with open(json_file, 'r') as file:
        genre_categories = json.load(file)
    return genre_categories
    

def analysis_by_category(df): 
    # Separate the MovieGenre and explode the list into separate rows
    df_MovieGenre_exploded = explode_MovieGenre(df)

    # Group by 'MovieGenre' and count the number of movies in each genre
    genre_counts = df_MovieGenre_exploded['MovieGenre'].value_counts()

    # Load the genre categories from a JSON file
    genre_categories = load_genre_categories('data/genre_categories.json')

    # Map MovieGenre to categories
    df_MovieGenre_exploded['category'] = df_MovieGenre_exploded['MovieGenre'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # Count the number of movies in each genre category
    genre_category_counts = df_MovieGenre_exploded['category'].value_counts()
    return genre_category_counts, df_MovieGenre_exploded


def category_evolution(df): 
    _, df = analysis_by_category(df)
    genre_categories = load_genre_categories('data/genre_categories.json')

    category_evolution = {}
    for category in genre_categories: 
        evolution = df[df['category'] == category]['movie_date']
        category_evolution[category] = evolution

    return category_evolution


