import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def scrap_book_to_movie(url): 
    """
    Scrapes a Wikipedia page for a table of books and their movie adaptations.
    Args:
        url (str): The URL of the Wikipedia page to scrape.
    Returns:
        pandas.DataFrame: A DataFrame containing two columns: 'fiction_work' and 'film_adaptations',
                          which list the book titles and their corresponding movie adaptations, respectively.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    response = requests.get(url)
    result = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', {'class': 'mw-parser-output'})
        tables = content.find_all('table', {'class': 'wikitable'})
        for table in tables:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')

                # Split into book and movie
                cell_tab = [cell.get_text(strip=True) for cell in cells]
                result.append(cell_tab)    

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    result = pd.DataFrame(result)
    result.columns = ['fiction_work', 'film_adaptations']
    return result
    

def extract_years_film(text):
    """
    Extracts the year or range of years from a given text string.
    This function searches for patterns that match a year or a range of years within parentheses in the format (YYYY) or (YYYY-YYYY) or (YYYY-present).
    Args:
        text (str): The input text string from which to extract the year(s).
    Returns:
        str or None: The first matched year or range of years as a string, or None if no match is found.
    """
    years = re.findall(r'\((?:[^)]*?)(\d{4}(?:[–-](?:\d{4}|present))?)(?:[^)]*?)\)', text)
    return years[0] if years else None


def extract_years_books(text):
    """
    Extracts the start and end years from a given text string.
    This function searches for patterns in the text that match a year or a range of years. 
    Args:
        text (str): The input text string containing the years.
    Returns:
        tuple: A tuple containing the start year and end year as strings. If no years are found,
               both elements of the tuple will be None.
    """
    years = re.findall(r'\((?:[^)]*?)(\d{4}(?:[–-](?:\d{4}|present))?)(?:[^)]*?)\)', text)
    years = years[0].replace('–', '-').split('-') if years else None
    start_year = years[0] if years else None
    end_year = years[-1] if years else None
    return start_year, end_year


def clean_authors(authors): 
    """
    Clean the authors' names in a DataFrame column by performing several text replacements and regex substitutions.
    Args:
        authors (pd.Series): A pandas Series containing authors' names.
    Returns:
        pd.Series: A pandas Series with cleaned authors' names.
    """
    # Replace NaN values with an empty string.
    authors = authors.fillna("")
    # Replace the string "unknown" with an empty string.
    authors = authors.replace("unknown", "")

    # Replace occurrences of "and" followed by an uppercase letter with a comma and the uppercase letter.
    authors = authors.apply(lambda a: re.sub(r'and([A-Z])', r', \1', a))
    # Replace occurrences of "and " with a comma.
    authors = authors.apply(lambda a: a.replace('and ', ','))

    # Remove the string "(series)".
    authors = authors.apply(lambda a: a.replace('(series)', ''))
    # Remove the string "various authors".
    authors = authors.apply(lambda a: a.replace('various authors', ''))
    
    # Remove text within square brackets.
    authors = authors.apply(lambda a: re.sub(r'\[.*?\]', '', a))
    # Remove text within parentheses that starts with "as".
    authors = authors.apply(lambda a: re.sub(r'\(as[^)]+\)', '', a))
    # Remove text within parentheses that starts with "pseudonym".
    authors = authors.apply(lambda a: re.sub(r'\(pseudonym[^)]+\)', '', a))

    return authors


def extract_authors(text): 
    """
    Extracts author names from a given list of text elements.
    Args:
        text (list of str): A list of text elements from which author names are to be extracted.
    Returns:
        str or None: The extracted author names or None if conditions are not met.
    """
    if any(substring in text for substring in [" fils", " père", " III", " Sr.", " Jr."]):
        text[-1] = text[-1].replace(r'\[.*?\]', '')
        return ",".join(text[-2:])
    if len(text) > 1 :
        return text[-1]
    return None


def extract_features(df):
    """
    Extracts and processes features from a DataFrame containing information about fiction works and their film adaptations.
    The function drops the original 'fiction_work' and 'film_adaptations' columns.
    Args:
        df (pandas.DataFrame): DataFrame with columns 'fiction_work' and 'film_adaptations'.
    Returns:
        pandas.DataFrame: DataFrame with the following new columns:
            - 'BookTitle': Title of the book extracted from 'fiction_work'.
            - 'BookAuthor': Author(s) of the book extracted and cleaned from 'fiction_work'.
            - 'BookStartYear': The start year of the book extracted from 'fiction_work'.
            - 'BookEndYear': The end year of the book extracted from 'fiction_work'.
            - 'FilmTitle': Title of the film extracted from 'film_adaptations'.
            - 'FilmYear': Year of the film extracted from 'film_adaptations'.
    """
    df['BookTitle'] = df['fiction_work'].str.split('(').str[0]
    df['BookTitle'] = df['BookTitle'].apply(lambda t: t.replace('"', ''))

    df_split_comma = df['fiction_work'].str.split(',')
    df['BookAuthor'] = df_split_comma.apply(extract_authors)
    df['BookAuthor'] = clean_authors(df['BookAuthor'])

    df['BookYear'] = df['fiction_work'].apply(extract_years_books)
    df['BookStartYear'] = df['BookYear'].apply(lambda x: x[0])
    df['BookEndYear'] = df['BookYear'].apply(lambda x: x[-1])
    df.drop('BookYear', axis=1, inplace=True)

    df['FilmTitle'] = df['film_adaptations'].str.split('(').str[0]
    df['FilmYear'] = df['film_adaptations'].apply(extract_years_film)

    df = df.drop(['fiction_work', 'film_adaptations'], axis = 1)

    return df


def clean_same_as_above_below(df):
    """
    Cleans the DataFrame by replacing 'same as above' and 'same as below' entries in the 'FilmTitle' column 
    with the corresponding titles from the rows above or below, respectively. The 'FilmYear' column is also 
    updated accordingly.
    Args:
        df (pandas.DataFrame): The DataFrame containing film data with 'FilmTitle' and 'FilmYear' columns.
    Returns:
        pandas.DataFrame: The cleaned DataFrame with 'same as above' and 'same as below' entries replaced.
    """
    indexes = df.index[df['FilmTitle'] == 'same as above'].tolist()
    target_ind =[(index - 1) for index in indexes]
    df['FilmTitle'][indexes] = df['FilmTitle'][target_ind]
    df['FilmYear'][indexes] = df['FilmYear'][target_ind]

    indexes = df.index[df['FilmTitle'] == 'same as below'].tolist()
    target_ind =[(index + 1) for index in indexes]
    df['FilmTitle'][indexes] = df['FilmTitle'][target_ind]
    df['FilmYear'][indexes] = df['FilmYear'][target_ind]

    return df


# Final processing on scrapping result - drops nan, null columns, fills empty rows and cleans the features
def scrap_post_processing(df): 
    """
    Post-processes the scraped data in the DataFrame.
    Args:
        df (pandas.DataFrame): The DataFrame containing the scraped data.
    Returns:
        pandas.DataFrame: The processed DataFrame.
    """
    # 1. Fill missing 'film_adaptations' values with 'fiction_work' values if 'fiction_work' is not null.
    df.loc[df['film_adaptations'].isnull() & df['fiction_work'].notnull(), ['film_adaptations']] = df['fiction_work']
    # 2. Set 'fiction_work' to None if it is the same as 'film_adaptations'.
    df.loc[df['film_adaptations'] == df['fiction_work'], ['fiction_work']] = None

    # 3. Forward fill missing 'fiction_work' values with the last non-null value.
    df['fiction_work'] = df['fiction_work'].ffill()
    # 4. Drop rows where both 'film_adaptations' and 'fiction_work' are null.
    df = df.dropna(subset=['film_adaptations'])

    # 5. Extract additional features from the DataFrame.
    df = extract_features(df)

    # 6. Clean up rows with 'same as above/below' values.
    df = clean_same_as_above_below(df)

    return df