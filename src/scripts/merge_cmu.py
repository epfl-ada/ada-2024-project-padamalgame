
import ast
import pandas as pd


def clean_title(title):
    """
    Cleanup of titles consistent accross datasets.
    """
    return title.lower().replace(" ", "")

# 
def clean_json_format(list):
    """
    Clean a json-like representation into a list of the values of the json-pairs.
    """
    dict = ast.literal_eval(list)
    return ', '.join(dict.values())

def clean_cmu(dataset_path): 
    cmu_movies = pd.read_csv(dataset_path, 
                             sep='\t', usecols=[0,2,3,4,5,6,7,8], 
                             names=['wikipedia_id','movie_name', 'movie_date', 'box_office', 'runtime', 'language', 'countries', 'genres']) 
    
    # Clean the move name and place it in another column to save the original version. This will also be used when merging with IMDB
    name_column = cmu_movies['movie_name']
    new_name_column = name_column.apply(clean_title)
    cmu_movies['clean_name'] = new_name_column

    # Clean json values to have a nicer representation
    cmu_movies['language'] = cmu_movies['language'].apply(clean_json_format)
    cmu_movies['countries'] = cmu_movies['countries'].apply(clean_json_format)
    cmu_movies['genres'] = cmu_movies['genres'].apply(clean_json_format)
    
    # Extract only the year of the Movie release date
    date_column = cmu_movies['movie_date']
    new_date_column = date_column.apply(lambda x : str(x)[0:4])
    cmu_movies['movie_date'] = new_date_column

    return cmu_movies


def merge_with_CMU(df):    
    """
    Merge a DataFrame containing movie data with the CMU Movie Summaries dataset.
    Clean movie titles, normalize JSON-like fields, extract the release year from dates, and remove duplicates and invalid data, 
    before merging the datasets.

    """
    cmu_movies = clean_cmu("../MovieSummaries/movie.metadata.tsv")
    title_column = df['FilmTitle']
    new_title_column = title_column.apply(clean_title)
    df['FilmTitle'] = new_title_column

    # Do the merge
    merge_cmu = cmu_movies.merge(right=df, how="inner", left_on=['clean_name'], right_on=['FilmTitle'], copy=False)
    merge_cmu = merge_cmu[merge_cmu.apply(check_year_in_range, axis=1)]
    merge_cmu = merge_cmu.drop(['FilmTitle', 'FilmYear'], axis=1)
    merge_cmu = merge_cmu.drop_duplicates()
    merge_cmu = merge_cmu.dropna(subset=['movie_date'])
    merge_cmu = merge_cmu[merge_cmu.movie_date != "nan"]
    merge_cmu['movie_date'] = merge_cmu['movie_date'].astype('int64')
    return merge_cmu

def check_year_in_range(row):
    year = row['movie_date']
    year_range = row['FilmYear']
    if isinstance(year_range, str) and '-' in year_range:
        start, end = map(int, year_range.split('-'))
        if end == 'present': 
            end = 2024
        return start <= year <= end
    else:
        return True
