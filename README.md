# From Page to Screen: The Powerful Influence of Literature on Cinema ?

# Abstract 

After dropping my studies in data science, I wanted to pursue a life in my passion of all time: Literature.
Regrettably, the *industry of literature is falling* due to new technologies and social networks, and at this time, it’s becoming impossible to make a life out of writing books.
Having this bitter taste in my mouth, I decided to use my background in data science to fight for my dreams and make my books as profitable as possible.
My idea was to analyze the influence of Literature on Cinema. I wanted to understand what factors would make my books more likely to be adapted on the big screen. 
Finally, I want to make royalties, but money is not what matters most to me. What is most important is to spread my stories all around the world, and I need to analyze what divergences could appear, in order to protect my stories at all cost. 

# Research questions
We will use several questions to drive our analysis :
First, we will analyze **What kind of books are adapted to movies?** This is done through analyzing the most adapted *time periods* and *authors* book-wise, and through crossing information by analyzing the adaptation *languages*, *genres* and financing countries. This should lead us to understand which trends underline book’s adaptation through time and across countries.

Then, we will analyze the **success of the adaptations themselves**: are they more successful than non-adaptations? Is there a correlation between the success of a book and of its adaptation? This success can both be represented in terms of box-office, rating and engagement (number of reviews).

Finally, we will analyze **Do a book’s plots and its adaptation’s plot resemble each other?** This would lead us to understand to what extent are the subjects in the plots the same, or if adaptations tend to add / remove some topics. We could then understand how this correlates with the rating of users.


# Additional Datasets
## 1. Wiki/List_of_fiction_works_made_into_feature_films
We scraped.

## 2. Goodreads
It has been scraped.

## 3. IMdB
We merged CMU with two datasets from [https://developer.imdb.com/non-commercial-datasets/](IMDB’s non-commercial datasets). Both of them are small-enough (up to ~1Gb) so they can be handled without specific measures.
### title.basics
We merge the CMU dataset with title.basics on both the movie’s name and date. Special care is taken to handle the fact that IMDB has both the originalTitle or the PrimaryTitle that can match. We extract the titleId to use when merging the next dataset, and isAdult for further analysis.
### title.ratings
We merge the CMU dataset with title.ratings using the common titleId. We extract both averageRating and numVotes for further analysis.


# Methods


# Proposed Timeline


# Organization within the Team



# Questions for TAs 





## install requirements
First, install all the necessary requirements.

pip install -r pip_requirements.txt
```



### How to use the library
Tell us how the code is arranged, any explanations goes here.



## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

