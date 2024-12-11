import pandas as pd
import json


def analysis_by_category(df): 
    # Separate the genres by each comma and explode the list into separate rows
    df['genres'] = df['genres'].str.split(', ')
    df_genres_exploded = df.explode('genres')

    # Group by 'genres' and count the number of movies in each genre
    genre_counts = df_genres_exploded['genres'].value_counts()

    # Load the genre categories from a JSON file
    with open('data/genre_categories.json', 'r') as file:
        genre_categories = json.load(file)
    # Map genres to categories
    df_genres_exploded['category'] = df_genres_exploded['genres'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # Count the number of movies in each genre category
    genre_category_counts = df_genres_exploded['category'].value_counts()
    return genre_category_counts