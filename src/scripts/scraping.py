import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Scraps a url to extract a list of fiction works and their film adaptation
def scrap_book_to_movie(url): 
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

                # splits into book and movie
                cell_tab = [cell.get_text(strip=True) for cell in cells]
                result.append(cell_tab)    

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    result = pd.DataFrame(result)
    result.columns = ['fiction_work', 'film_adaptations']
    return result
    
# Extracts years in format "2000", "1999-2000" or "1999-present"
def extract_years_film(text):
    years = re.findall(r'\((?:[^)]*?)(\d{4}(?:[–-](?:\d{4}|present))?)(?:[^)]*?)\)', text)
    return years[0] if years else None


def extract_years_books(text):
    years = re.findall(r'\((?:[^)]*?)(\d{4}(?:[–-](?:\d{4}|present))?)(?:[^)]*?)\)', text)
    years = years[0].replace('–', '-').split('-') if years else None
    start_year = years[0] if years else None
    end_year = years[-1] if years else None
    return start_year, end_year


# Cleanup authors feature
def clean_authors(authors): 
    authors = authors.fillna("")
    authors = authors.replace("unknown", "")

    authors = authors.apply(lambda a: re.sub(r'and([A-Z])', r', \1', a))
    authors = authors.apply(lambda a: a.replace('and ', ','))

    authors = authors.apply(lambda a: a.replace('(series)', ''))
    authors = authors.apply(lambda a: a.replace('various authors', ''))
    
    authors = authors.apply(lambda a: re.sub(r'\[.*?\]', '', a))
    authors = authors.apply(lambda a: re.sub(r'\(as[^)]+\)', '', a))
    authors = authors.apply(lambda a: re.sub(r'\(pseudonym[^)]+\)', '', a))
    return authors

# Extracts authors from a text
def extract_authors(text): 
    if any(substring in text for substring in [" fils", " père", " III", " Sr.", " Jr."]):
        text[-1] = text[-1].replace(r'\[.*?\]', '')
        return ",".join(text[-2:])
    if len(text) > 1 :
        return text[-1]
    return None

# Extracts several features from a dataframe while sanitizing them
def extract_features(df):
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

# Filling in values "same as above" and "same as below" with the data above or below respectively
def clean_same_as_above_below(df):
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
    df.loc[df['film_adaptations'].isnull() & df['fiction_work'].notnull(), ['film_adaptations']] = df['fiction_work']
    df.loc[df['film_adaptations'] == df['fiction_work'], ['fiction_work']] = None

    # fill nan fiction_work values with the last non null value of fiction_work
    df['fiction_work'] = df['fiction_work'].ffill()
    # drop nan where both columns are nan
    df = df.dropna(subset=['film_adaptations'])

    df = extract_features(df)

    df = clean_same_as_above_below(df)

    return df
    