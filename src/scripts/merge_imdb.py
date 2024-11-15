import pandas as pd

data_folder = "./data/"

def clean_title(title):
    """
    Cleanup of titles consistent accross datasets.
    """
    return title.lower().replace(" ", "")

def merge_with_imdb_id(df):
    """
    Merge a dataframe with 'title.basics.tsv' and append 'imdbID' and 'isAdult' as new features.
    """
    titles = pd.read_csv(data_folder + "title.basics.tsv", sep='\t', 
                         header=0, 
                         usecols=[0, 1, 2, 3, 4, 5], 
                         names=['imdbID', 'titleType', 'imdbPrimaryTitle', 'imdbOriginalTitle', 'isAdult', 'imdbYear'], dtype={'isAdult': 'string'})

    # sanitize imdbYear, isAdult and titleType
    titles['imdbYear'] = pd.to_numeric(titles['imdbYear'], errors='coerce')
    titles['isAdult'] = pd.to_numeric(titles['isAdult'], errors='coerce')
    titles = titles.dropna()
    titles = titles[titles['titleType'] == 'movie']

    # merge with both the imdb's original and primary titles to consider both cases
    titles['imdbOriginalTitle'] = titles['imdbOriginalTitle'].apply(clean_title)
    titles['imdbPrimaryTitle'] = titles['imdbPrimaryTitle'].apply(clean_title)
    mergeOnOriginal = pd.merge(titles, df, how='inner', left_on=['imdbOriginalTitle', 'imdbYear'], right_on=['clean_name', 'movie_date'])
    mergeOnPrimary = pd.merge(titles, df, how='inner', left_on=['imdbPrimaryTitle', 'imdbYear'], right_on=['clean_name', 'movie_date'])
    
    merge = pd.concat([mergeOnOriginal, mergeOnPrimary], axis=0)
    merge = merge.drop_duplicates(subset=['imdbID'])
    merge = merge.drop(['imdbPrimaryTitle', 'imdbOriginalTitle', 'imdbYear', 'titleType'], axis=1)
    
    return merge


def merge_with_imdb_ratings(df):
    """
    Merge a dataframe with 'title.ratings.tsv' to add rating and number of votes.
    """
    imdb_ratings = pd.read_csv(data_folder + "title.ratings.tsv", sep='\t', header=0, names=['imdbID', 'rating', 'numVotes'])

    # sanitize rating and numVotes
    imdb_ratings['rating'] = pd.to_numeric(imdb_ratings['rating'])
    imdb_ratings['numVotes'] = pd.to_numeric(imdb_ratings['numVotes'])
    imdb_ratings = imdb_ratings.dropna()

    # merge using the common imdbID
    return pd.merge(df, imdb_ratings, how='inner', on=['imdbID'])


def merge_with_imdb(df):
    """
    Merge a dataframe with IMDB's datasets.
    """
    # perform merging
    merged_id = merge_with_imdb_id(df)
    merge_imdb = merge_with_imdb_ratings(merged_id)

    # cleanup merging
    merge_imdb = merge_imdb.drop(['imdbID', 'clean_name'], axis=1)
    
    print('lines dropped during merge with IMDB: ', len(df) - len(merge_imdb))
    return merge_imdb