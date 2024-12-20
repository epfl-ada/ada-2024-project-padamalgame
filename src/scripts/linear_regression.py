import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import math
from src.scripts.clustering import *
from src.scripts.category_analysis import *
from collections import defaultdict
from statsmodels.stats.outliers_influence import variance_inflation_factor


def create_regression_dataset(genre_categories):
    """
    Creates a regression dataset from adapted movies data and their sentiments.
    Args:
        genre_categories (list): List of genre categories to be used for analysis.
    Returns:
        pd.DataFrame: A DataFrame containing the processed data ready for regression analysis.
    The function performs the following steps:
    1. Reads the adapted movies data and selects specific features.
    2. Drops rows with missing values in 'MovieBoxOffice', 'MoviePlot', and 'MovieRating'.
    3. Removes duplicate entries based on 'wikipedia_id'.
    4. Reads the movie sentiments data and merges it with the adapted movies data.
    5. Fills missing values in 'MovieRuntime', 'BookRating', and 'MovieRatingNb' with their respective means.
    6. Dummifies the 'MovieLanguage' column, keeping the top 4 languages and grouping the rest as 'Other Language'.
    7. Dummifies the 'MovieGenre' column based on the provided genre categories, keeping the top 10 genres and grouping the rest as 'Other Genre'.
    8. Renames columns to remove spaces and special characters.
    9. Drops the 'OtherLanguage' column and any remaining duplicates based on 'wikipedia_id'.
    10. Saves the processed data to 'data/linear_regression_data.csv'.
    Note:
        The function assumes the existence of 'data/adapted_movies.csv' and 'data/adapted_movies_sentiments.csv' files.
    """
    features = ['wikipedia_id', 'BookRating', 'MovieYear', 'MovieLanguage', 'MovieRuntime', 'MovieRating', 'MovieBoxOffice', 'MoviePlot', 'MovieRatingNb']
    adapted_movies_df = pd.read_csv('data/adapted_movies.csv')[features]
    adapted_movies_df = adapted_movies_df.dropna(subset=['MovieBoxOffice', 'MoviePlot', 'MovieRating']).reset_index(drop=True)
    adapted_movies_df.drop_duplicates(subset = 'wikipedia_id', inplace=True)
    movie_sentiments = pd.read_csv('data/adapted_movies_sentiments.csv').drop(columns=['MovieBoxOffice'])
    movie_sentiments.drop_duplicates(subset='wikipedia_id', inplace=True)

    # merge the two dataframes
    data = pd.merge(adapted_movies_df, movie_sentiments, on='wikipedia_id').drop(columns=['MoviePlot', 'MovieYear'])

    # fill missing values with the mean
    replace_mean_cols = ['MovieRuntime', 'BookRating', 'MovieRatingNb']
    data[replace_mean_cols] = data[replace_mean_cols].fillna(data[replace_mean_cols].mean())

    # dummify genres and languages
    data.MovieLanguage = data.MovieLanguage.apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    data = data.explode('MovieLanguage')
    languages = data.MovieLanguage.value_counts()[:4].index.tolist()
    data.MovieLanguage = data.MovieLanguage.apply(lambda x: x if (x in languages) else 'Other Language')
    _, data = get_dummy(data, 'MovieLanguage')
    data.dropna(subset=['MovieGenre'], inplace=True)
    _, data = analysis_by_category(data, genre_categories)
    categories = data.category.value_counts()[:10].index.tolist()
    data.category = data.category.apply(lambda x: x if (x in categories) else 'Other Genre')
    _, data = get_dummy(data, 'category')
    new_cols = {col: col.replace(" ", "").replace("&", "") for col in data.columns.tolist()}
    data.rename(columns=new_cols, inplace=True)
    data.drop(columns = ['OtherLanguage'], inplace=True)
    data.drop_duplicates(subset='wikipedia_id', inplace=True)
    data.to_csv('data/linear_regression_data.csv', index=False)
    return data


def train_linear_regression(data, formula):
    """
    Trains a linear regression model using the provided data and formula.
    Args:
        data (pandas.DataFrame): The dataset containing the variables specified in the formula.
        formula (str): A string representing the formula for the linear regression model. 
                    The formula should be in the format 'response ~ predictor1 + predictor2 + ...'.
    Returns:
        statsmodels.regression.linear_model.RegressionResultsWrapper: The fitted linear regression model results.
    """
    model = smf.ols(formula=formula, data=data)
    np.random.seed(2)
    results = model.fit()
    print(results.summary())

    return results


def exploratory_plot(data, y):
    """
    Generates scatter plots for each feature in the dataset against the target variable.
    Args:
        data (pandas.DataFrame): The input dataframe containing the dataset.
        y (str): The name of the target variable column.
    """
    feature_columns = [column for column in data.columns if (column != y and column != 'MovieGenre' and column != 'wikipedia_id')]
    num_features = len(feature_columns)

    cols = 3  
    rows = math.ceil(num_features / cols)

    # Create subplots
    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 5))
    axes = axes.flatten()  

    for i, column in enumerate(feature_columns):
        ax = axes[i]
        data.plot(kind='scatter', x=column, y=y, ax=ax, grid=True, color='fuchsia', alpha=0.5)
        ax.set_title(f'{column} vs {y}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    return


def plot_coefficients(res, title = 'Coefficients'):
    """
    Plots the coefficients of a linear regression model with error bars.
    Args:
        res (statsmodels.regression.linear_model.RegressionResultsWrapper): The result object from a fitted linear regression model.
        title (str, optional): The title of the plot. Default is 'Coefficients'.
    The function creates a plot of the coefficients of the linear regression model, including error bars representing 
    the standard errors of the coefficients. The plot is saved as a PNG file with the title as the filename (spaces 
    replaced by underscores) and displayed.
    """
    variables = res.params.index    
    coefficients = res.params.values
    p_values = res.pvalues
    standard_errors = res.bse.values

    l1, l2, l3, l4 = zip(*sorted(zip(coefficients[1:], variables[1:], standard_errors[1:], p_values[1:])))

    plt.errorbar(l1, np.array(range(len(l1))), xerr= 2*np.array(l3), linewidth = 1,
             linestyle = 'none',marker = 'o',markersize= 3,
             markerfacecolor = 'black',markeredgecolor = 'black', capsize= 5)

    plt.vlines(0,0, len(l1), linestyle = '--')

    plt.yticks(range(len(l2)),l2)
    plt.title(title)
    plt.savefig(title.replace(" ", "") +'.png')
    plt.show()

    return


def compute_vif(df):
    """
    Compute the Variance Inflation Factor (VIF) for each feature in the given DataFrame.
    VIF measures how much the variance of a regression coefficient is inflated due to multicollinearity 
    with other features in the dataset. A high VIF indicates a high correlation between the feature and 
    other features, which can be problematic in regression analysis.
    Args:
        df (pandas.DataFrame): The input DataFrame containing the features for which VIF is to be computed.
    Returns:
        pandas.DataFrame: A DataFrame containing two columns - 'Feature' and 'VIF'. 'Feature' lists the 
                        names of the features, and 'VIF' lists their corresponding VIF values.
    """
    vif_data = pd.DataFrame()
    vif_data["Feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]

    return vif_data


def explode_MovieGenre(df):
    """
    Separate the MovieGenre column by each comma and explode the list into separate rows.
    Args:
        df (pandas.DataFrame): The input DataFrame containing a 'MovieGenre' column with genres separated by commas.
    Returns:
        pandas.DataFrame: A DataFrame with each genre in the 'MovieGenre' column separated into individual rows.
    """
    df['MovieGenre'] = df['MovieGenre'].str.split(', ')
    df_MovieGenre_exploded = df.explode('MovieGenre')
    return df_MovieGenre_exploded
    

def analysis_by_category(df, genre_categories): 
    """
    Analyze the movie data by genre categories.
    Args:
        df (pd.DataFrame): DataFrame containing movie data with a 'MovieGenre' column.
        genre_categories (dict): Dictionary where keys are category names and values are lists of genres belonging to those categories.
    Returns:
        tuple: A tuple containing:
            - genre_category_counts (pd.Series): A Series with the count of movies in each genre category.
            - df_MovieGenre_exploded (pd.DataFrame): The original DataFrame with the 'MovieGenre' column exploded into individual genres and a new 'category' column.
    """
    # Separate the MovieGenre and explode the list into separate rows
    df_MovieGenre_exploded = explode_MovieGenre(df)

    # Group by 'MovieGenre' and count the number of movies in each genre
    genre_counts = df_MovieGenre_exploded['MovieGenre'].value_counts()

    # Map MovieGenre to categories
    df_MovieGenre_exploded['category'] = df_MovieGenre_exploded['MovieGenre'].map(lambda x: next((k for k, v in genre_categories.items() if x in v), 'Other'))

    # Count the number of movies in each genre category
    genre_category_counts = df_MovieGenre_exploded['category'].value_counts()
    return genre_category_counts, df_MovieGenre_exploded


def backward_elimination(data, target, predictors):
    """
    Perform backward elimination to select features based on AIC (Akaike Information Criterion).
    Args:
        data (pandas.DataFrame): The dataset containing the features and target variable.
        target (str): The name of the target variable in the dataset.
        predictors (list of str): A list of predictor variable names to consider for the model.
    Returns:
        list of str: A list of selected features after performing backward elimination.
    """
    selected_features = predictors.copy()
    while len(selected_features) > 0:
        aic_with_candidates = []
        
        # Try removing each feature from the model
        for feature in selected_features:
            remaining = [f for f in selected_features if f != feature]
            formula = f"{target} ~ {' + '.join(remaining)}" if remaining else f"{target} ~ 1"  # Model with intercept only if no predictors
            model = smf.ols(formula, data=data).fit()
            aic_with_candidates.append((model.aic, feature))
        
        # Find the feature whose removal improves AIC the most
        aic_with_candidates.sort()
        worst_candidate_aic, worst_candidate_feature = aic_with_candidates[0]
        
        # Stop if removing the feature increases AIC
        if worst_candidate_aic < smf.ols(f"{target} ~ {' + '.join(selected_features)}", data=data).fit().aic:
            selected_features.remove(worst_candidate_feature)
            print(f"Removed {worst_candidate_feature} with AIC {worst_candidate_aic}")
        else:
            break

    return selected_features


def forward_selection(data, target, predictors):
    """
    Perform forward selection to identify the best set of features for a linear regression model based on AIC.
    Args:
        data (pandas.DataFrame): The dataset containing the target and predictor variables.
        target (str): The name of the target variable.
        predictors (list of str): A list of predictor variable names to consider for the model.
    Returns:
        list of str: The list of selected features that result in the lowest AIC.
    """
    remaining_features = predictors.copy()
    selected_features = []
    best_aic = float('inf')  # Initialize with a very high AIC value

    while remaining_features:
        aic_with_candidates = []
        
        # Try adding each remaining feature to the model
        for feature in remaining_features:
            formula = f"{target} ~ {' + '.join(selected_features + [feature])}" if selected_features else f"{target} ~ {feature}"
            model = smf.ols(formula, data=data).fit()
            aic_with_candidates.append((model.aic, feature))
        
        # Find the feature that gives the lowest AIC
        aic_with_candidates.sort()
        best_candidate_aic, best_candidate_feature = aic_with_candidates[0]
        
        # If the AIC improves, add the feature to the model
        if best_candidate_aic < best_aic:
            best_aic = best_candidate_aic
            selected_features.append(best_candidate_feature)
            remaining_features.remove(best_candidate_feature)
            print(f"Selected {best_candidate_feature} with AIC {best_aic}")
        else:
            break

    return selected_features