import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def explode_MovieGenre(df):
    """
    Separate the MovieGenre by each comma and explode the list into separate rows.
    """
    #df['MovieGenre'] = df['MovieGenre'].str.split(', ').copy()
    df.loc[:, 'MovieGenre'] = df['MovieGenre'].str.split(', ')
    df_MovieGenre_exploded = df.explode('MovieGenre')
    return df_MovieGenre_exploded

def load_genre_categories(json_file):
    """
    Load json file containing genre categories.
    """
    with open(json_file, 'r') as file:
        genre_categories = json.load(file)
    return genre_categories
    
def analysis_by_category(df, path): 
    # Separate the MovieGenre and explode the list into separate rows
    df_MovieGenre_exploded = explode_MovieGenre(df)

    # Group by 'MovieGenre' and count the number of movies in each genre
    genre_counts = df_MovieGenre_exploded['MovieGenre'].value_counts()

    # Load the genre categories from a JSON file
    genre_categories = load_genre_categories(path)
    #genre_categories = load_genre_categories('data/genre_categories.json')

    # Map MovieGenre to categories
    df_MovieGenre_exploded['MovieCategory'] = df_MovieGenre_exploded['MovieGenre'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # Count the number of movies in each genre category
    genre_category_counts = df_MovieGenre_exploded['MovieCategory'].value_counts()
    return genre_category_counts, df_MovieGenre_exploded

def category_evolution(df): 
    #_, df = analysis_by_category(df)
    genre_categories = load_genre_categories('../data/genre_categories.json')

    category_evolution = {}
    for category in genre_categories: 
        evolution = df[df['MovieCategory'] == category]['MovieYear']
        category_evolution[category] = evolution

    return category_evolution

def category_correlation(coef, df, col1, col2): 
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