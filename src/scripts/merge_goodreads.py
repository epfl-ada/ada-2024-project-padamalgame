import os
import kagglehub
import pandas as pd
import re

def books_csv_to_df(path):
    """
    Loads all CSV files from a specified directory (except the last one) into a single pandas DataFrame.
    """
    book_csv_list = os.listdir(path)[:-1]
    book_csv_path_list = [os.path.join(path, book_csv) for book_csv in book_csv_list]
    dataframes = []
    for path, name in zip(book_csv_path_list, book_csv_list):
        df = pd.read_csv(path)
        dataframes.append(df)

    df_goodreads = pd.concat(dataframes)
    return df_goodreads


def clean_spaces(column):
    """
    Cleans the given column by converting text to lowercase and removing all spaces.
    """
    return column.apply(lambda name: str(name).lower().replace(" ", ""))


def remove_parenthesis(column):
    """
    Removes any text inside parentheses (including the parentheses themselves) from the given column.
    """
    return column.apply(lambda name: re.sub(r"\(.*?\)", "", str(name)))