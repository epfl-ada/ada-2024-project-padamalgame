import pandas as pd

def weighted_ratings(m, rating_nb_df, rating_df):
    C = rating_df.mean()
    return (rating_nb_df/ (rating_nb_df + m)) * rating_df + (m / (rating_nb_df + m)) * C

def create_weighted_ratings_df(df): 
    rating_df = pd.DataFrame(df[['MovieRating', 'MovieRatingNb', 'BookRating', 'BookRatingNb', 'MovieRuntime', 'category']])
    rating_df = rating_df[~rating_df.index.duplicated(keep='first')].dropna()

    m_book = rating_df['BookRatingNb'].quantile(0.25)
    rating_df['WeightedBookRating'] = weighted_ratings(m_book, rating_df['BookRatingNb'], rating_df['BookRating'])

    m_movie = rating_df['MovieRatingNb'].quantile(0.25)
    rating_df['WeightedMovieRating'] = weighted_ratings( m_movie, rating_df['MovieRatingNb'], rating_df['MovieRating'])
    
    return rating_df
