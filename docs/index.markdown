---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: 'Data Alchemy: Transforming Literature into Cinema'
---

# Introduction  
After dropping my studies in data science, I wanted to pursue a life in my passion of all time: **Literature**.\\
Regrettably, the industry of literature is falling due to new technologies and social networks, and at this time, it’s becoming impossible to make a life out of writing books. Having this bitter taste in my mouth, I decided to use my background in data science to fight for my dreams and make my books as profitable as possible.\\
My idea was to analyze **the influence of Literature on Cinema**. I wanted to understand what factors would make my books more likely to be adapted to the big screen. Finally, I want to make royalties, but money is not what matters most to me. What is most important is to spread my stories all around the world, and I need to analyze what divergences could appear, in order to protect my stories at all cost.

{% include whitework.html %}

*We begin the first part of the work, also known as the Opus albedo (The Work of White) by preparing and cleaning our data. Long and toilsome, this stage is vital, as it is through this refining that we obtain a reliable and solid matter. As the alchemists of old sought to cleanse their base matter to bring forth gold, so must we cleanse our data, that it may serve as the foundation for that which is to come.*

We needed to expand our dataset to obtain information on movies adapted from books. We began to scrap book-movie adaptation pairs from wikipedia pages. We then merged with the original CMU movie dataset.
In order to gain more insights into the books, we merged our dataset with a goodreads dataset. Goodreads is a website where book aficionados can find information such as book plots and user ratings. Finally, we merged our dataset with the IMDb dataset in order to have access to user ratings for the movies this time. This came with extensive data cleaning. 
Emerging from this fusion, we obtained the dataset on which we will perform our analysis.

# Streamlining Genres for Cinematic Analysis

To streamline the analysis of movie data, we mapped 529 unique movie genres into 37 broader categories, referred to as super-genres. This mapping was necessary as many of the original genres were either identical in essence but written differently or exhibited strong similarities that made them suitable for grouping. By consolidating these genres into broader categories, the analysis becomes more manageable, reducing the number of features from 529 to 37. This simplification not only enhances the interpretability of the dataset but also facilitates more effective comparisons and insights by focusing on overarching trends rather than granular distinctions.
Dive into the details, and click on the interactive sunburst plot to explore the composition of each broader category!

{% include genre_sunburst.html %}


{% include blackwork.html %}

{% include table.html %}

![ImageTest]({{ site.baseurl }}/assets/img/graph1.png)

{% include toggler1.html %}

{% include regression_rating_summary.html %}

Now that we have purged the impurities, we must summon the courage to face the shadowed depths of our data, and delve into the dark recesses that lie within. What secrets does this matter hold, waiting to be revealed unto us?
Breaking asunder the old and the familiar, we are left with the raw and undefined form, marking the second step in this great unfolding—the Opus Nigredo, the Work of Blackening. It is the commencement of the process of separation, wherein we strive to draw forth the essence of our data.

{% include carousel_evolution.html %}

Category Evolution

{% include yellowwork.html %}

Amidst the doubts and perils that beset our journey, fate weaves our path with that of an old grimoire. This venerable tome, passed from one alchemist to another across the ages and lands , bears the chronicles of those who, in their own wise, sought to unveil the great enigma. Thus do we come to the third stage of the alchemical journey, known as the Opus Citrinum, the Work of Yellowing, where we open our eyes towards the world and the wisdom of our peers.

{% include carousel_author.html %}

Authors


{% include redwork.html %}

*In this final stage, we come unto the completion of our toil, the Opus Rubedo, the Work of Reddening. Here, we gather all the fragments of our quest, binding together the purified data and the wisdom we have wrought. Through the art of sentiment analysis, we trace the shifting paths of emotion in both the book and its film, uncovering the bond between their ratings, and revealing how one doth shape the other, as base matter is transmuted into gold.*

# Genre clustering

In order to better understand movie genres and how they interact we have applied dimensionality reduction and K-means in order to identify the main cluster and their characteristics. We chose t-SNE as our dimensionality reduction method in order to allow for non-linear relations and applied K-means after t-SNE to mitigate the curse of dimensionality as we have 30 genres and hence 30 features!

In order to pick the ideal number of clusters, we used the elbow method. 
As we can see, for adapted movies, a good number of clusters is 11. 

{% include side_by_side_images.html image1="elbow_plot_adapted.png" alt1="elbow plot for adapted movies" image2="elbow_plot_all.png" alt2="elbow plot for all movies" %}

However, for all movies the ideal number of clusters is less clear as there is no defined elbow, so we have therefore tried to find a good balance and picked 16 clusters.\\
This is interesting as it implies that adapted movies have more defined and stronger genre clusters.\\
It is quite visible when comparing the two clustering graphs ! 

{% include side_by_side_plotly.html plotly1="adapted_movies_cluster.html" plotly2="all_movies_cluster.html" %}


Let’s now dig deeper and look into the clusters of adapted movies:

[INSERT TABLE HERE]

[CLUSTER LIST]

**So to maximise your chances of success, you can have two strategies. Either you play it safe and make an animated, family friendly movie (cluster 5) in order to be universally enjoyed and have a decent box office, or you go all in: high risks but high rewards with a nice thriller (cluster 7).**

# Sentiment Analysis

The comparison of book and movie plots using sentiment analysis reveals intriguing differences and alignments in emotional representation across these two storytelling mediums. Three sentiment analysis tools were used for this purpose: VADER, a fine-tuned BERT-based classifier, and TextBlob.

### Methods and Metrics

1. VADER[1] : 
This lexicon and rule-based tool computes a compound sentiment score (ranging from -1 to +1) and proportions of text classified as positive, neutral, or negative.

2. BERT-based Classifier[2]:
 Fine-tuned on a Twitter sentiment analysis dataset, it identifies six emotions: sadness, joy, love, anger, fear, and surprise.

3. TextBlob[3]: 
Outputs include polarity, measuring sentiment from very negative to very positive, and subjectivity, assessing the degree of personal opinion or bias.

![ImageTest]({{ site.baseurl }}/assets/img/book-movie_plot_correlation.jpg)

The sentiment scores between book and movie plots showed significant Spearman correlations for most metrics which suggests that films faithfully follow book sentiment. However, certain scores exhibited notable discrepancies:

The strongest correlation was observed in negative sentiment and fear. These findings suggest that darker emotional tones and intense moments in books tend to translate effectively into their movie adaptations.

Polarity, subjectivity, love, and surprise didn’t show significant correlations between the two mediums. This discrepancy highlights potential differences in how these aspects are presented:\\
Polarity or emotional extremes in books may be softened or exaggerated in movies.

Visual storytelling in movies could introduce objectivity or dilute the personal perspective offered in books.


Love and Surprise may be interpreted differently due to pacing or narrative restructuring during adaptation.


This analysis underscores how certain sentiments, especially negative and fear-based tones, are effectively preserved in film adaptations. In contrast, emotions like love and surprise, as well as subjective viewpoints, may be more susceptible to alteration when transitioning from text to screen. However, it is important to note that the book plots and movie plots are derived from two different sources. This lack of correlation may simply reflect one plot being written more subjectively than the other.

# Linear regression

In order to understand which factors are the most important to determine success, we will use ordinary least squares (OLS) on both box office and IMDb rating. We picked OLS in order to maintain interpretability. The possible features we run the OLS on are: 
- book rating
- movie runtime
- sentiments: positive, negative, neutral, compound, polarity, subjectivity, sadness, joy, love, anger, fear, surprise
- most common languages: english, french, german, spanish
- most common genres: action & adventure, comedy, crime & gangster, drama, family & children, fantasy & science fiction, historical & period, horror & supernatural, romance & relationship, thrillers & mystery, other 

When plotting the data, we observe that the box office seems to have a heavy tailed distribution, we therefore run our regression on the log box office and see that it does indeed improve R squared (or explained variance) !

Finally, we face a serious problem with collinearity which falsifies our interpretation of the coefficients. We combat it with a technique called forward selection which greedily selects the best features until our metric isn’t improved by the addition of a new feature. We now have our most important features and can safely run OLS without fearing collinearity too much ! 

*Here are our findings:*

### Log Box Office:  a nice family outing
[INSERT BOX OFFICE OLS SUMMARY PNG HERE] 	[INSERT BOX OFFICE COEF PLOT HERE]
[TOGGLE BUTTON]

We’ll have to be careful here. As we have taken the log value of the box office, our interpretation of the coefficients will be a little different.
Each coefficient represents a multiplicative increase !  

The forward selection algorithm has picked 14 features out of the original 29: 
- movie runtime
- sentiments: sadness, subjectivity, fear
- genres: family & children, thrillers & mysteries, fantasy & science fiction, comedy, romance & relationship, historical & period, action & adventure, drama
- languages: english, spanish

We have an R squared value of 0.268 which means that we can explain 26% of box office variance. It ain’t much but it’s honest work !\\
Only subjectivity, fear, action & adventure are not significant at a 5% level.\\
Features that positively impact box office are often linked to positivity and accessibility for all. The genres associated with a good box office are mostly family friendly such as family & children, romance & relationship, comedy, fantasy & science fiction. Furthermore, sadness and drama negatively impacts box office ! 

### Movie Rating: in search of thrill
[INSERT RATING OLS SUMMARY PNG HERE] 	[INSERT RATING COEF PLOT HERE]
[TOGGLE BUTTON]

We’re in familiar territory again. The coefficient represents an additive increase !
The forward selection algorithm has picked 15 features out of the original 29: 
- movie runtime
- book rating
- sentiments: surprise, negative, neutral, compound
- genres: fantasy & science fiction, action & adventure, drama, other genre, crime & gangster, horror & supernatural
- languages:  spanish, german, french

We have an R squared value of 29.8%, not too shabby for only 15 features !

Only negative sentiment, surprise, compound sentiment and action & adventure do not have a significant pvalue at a 5% level. Negative sentiment, with a pvalue at 92% can be considered insignificant however the others should still be considered, however with a pinch of salt.\\
Interestingly, surprise positively impacts movie rating whilst neutrality negatively impacts it.
It suggests that viewers value thrills and emotions !\\
The fact that the positively impactful genres are fantasy & science fiction, drama and crime & gangster supports this claim ! However, they seem to have their limits as the horror & supernatural genre negatively impacts ratings. A bit of thrill but nothing too scary. 

### Overview: a paradox galore 

Unsurprisingly, sentiments are often insignificant. Indeed, they are the least reliable as they are calculated from the movie plot which does not perfectly transcribe movie sentiments and on top of which we use imperfect metrics.\\
Interestingly, book rating impacts movie rating significantly whilst it does not impact box office.

Furthermore, English and Spanish positively impact box office whilst French, Spanish and German positively impact movie rating !
It seems coherent that english and spanish positively impact box office as they are the two of the most widely spoken languages and it opens the movie up to a larger audience. However, interestingly when it is not the “dominant” language, users tend to be kinder and rate the movie better !

Finally, it is curious that movie runtime impacts positively (albeit timidly) both box office and movie rating. There are many possible theories, it probably stems from an unobserved covariate. Maybe famous directors have more successful movies and with a longer runtime (we’re looking at you Christopher Nolan). Maybe longer book trilogies lead to long runtimes and to greater success (hello Dune). Who knows ! But it’s a good reminder that there are still many unobserved variables which significantly impact box office and rating success. There’s still much to discover ! 


{% include conclusion.html %}
