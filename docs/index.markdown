---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: 'Data Alchemy: Transforming Literature into Cinema'
---

# Introduction  
*Here begins our quest to unveil the secret of transforming books into cinematic masterpieces. Just as alchemists sought to turn lead into gold, we will explore the transmutation of data into meaningful insights. Only meticulous work, data cleansing, analysis, and modeling, can reveal the full potential of a book into the big screen. We will follow the four major alchemical stages, each associated with its own color and symbolism: purification, separation, awakening, and unification. Our goal is to determine the unique characteristics of literary works that make their way to the big screen and to understand their impact on the world of cinema.*


{% include whitework.html %}

*We begin the first part of the work, also known as the Opus albedo (The Work of White) by preparing and cleaning our data. Long and toilsome, this stage is vital, as it is through this refining that we obtain a reliable and solid matter. As the alchemists of old sought to cleanse their base matter to bring forth gold, so must we cleanse our data, that it may serve as the foundation for that which is to come.*

We needed to expand our dataset to obtain information on movies adapted from books. We began to scrap book-movie adaptation pairs from wikipedia pages. We then merged with the original CMU movie dataset.

In order to gain more insights into the books, we merged our dataset with a goodreads dataset. Goodreads is a website where book aficionados can find information such as book plots and user ratings. Finally, we merged our dataset with the IMDb dataset in order to have access to user ratings for the movies this time. This came with extensive data cleaning. 
Emerging from this fusion, we obtained the dataset on which we will perform our analysis.


###  Streamlining Genres for Cinematic Analysis

To streamline the analysis of movie data, we mapped 529 unique movie genres into 37 broader categories, referred to as super-genres. This mapping was necessary as many of the original genres were either identical in essence but written differently or exhibited strong similarities that made them suitable for grouping. By consolidating these genres into broader categories, the analysis becomes more manageable, reducing the number of features from 529 to 37. This simplification not only enhances the interpretability of the dataset but also facilitates more effective comparisons and insights by focusing on overarching trends rather than granular distinctions.\\
Dive into the details, and click on the interactive sunburst plot to explore the composition of each broader category!


{% include genre_sunburst.html %}


{% include blackwork.html %}

*Now that we have removed the impurities, we must confront the deeper, hidden layers of our data and explore what lies beneath. What secrets does this matter hold, waiting to be revealed ? By breaking apart the old and familiar, we reach the raw, unrefined state, marking the second step in our journey: the Opus Nigredo, or the Work of Blackening. This stage begins the process of separation, where we aim to uncover the true essence of our data.*

This section represents the first steps in exploring our data. It focuses on two main axes: time-related trends, to understand the evolution of adapted and non-adapted films, and their success, by comparing their respective performances with added granularity across genre categories. 


#  TIME: Evolution Across Eras and Genres

![Percentage of adapted movies vs non adapted per category]({{ site.baseurl }}/assets/img/Percentage_of_Movies_per_Category_Adapted_Movies_vs_Non_Adapted_Movies.png
)


Which book categories are most likely to be adapted into movies? Well, it looks like people have a soft spot for drama, adventure, and mysteries. But throw in a bit of time travel and a good laugh, and you may have a winning combination as well !

![Average Movie Year per Genre Category]({{ site.baseurl }}/assets/img/Average_Movie_Year_per_Genre_Category.png)

We then examine the average release year of movies across various categories. This reveals a rise in adaptations exploring new themes, such as LGBTQ+ narratives and cyber topics, closely tied to societal evolution. Notably, there is also a surge in animated movies, made possible by advancements in audio-visual technologies. On the flip side, some themes have been abandoned due to dwindling audience interest. The most striking, yet not surprising, example is the decline of classic and silent films.

Turn the page for even more exciting insights, where you'll discover the evolving trends of the six most represented categories among adaptations. You will notice that the distributions of both adaptations and non-adapted  movies often align, revealing a positive spearman correlation and showing how the trends are in sync whether it is based on a book or not!

{% include carousel_evolution.html %}

![Number of Adapted Movies Per Year]({{ site.baseurl }}/assets/img/Number_of_Movies_Released_Each_Year.jpg)

Looking at the number of adaptations released each year, it's clear that the early 2000s saw a significant increase in adaptations in cinema. Major literary works, like *Harry Potter and the Sorcerer's Stone* (2001) and *The Lord of the Rings: The Fellowship of the Ring* (2001), led the charge, dominating the box office and spawning iconic series. However, don’t be fooled, young fellow! While these films certainly fueled excitement for adaptations, the increase is more likely tied to the broader boom in the entertainment industry. As shown in the graph on the right, the rise in adaptations correlates closely with the overall increase in movie productions during this time, rather than a sudden surge in literary interest.towards books but as you can see on right graph would be more likely to be explain by the general rise of the entertainment industry and the significant augmentation of movie produced per year in general.

![Number of Movies per Bokk Release Date]({{ site.baseurl }}/assets/img/Number_of_Movies_per_Book_Release_Date.png)


To wrap up our journey through time, we took a look at when the books adapted into movies were originally published. And here’s the star of the show, the Gaussian distribution! It centers around the 1950s, a period that saw the publication of iconic works like *The Angel* of Elizabeth Taylor and Richard Matheson’s legendary *I Am Legend*. It seems we love to rediscover literary treasures after some time has passed. But wait, some notable peaks highlight timeless authors like Grimm and Austen from the 1800s. Could it be that age is just a number when it comes to great literature?

# SUCCESS: A First Look to the Impact of Adapted Movies

Virtus post nummos *(virtue after money)*: it is good to keep one's feet on the ground and talk about money. Is adapting books to cinema a good strategy, and does it receive success with the audience?

We took a closer look at the box office performance of adapted movies, carefully adjusting the figures for inflation to capture the real impact over time.

![Average Adjusted Box Office per Genre Category]({{ site.baseurl }}/assets/img/Average_Adjusted_Box_Office_per_Genre_Category.png)

Espionage & Spy movies dominate the list, closely followed by Horror & Supernatural. These genres seem to have a knack for captivating audiences at the time of their release, with some, like the iconic James Bond films, marking their era to become part of pop culture.

**But do adaptations actually outperform original films in profitability?**

![Average Adjusted Box Office per Genre Category Adapted vs Non Adapted]({{ site.baseurl }}/assets/img/Average_Adjusted_Box_Office_per_Genre_Category_Adapted_Movies_vs_Non_Adapted_Movies.png)

The answer appears to be a resounding yes. Adapted movies clearly have an edge over non-adapted ones in terms of box office performance, as seen in most genres. This suggests that adapting existing literary works, especially in genres with high market demand, is not only a safer bet financially but also a pathway to cultural impact. So, here’s an ironic takeaway: if your goal is to make money, creativity might be optional. Simply adapt a book!

The list of the top 10 movies with the highest adjusted box office reveals a fascinating interplay between adaptation and original screenplay. Topping the charts are iconic literary adaptations such as *Snow White and the Seven Dwarfs* (1937) and *Gone with the Wind* (1939), both timeless classics that leveraged beloved stories to captivate audiences for generations. Other adaptations, like *Bambi* (1942) and *The Exorcist* (1973), showcase the enduring power of narrative, whether enchanting or terrifying. Yet, original creations like *Star Wars : A New Hope* (1977), *Titanic* (1997), *Avatar* (2009), and *E.T. the Extra-Terrestrial* (1982) prove that unique visions can also redefine cinema, resonating deeply with audiences worldwide. This delicate balance of adapted and original works highlights how both storytelling roots and bold innovation shape the cinematic landscape.


{% include yellowwork.html %}

*Amid the challenges we face, we come across an ancient grimoire—a record passed down through generations of alchemists. This book holds the wisdom of those who sought to solve the great enigma. With this knowledge, we enter the third stage of our process, the Opus Citrinum, or the Work of Yellowing, where we broaden our perspective and draw on the insights of others.*

![Top 25 Authors]({{ site.baseurl }}/assets/img/Number_of_Movies_Adapted_from_Books_per_Author.png)

These are the authors whose books have inspired the most cinematic adaptations. While some are not to be presented anymore, this can also unveil the mind behind some heroes that are now part of our collective imagination. These authors have created works that continue to resonate across generations, but each of them has had a unique strategy in how their creations are carried forward and cherished. Let’s see what these literary alchemists can reveal to us !

{% include carousel_author.html %}

{% include toggler_worldmap.html %}

As the wise say, travel shapes the mind and our journey takes us afar ! This allows us to have a global perspective towards adapted movies on the big screen. It is clear that the U.S. takes center stage with an astonishing number of films, leaving other nations trailing far behind, most producing just a fraction of what the U.S. achieves. In fact, many countries around the world are barely represented at all. Yet, there’s a surprising consistency in average film length, with movies typically ranging from 96 to 104 minutes no matter where they’re made. Ratings show a similar alignment, though a few countries with minimal production stand out with lower scores. The average number of votes per film also follows this trend, except for standout cases like the United Arab Emirates, where only three films have garnered an unusually high level of attention.

When we narrow our focus to book adaptations, the story takes an intriguing turn: while most trends stay consistent, there’s a remarkable surge in audience engagement, with many countries seeing significantly higher vote counts for adaptations. This highlights the global appeal and impact of bringing beloved books to the big screen. We encourage you to explore this map by yourself!


{% include redwork.html %}

*In this final stage, we come unto the completion of our toil, the Opus Rubedo, the Work of Reddening. Here, we gather all the fragments of our quest, binding together the purified data and the wisdom we have wrought. Through the art of sentiment analysis, we trace the shifting paths of emotion in both the book and its film, uncovering the bond between their ratings, and revealing how one doth shape the other, as base matter is transmuted into gold.*

# Genre clustering

In order to better understand movie genres and how they interact we have applied dimensionality reduction and K-means in order to identify the main clusters and their characteristics. We chose t-SNE as our dimensionality reduction method in order to allow for non-linear relations and applied K-means after t-SNE to mitigate the curse of dimensionality as we have 30 features !

In order to pick the ideal number of clusters, we used the elbow method. 

{% include side_by_side_images.html image1="elbow_plot_adapted.png" alt1="elbow plot for adapted movies" image2="elbow_plot_all.png" alt2="elbow plot for all movies" %}

As we can see, for adapted movies, a good number of clusters is 11. 

However, for all movies the ideal number of clusters is less clear as there is no defined elbow, so we have therefore tried to find a good balance and picked 16 clusters.\\
This is interesting as it implies that adapted movies have more defined and stronger genre clusters.\\
It is quite visible when comparing the two clustering graphs!

{% include side_by_side_plotly.html plotly1="adapted_movies_cluster.html" plotly2="all_movies_cluster.html" %}

Let’s now dig deeper and look into the clusters of adapted movies:

{% include adapted_movies_cluster_stats.html %}

**Overall statistics**\\
avg box office: 7.84e+07\\
variance box office: 1.41e+08\\
avg rating: 6.45\\
variance rating: 254


**Cluster 0**\\
This cluster is very average. Average box office, average rating, most common genres. You get the picture, it’s the average Joe… It helps to explain why it is also one of the biggest clusters !

**Cluster 1**\\
It regroups horror, thriller and sci-fi. This one will get your heart beating. It is one of the biggest clusters (to my great regret…) It is quite successful at the box office on average however these movies seem to be hit or miss as the variance is quite high. The rating on the other hand is systematically low …

**Cluster 2**\\
Here we have old school movies. Silent films, classics, gangster movies, period pieces, you name it. Unfortunately for the nostalgic folk, they aren’t very successful as they have a low box office (which is likely due to inflation!) and low rating on average, along with a low variance for both. 

**Cluster 3**\\
Nothing to see here… Similar to cluster 0, with less romance and more family movies. 

**Cluster 4**\\
We now have family and kid oriented movies. Prepare yourself for lots of animations, comedy and fantasy. It is the best performing cluster on rating, with the highest average and lowest variance ! It does not shine as bright with its box office, however it is nonetheless a promising cluster.

**Cluster 5**\\
It mixes action, comedy, sci-fi and thriller. An unnoteworthy cluster with consistently low box office and rating.

**Cluster 6**\\
This cluster is for thrill chasers with crime, action and horror. A good performer at the box office, although somewhat unsteady, and an average and unvarying rating.

**Cluster 7**\\
A cluster for the nostalgic romantic with a whimsical soul. It is the highest performing cluster in terms of box office. Romance wins again !

**Cluster 8**\\
An alliance of family movies, comedy and musicals: a more lighthearted cluster.
It has the lowest box office and highest rating variance which suggests mixed reviews…

**Cluster 9**\\
We’ve seen it before, a blend of action, thriller and fantasy, but this time with a historical twist ! Not a very promising cluster with a high variance, mediocre box office and a low rating… 

**Cluster 10**\\
The smallest cluster, featuring niche and classic genres. It has the third-highest box office average but significant variability. These movies seem to leave the public unimpressed according to average rating. 

**Conclusion**\\
So to maximise your chances of success, you can have two strategies. Either you play it safe and make an animated, family friendly movie (cluster 4) in order to be universally enjoyed and have a decent box office, or you go all in: high risks but high rewards with a whirlwind romance (cluster 7).


# Sentiment Analysis

The comparison of book and movie plots using sentiment analysis reveals intriguing differences and alignments in emotional representation across these two storytelling mediums. Three sentiment analysis tools were used for this purpose: VADER, a fine-tuned BERT-based classifier, and TextBlob.

### Methods and Metrics

1. VADER[1]:\\
This lexicon and rule-based tool computes a compound sentiment score (ranging from -1 to +1) and proportions of text classified as positive, neutral, or negative.

2. BERT-based Classifier[2]:\\
Fine-tuned on a Twitter sentiment analysis dataset, it identifies six emotions: sadness, joy, love, anger, fear, and surprise.

3. TextBlob[3]:\\
Outputs include polarity, measuring sentiment from very negative to very positive, and subjectivity, assessing the degree of personal opinion or bias.

![Movie Plot Correlation]({{ site.baseurl }}/assets/img/book-movie_plot_correlation.jpg)

The sentiment scores between book and movie plots showed significant Spearman correlations for most metrics which suggests that films faithfully follow book sentiment.\\
However, certain scores exhibited notable discrepancies:

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

When plotting the data, we observe that the box office seems to have a heavy tailed distribution, we therefore run our regression on the log box office and see that it does indeed improve R squared (or explained variance)!

Finally, we face a serious problem with collinearity which falsifies our interpretation of the coefficients. We combat it with a technique called forward selection which greedily selects the best features until our metric isn’t improved by the addition of a new feature. We now have our most important features and can safely run OLS without fearing collinearity too much ! 

*Here are our findings:*

### Log Box Office:  a nice family outing
{% include side_by_side_images.html image1="log_boxoffice_regression.png" alt1="box office regression" image2="log_boxoffice_regression_coef.png" alt2="box office regression coef" %}

We’ll have to be careful here. As we have taken the log value of the box office, our interpretation of the coefficients will be a little different.
**Each coefficient represents a multiplicative increase !**

The forward selection algorithm has picked 14 features out of the original 29: 
- movie runtime
- sentiments: sadness, subjectivity, fear
- genres: family & children, thrillers & mysteries, fantasy & science fiction, comedy, romance & relationship, historical & period, action & adventure, drama
- languages: english, spanish

We have an R squared value of 0.268 which means that we can explain 26% of box office variance. It ain’t much but it’s honest work !

Only subjectivity, fear, action & adventure are not significant at a 5% level.\\
Features that positively impact box office are often linked to positivity and accessibility for all. The genres associated with a good box office are mostly family friendly such as family & children, romance & relationship, comedy, fantasy & science fiction. Furthermore, sadness and drama negatively impacts box office ! 

### Movie Rating: in search of thrill
{% include side_by_side_images.html image1="rating_regression.png" alt1="rating regression" image2="rating_regression_coef.png" alt2="rating regression coef" %}

We’re in familiar territory again. **The coefficient represents an additive increase !**

The forward selection algorithm has picked 15 features out of the original 29: 
- movie runtime
- book rating
- sentiments: surprise, negative, neutral, compound
- genres: fantasy & science fiction, action & adventure, drama, other genre, crime & gangster, horror & supernatural
- languages:  spanish, german, french

We have an R squared value of 0.268 which means that we can explain 26% of box office variance. It ain’t much but it’s honest work !\\ 
Only negative sentiment, surprise, compound sentiment and action & adventure do not have a significant pvalue at a 5% level. Negative sentiment, with a pvalue at 92% can be considered insignificant however the others should still be considered even if it is with a pinch of salt.\\
Interestingly, surprise positively impacts movie rating whilst neutrality negatively impacts it.\\
It suggests that viewers value thrills and emotions.\\
The fact that the positively impactful genres are fantasy & science fiction, drama and crime & gangster supports this claim. However, there seems to be a limit as the horror & supernatural genre negatively impacts ratings. A bit of thrill but nothing too scary !


### Overview: a paradox galore 

Unsurprisingly, sentiments are often insignificant. Indeed, they are the least reliable as they are calculated from the movie plot which does not perfectly transcribe movie sentiments, on top of which we use imperfect metrics.\\
Interestingly, book rating impacts movie rating significantly whilst it does not impact box office.\\
Furthermore, English and Spanish positively impact box office whilst French, Spanish and German positively impact movie rating !

It seems coherent that english and spanish positively impact box office as they are two of the most widely spoken languages and hence open the movie up to a larger audience. However, interestingly when it is not the “dominant” language, users tend to be kinder and rate the movie better ! 

Finally, it is curious that movie runtime impacts positively (albeit timidly) both box office and movie rating. There are many possible theories; it probably stems from an unobserved covariate. Maybe famous directors have more successful movies with a longer runtime (we’re looking at you Christopher Nolan). Maybe longer book trilogies lead to longer runtimes and to greater success (hello Dune). Who knows ! But it’s a good reminder that there are still many unobserved variables which significantly impact box office and rating success. There’s still much to discover ! 


{% include conclusion.html %}

*And so, we reach the end of this journey, where books and cinema converge in the same vision. Along the way, we’ve uncovered the intricate processes that shape raw narratives into cinematic marvels and seen how these adaptations leave their mark on the world of the silver screen. This is not just an end but an invitation, a reminder of the enduring power of storytelling to bridge worlds and create something entirely new, one frame and one word at a time.*


# Bibliography
[1] https://github.com/cjhutto/vaderSentiment\\
[2] https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion\\
[3] https://textblob.readthedocs.io/en/dev/index.html
