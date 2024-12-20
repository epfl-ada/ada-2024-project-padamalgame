import pandas as pd


def weighted_ratings(m, rating_nb_df, rating_df):
    """
    Calculate the weighted ratings for items based on the number of ratings and the average rating.
    Args:
        m (int or float): The minimum number of ratings required to consider the average rating.
        rating_nb_df (pd.Series or pd.DataFrame): The number of ratings for each item.
        rating_df (pd.Series or pd.DataFrame): The average rating for each item.
    Returns:
        pd.Series or pd.DataFrame: The weighted ratings for each item.
    """
    C = rating_df.mean()
    return (rating_nb_df/ (rating_nb_df + m)) * rating_df + (m / (rating_nb_df + m)) * C


def create_weighted_ratings_df(df): 
    """
    Create a DataFrame with weighted ratings for books and movies.
    Args:
        df (pd.DataFrame): A DataFrame containing the following columns:
            - 'MovieRating': The rating of the movie.
            - 'MovieRatingNb': The number of ratings for the movie.
            - 'BookRating': The rating of the book.
            - 'BookRatingNb': The number of ratings for the book.
            - 'MovieRuntime': The runtime of the movie.
            - 'MovieCategory': The category of the movie.
    Returns:
        pd.DataFrame: A DataFrame with the following columns:
            - 'MovieRating': The rating of the movie.
            - 'MovieRatingNb': The number of ratings for the movie.
            - 'BookRating': The rating of the book.
            - 'BookRatingNb': The number of ratings for the book.
            - 'MovieRuntime': The runtime of the movie.
            - 'MovieCategory': The category of the movie.
            - 'WeightedBookRating': The weighted rating of the book.
            - 'WeightedMovieRating': The weighted rating of the movie.
    """
    rating_df = pd.DataFrame(df[['MovieRating', 'MovieRatingNb', 'BookRating', 'BookRatingNb', 'MovieRuntime', 'MovieCategory']])
    rating_df = rating_df[~rating_df.index.duplicated(keep='first')].dropna()

    m_book = rating_df['BookRatingNb'].quantile(0.25)
    rating_df['WeightedBookRating'] = weighted_ratings(m_book, rating_df['BookRatingNb'], rating_df['BookRating'])

    m_movie = rating_df['MovieRatingNb'].quantile(0.25)
    rating_df['WeightedMovieRating'] = weighted_ratings( m_movie, rating_df['MovieRatingNb'], rating_df['MovieRating'])
    
    return rating_df
