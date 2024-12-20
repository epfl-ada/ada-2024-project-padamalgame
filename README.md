# From Page to Screen: The Powerful Influence of Literature on Cinema ?

# Website URL 
[Link to our website](https://epfl-ada.github.io/ada-2024-project-padamalgame/), we hope you enjoy :)

# Contributions
- Christelle: genre to category mapping, preliminary data analysis, graph plotting, box-office & inflation analysis, final refactoring & commenting
- Hugo: merging, interactive map, graph plotting
- Julia: scrapping, preliminary data analysis, graph plotting, category analysis and storyline
- Mallory: website, merging, storyline
- Iris: data scrapping, cleaning and merging, genre clustering, sentiment analysis, linear regression

# Abstract 


Here begins our quest to unveil the secret of transforming books into cinematic masterpieces. Just as alchemists sought to turn lead into gold, we will explore the transmutation of data into meaningful insights. Only meticulous work, data cleansing, analysis, and modeling, can reveal the full potential of a book into the big screen. We will follow the four major alchemical stages, each associated with its own color and symbolism: purification, separation, awakening, and unification. Our goal is to determine the unique characteristics of literary works that make their way to the big screen and to understand their impact on the world of cinema.


# Research questions

First Part : First Step Analysis - Category Analysis & Specificities of Adapted Book compared to Non Adapted

Which book genres are most frequently adapted into films, and how have these preferences evolved over time? What trends are revealed by the average release years of adapted movies and their source books? How do adaptations compare to original films in terms of box office performance? 

Second Part : Authorial Strategies and Global Trends in Book-to-Film Adaptations

Which authors have inspired the most cinematic adaptations, and what strategies have made their works so enduring? How do single masterpieces differ from serial or diverse storytelling approaches in terms of adaptation success? What global trends emerge in the production and reception of book adaptations? Finally, how does audience engagement vary across countries when beloved stories are brought to the big screen?

Third Part : Clustering, Sentiment Analysis & Linear Regression

This section addresses the following questions: How do genre clustering and dimensionality reduction techniques help identify patterns in adapted movie genres? What insights does sentiment analysis reveal about the emotional alignment between book plots and their film adaptations? How do linear regression models determine the factors influencing box office success and IMDb ratings? Finally, how do features like runtime, sentiment, and genre impact the performance of adaptations across different metrics?

# Additional Datasets
## 1. Wiki/List_of_fiction_works_made_into_feature_films
The foundation of our dataset on movie adaptations of books was built using data from Wikipedia's [List of Fiction Works Made into Feature Films](https://en.wikipedia.org/wiki/Lists_of_works_of_fiction_made_into_feature_films). We decided to focus on fiction and scraped all the pages under the subsection “Books”. This has allowed us to have a mapping of 4941 books to movies with book name, book authors, book year, film name and film year.


## 2. Goodreads
To enhance our dataset further, we merged it with the **Goodreads Book Dataset** available on [Kaggle](https://www.kaggle.com/datasets/bahramjannesarr/goodreads-book-datasets-10m). This dataset provides extensive metadata about books, including book genre, average rating and the rating distribution, and number of pages. 

## 3. IMdB
We merged CMU with two datasets from [IMDB’s non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/). Both of them are small-enough (up to ~1Gb) so they can be handled without specific measures.
### title.basics
We merge the CMU dataset with title.basics on both the movie’s name and date. Special care is taken to handle the fact that IMDB has both the originalTitle or the PrimaryTitle that can match. We extract the titleId to use when merging the next dataset, and isAdult for further analysis.
### title.ratings
We merge the CMU dataset with title.ratings using the common titleId. We extract both averageRating and numVotes for further analysis.



# Methods

## Data enhancement  & cleaning
We enhance our data by merging it with the IMdB databaset, the goodreads dataset, and our scrapped book to movie mapping.
We have extensively cleaned our data, particularly the scrapped Wikipedia dataset.
We mapped numerous movie genres into new movie genres with a wider sense, based on the occurrence of these genres and their nature.

## Simple analysis
We first start off with a simple exploratory analysis. We do that by plotting key insights on features such as their min/max, standard deviation, or count. We then analyse our data through aggregations according to authors, genres, countries, etc…

## Correlation 
We will look for correlations, for example : 
between the success of a book and the success of the movie
between the date of release of a book and the date of release of the movie

## Dimensionality reduction & clustering
Are there any movie genres that can be regrouped into clusters?

## Natural language processing
We will use NLP techniques and LLMs to analyze plot similarities between books and movies and attempt to evaluate how similar they are. We will also analyze the common divergences that can occur and if they impact the success.

## Linear regression
Can we predict movie success efficiently with other features and which features have the biggest coefficients





# Proposed Timeline

Step 1 : Simple analysis and correlation

Step 2 : Dimensionality reduction & clustering

Step 3 : Linear regression

Step 4 : Natural language processing

Final Step : Clean the repository in preparation of the final submit.



# Organization within the Team

We will organize weekly meetings in order to look at each steps, divide them into small tasks, and assign tasks to each team members.
We know we all have tasks we are more familiar with. Therefore, we will optimize the repartition of work. 
Moreover, we will start working on branches and do pull requests to review the code of our teammates.


## install requirements
First, install all the necessary requirements.
```
pip install -r pip_requirements.txt
```
