# From Page to Screen: The Powerful Influence of Literature on Cinema ?

# Website URL 
[Link To Our Website](https://epfl-ada.github.io/ada-2024-project-padamalgame/) We hope you enjoy :)

# Contributions
- Christelle:
- Hugo:
- Julia:
- Mallory:
- Iris:

# Abstract 

After dropping my studies in data science, I wanted to pursue a life in my passion of all time: Literature.
Regrettably, the *industry of literature is falling* due to new technologies and social networks, and at this time, it’s becoming impossible to make a life out of writing books.
Having this bitter taste in my mouth, I decided to use my background in data science to fight for my dreams and make my books as profitable as possible.
My idea was to analyze the influence of Literature on Cinema. I wanted to understand what factors would make my books more likely to be adapted to the big screen. 
Finally, I want to make royalties, but money is not what matters most to me. What is most important is to spread my stories all around the world, and I need to analyze what divergences could appear, in order to protect my stories at all cost. 


# Research questions
We will use several questions to drive our analysis :
First, we will analyze **What kind of books are adapted to movies?** How do they differ from unadapted movies ? This is done through analyzing the most adapted *time periods* and *authors* book-wise, and through crossing information by analyzing the adaptation *languages*, *genres* and financing countries. This should lead us to understand which trends underline book’s adaptation through time and across countries.

Then, we will analyze the **success of the adaptations themselves**: are they more successful than non-adaptations? Is there a correlation between the success of a book and of its adaptation? This success can both be represented in terms of box-office, rating and engagement (number of reviews).

Finally, we will analyze **Does a book’s plots and its adaptation’s plot resemble each other?** This would lead us to understand to what extent are the subjects in the plots the same, or if adaptations tend to add / remove some topics. We could then understand how this correlates with the rating of users.

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
