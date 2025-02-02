# Documentation for Team: ML Freunde

This is the documentation for the forked repository of Magnus Müller, Maximilian Kalcher and Samuel Hagemann. 

Please refer to our [README.md](README.md) for the source code and practical guide on how to get the project running. 

Our task involved building and documenting a real-life application of a machine learning task. We were given a [dataset](https://www.kaggle.com/ruchi798/data-science-tweets) of 295811 tweets about data science from the years 2010 until 2021 and had to build a classifier that would detect whether a tweet would go viral or not. The measure for it being viral was when the sum of likes and retweets were bigger than 50, which resulted in 91% false (or non-viral) labels, and 9% true (or viral) labels.

Our work consisted of a number of steps in a pipeline, in summary: We loaded and labeled the data using the framework given to us by Bechberger. We then preprocessed the data, mainly the raw tweet, to better fit our feature extraction later. This was done by removing punctuation, stopwords, etc. and also tokenizing into single words. After this, we extracted a handful of features which we found to be of importance, some were already included in the raw dataset columns, some we had to extract ourselves. Since the feature space was not exactly very large and mostly overseeable, we did not apply any dimensionality reduction other than what was already implemented. So after the features, we headed straight into classification using a variety of classifiers and benchmarks for evaluation. 

![1](/Documentation/1.png)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[1] From preprocessing to evaluation

<br />

At the end, our best classifier is implemented into an 'application', callable by terminal, which gives the likeliness of an input tweet being viral, having used the features as training. 

![2](/Documentation/2.png)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[2] Generalizing new instances via the application

<br />

This pipeline is documented more in detail below.

## Preprocessing

Before having used any data of columns such as the raw tweets, it was important for us to process parts of it beforehand so our chosen features could be extracted smoothly. The first thing we noticed was that many tweets had different kinds of punctuation, stopwords, emojis, and some of them even were written in different languages.

Since we found it interesting from the start to use some NLP features like the semantics of words alongside other features, we aimed to keep the core words of the tweet only.

### Design Decisions

To achieve to only keep the core words of a tweet, we used the following data cleaning methods: 

<br />
<br />

1. *Removing punctuation and digits*

We knew that tweets can sometimes use extensive punctuation, which would be a problem for later features and/or the tokenizer, since it detects punctuation as a token too. We chose to remove any written digits as well to only keep strings. With the help of the ```string``` package, we filtered out most punctuation and digits, namely: ```['!"#$%&\'()*+, -./:; <=>?@[\\]^_ ` {|}~0123456789]``` . But we also had to add some other special characters that the package did not pick up, and were still being present after the cleaning: ```[’—”“↓']``` . 

Example: 

Input: | Output: 
-------|--------
`Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp ` | `Red Black tree AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops Data Science roles 😏 httptcoQrKYJpiiVp`

<br />
<br />

2. *Removing stopwords*

For the sake of only using important words for our features, we removed so called stopwords, or filler words used commonly in sentences. This was possible with the ```nltk``` package. So for each word in the tweet, any word that was equal to the corpus of stopwords was removed :

```
{'a',
 'about',
 'above',
 'after',
 'again',
… 
 'your',
 'yours',
 'yourself',
 'yourselves'}
 (179 total) 
```

Example: 

Input: | Output: 
-------|--------
`Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp` | `Red Black tree, AVL Tree Algorithms like Bellman ford etc asked interviews even Devops, Data Science roles 😏 httptcoQrKYJpiiVp`

<br />
<br />

3. *Removing emojis*

In between the now usable words, we found some tweets had emojis. This of course was not a string and since interpretability of emojis by encoding and decoding into ASCII was a little difficult, we chose to just remove them from the tweet. 

Seeing as how the decoded emojis all start with ```\UXXXX``` followed by a set of numbers and letters, we just removed every string that started or contained ```\U``` after being decoded (contained - because some emojis were written without spacing and recognized as a single string). 

Example: 

Input: | Output: 
-------|--------
` Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp` | `Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles httptcoQrKYJpiiVp`

<br />
<br />

4. *Removing links*

We thought we had finished the cleaning part, since there was finally only text in a tweet. But we quickly found that links were also recognized as strings, and were practically unusable for us. So we also removed any string that started with ```http``` . 

Example: 

Input: | Output: 
-------|--------
`Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp` | `Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏`

<br />
<br />

5. *Tokenizing tweet*

After these important cleaning steps, we took all words in the tweet and tokenized them for easier feature extraction when dealing with NLP features, because we would then just be iterating over a list or core words. This tokenizer is built using ```nltk``` and was already implemented in one of the seminar sessions. 

Every part of the string that is not a whitespace or ```’ ‘``` is then added onto a list of so-called tokens that represent the words in the sentence. We didn’t want to overwrite the normal preprocessed tweet, because of further features that would not need tokens, so we decided to just insert an extra preprocessing column only for these tokenized words. 

Example: 

Input: | Output: 
-------|--------
`Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp` | `[‘Red’, ‘Black’, ‘tree’, ’, ’, ‘AVL’, ‘Tree’, ‘and’, ‘other’, ‘Algorithms’, ‘like’, ‘Bellman’, ‘ford’, ‘etc’, ‘are’, ‘asked’, ‘in’, ‘most’, ‘interviews’, ‘even’, ‘on’, ‘Devops’, ‘, ’, ‘Data’, ‘Science’, ‘roles’, ‘😏’, ‘httptcoQrKYJpiiVp’ ]`

<br />
<br />

6. *Setting language to only english*

Taking a closer look at the languages of our tweets, our analysis summary was the following: 

{'en': 282035, 'it': 4116, 'es': 3272, 'fr': 2781, 'de': 714, 'id': 523, 'nl': 480, 'pt': 364, 'ca': 275, 'ru': 204, 'th': 157, 'ar': 126, 'tl': 108, 'tr': 84, 'hr': 68, 'da': 66, 'ro': 60, 'ja': 58, 'sv': 42, 'et': 29, 'pl': 25, 'bg': 24, 'af': 23, 'no': 21, 'fi': 20, 'so': 16, 'ta': 16, 'hi': 11, 'mk': 11, 'he': 9, 'sw': 9, 'lt': 7, 'uk': 6, 'sl': 6, 'te': 5, 'zh-cn': 5, 'lv': 5, 'ko': 5, 'bn': 4, 'el': 4, 'fa': 3, 'vi': 2, 'mr': 2, 'ml': 2, 'hu': 2, 'kn': 1, 'cs': 1, 'gu': 1, 'sk': 1, 'ur': 1, 'sq': 1}

It turns out, from the total 295811 samples, 95% were english tweets. The rest would be pretty much unusable for our subsequent NLP-based features, so we chose to remove that 5% portion from our preprocessed data. 

<br />
<br />

7. *Setting all words to lowercase*

Our final preprocessing step was only implemented after having examined keywords for the feature extraction and found out that many words on ‘most used words’ analysis had appeared twice. This was because sometimes people would write them with lower and uppercase. So we just went back into the code and made sure to append all strings to our preprocessing columns with ```.lower()``` , making all words lowercase. 

Example: 

Input: | Output: 
-------|--------
`Red Black tree, AVL Tree and other Algorithms like Bellman ford etc are asked in most interviews even on Devops, Data Science roles 😏 httptcoQrKYJpiiVp` | `red black tree, avl tree and other algorithms like bellman ford etc are asked in most interviews even on devops, data science roles 😏 httptcoQrKYJpiiVp`

<br />
<br />

### Results

At the end of our preprocessing, we had created 2 new columns: ```preprocess_col``` for the general feature extraction and ```preprocess_col_tokenized``` for the feature extraction based on the word level (semantics). 

Our resulting columns from a raw tweet looks like this: 

tweet | preprocess_col | preprocess_col_tokenized
------|----------------|-------------------------
Some solid #datascience podcasts here. And one looks super familiar... 😎 Check it out 👇  https://t.co/Lhrkp4FCoc | solid datascience podcasts one looks super familiar check | ['solid', 'datascience', 'podcasts', 'one', 'looks', 'super', 'familiar', 'check'] 

Looking at this from a different perspective, we can count how much of the original dataset was removed solely based on the character count: 

```
Number of characters before preprocessing: 52686072
Number of characters after preprocessing: 32090622
Removed: 20595450 (39.1 %)
```

At the end of our preprocessing, almost 60% of the original data was used and worked with. 

## Feature Extraction

The dataset was very variable and we had a lot of features to work with, which gave us the freedom to choose and experiment with these freely. We chose to extract two types of features: 

a) Features about special characters and metadata, and <br />
b) Features about natural language, word similarity and frequency

These features are appended to the preprocessed dataset as new columns and can be inspected in the ```features.csv``` file in the feature extraction folder. Below we listed all extracted features and their explanation. 

### Design Decisions

Below are listed all implemented features and their explanation. 

<br />
<br />

1. *Photo Bool*

We implemented a simple feature that would tell whether the tweet under consideration contains one (or even multiple) photos or not. The idea behind this was that tweets with visual stimulus are more appealing and would therefore be more likely to go viral. 

The possible outputs are either ```[1]``` if the tweet contains photo(s) and ```[0]``` if it does not. If we have 5 tweets that either contain videos or not, an exemplary output could be: ```[[1], [0], [0], [1], [0]]```

<br />
<br />

2. *Video Bool*

Also, we were interested in the possible effect of video(s) in the tweets and implemented it as a feature in a similar way to the photo feature. This feature will tell whether the tweet under consideration contains video(s) or not. The possible outputs are either ```[1]``` if the tweet contains video(s) and ```[0]``` if it does not. If we have 5 tweets that either contain videos or not, an exemplary output could be: ```[[0], [1], [0], [1], [1]]```

Since this feature was already integrated in the raw dataset, we just had to extract the values of this column. 

<br />
<br />

3. *Hashtag Counter*

We also thought about the importance of hashtags. Since using a hashtag increases the engagement of tweets by tagging similar topics together, having more hashtags would mean that more people could be reached for a variety of topics and the tweet is more likely to become viral. Because of this, we implemented a feature that counts the number of hashtags a tweet has. If we have 5 tweets that contain different number of hashtags, an exemplary output could be: ```[[0], [5], [2], [3], [1]]```

<br />
<br />

4. *Emoji Counter*

According to a [study](https://knepublishing.com/index.php/KnE-Social/article/view/4880/9771#toc), emojis have not only become a visual language used to reveal several things (like feelings and thoughts), but also part of the fundamental structure of texts. They have shown to convey easier communication and strengthen the meaning and social connections between users. 

Because of this, we thought it would be very fitting to add a feature about emojis. So we took the original unprocessed tweets again, and counted every occurrence of strings that started or contained ```\U``` after being decoded. This number was then added to a new column as a feature to show that using a n > 0 number of emojis would increase the attractiveness of the tweet. If we have 5 tweets that contain different number of emojis, an exemplary output could be: ```[[0], [5], [2], [3], [1]]```

<br />
<br />

5. *Tweet length*

This feature was already implemented, so we did not add anything to it. We did find this very interesting though. According to a 2013 [paper](https://www.researchgate.net/publication/262166912_Analyzing_and_predicting_viral_tweets) trying to analyze why tweets became viral, most viral tweets back then had less than 140 characters. This means that a shorter and precise tweet would perform better than a longer tweet conveying more information.

This feature just counts the entire tweet string and adds the value to a new feature column. If we have 5 tweets of different length, an exemplary output could be: ```[[45], [14], [41], [30], [12]]```

<br />
<br />

6. *Hour of tweet*

The last feature about the tweet metadata is about the posting time of the tweet. We wanted to know if there was a difference in the posting times in viral and non-viral tweets. The following two graphs represent the tweet frequency per hour of posting. 

![time_non_viral](/Documentation/time_non_viral.png)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[3] Hour frequency of non-viral tweets [0-24]

![time_viral](/Documentation/time_viral.png)

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[4] Hour frequency of viral tweets [0-24]

Interestingly enough, both viral and non-viral tweets are distributed pretty much equally except for a timeframe of about 3 hours in the morning from 7:00 - 10:00. This is where the viral tweets tend to be tweeted more. Using this information, we stripped the hour from the ```time``` column of the raw dataset and added this as a feature in a new column ```time_hours```. So for a time of ```12:05:45``` the feature would just extract the number ```12```. If we have 5 tweets of posting times, an exemplary output could be: ```[[12], [14], [3], [4], [0]]```

<br />
<br />

7. *Word2Vec*

We then started to analyze features about semantics and natural language. The first thing that came to mind was seeing if there was a different word usage comparing the viral and non-viral tweets. The two graphs below show the 20 most used words in both categories:

![word_count_non_viral](/Documentation/word_count_non_viral.png)

&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; [5] Top 20 most used words in non-viral tweets (label == False)

![word_count_viral](/Documentation/word_count_viral.png)

&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; [6] Top 20 most used words in viral tweets (label == True)

What we can gather from this is that both categories seem to use the word ‘data’, followed by ‘datascience’  the most. This is not surprising, as the entire dataset is about data-science related tweets. Applying a word embedding feature using these words would not make much sense, as the feature would score equally high for the majority of both viral and non-viral tweets. So we had to differentiate between the categories and find words that were only present in the top 20 words in viral tweets, and not in non-virals. Since we used a dataset of embedded words from google news ( ```'word2vec-google-news-300'``` ), the keywords had to be present there and could not be too specific (deepleaning, datascience, etc. did not exist). We then settled with the following words: 

 ` keywords  = ['coding', 'free', 'algorithms', 'statistics'] `

These words were present in the dataset for word embeddings and were also exclusively used in viral tweets. 

Using the package ```gensim``` for computing word embeddings and semantic similarity, we could easily iterate over all words in ```preprocess_col_tokenized``` and compare each word there with each word in our ```keyword``` list. For every (tokenized) tweet, we took the mean of all similarity values and added this float number to a new feature column ```word2vec``` . For example, using the keywords stated above and 2 sentences: 

```
keywords  = ['coding','free','algorithms','statistics'] 

['i', 'love', 'free', 'coding', 'courses'] = 0.1786
['i', 'will', 'make', 'some', 'pizza', 'today'] = 0.0890
```

We can see that the first sentence obvioulsy has more to do with the given keywords than the second sentence, and our word2vec score reflects this. 

<br />
<br />

8. *Hashing Vectorizer*

We also wanted to try something we didn't hear in the lecture. Therefore, we used a function called ```HashingVectorizer``` from ```sklearn``` to create an individual hash for each tweet. It is mainly used for converting a collection of text documents to a matrix of token occurances. But in our case, it worked just as well by using it to compare across all preprocessed tweets for some kind of similarity. It also performs really well and uses low memory. For a sentence like 'I love Machine Learning', the output can look like this depending on the number of ```features``` (argument in function): 

```
[0.4, 0, 0, 0, 0.21, 0.25, 0, 0.3]
```

Which is basically a very high dimensional but sparse matrix of values. <br />

After experimenting around for a bit, we found that this function yields some interesting results. After converting the column ```preprocessed_col_tokenized``` into a sparse matrix with 2^3 = 8 features via the HashingVectorizer, our feature looked like this: 

```
[[-0.22941573  0.          0.         -0.45883147 -0.22941573  0.
   0.45883147 -0.6882472 ]
 [ 0.35355339 -0.70710678  0.35355339  0.         -0.35355339  0.
   0.35355339  0.        ]
 [ 0.52522573 -0.13130643  0.13130643 -0.52522573  0.          0.26261287
  -0.52522573  0.26261287]
 [-0.33333333 -0.66666667 -0.33333333 -0.33333333  0.          0.
   0.33333333 -0.33333333]
 [-0.57735027  0.          0.          0.          0.          0.
   0.57735027 -0.57735027]
   ...]
```

Each row representing a vectorized tweet. To see if there was still structure in the data after the hashing, we used the newer cluster algorithm ```DBSCAN``` from ```sklearn``` to cluster this newly formed data and give us some unique labels for us to examine. For the entire data, there seemed to be about 8 unique clusters (-1 being noise): `[0, -1, 6, 1, 2, 5, 3, 4, 7]`. If we now reverse the search and look for each label, we could spot some interesting findings. Taking a look at a few instances of cluster `4`, we can see that almost all of them include the words 'data analysis' in some way: 

```
['email', 'UMich', 'Dean', 'Today', 'Provost', 'told', 'scientists', 'labs', 'closed', 'instead', 'work', 'activities', 'completed', 'remotely', 'writing', 'papers', 'grant', 'proposals', 'completing', 'data', 'analysis'] 

['Heres', 'chance', 'identify', 'skills', 'needed', 'future', 'amp', 'plan', 'tomorrow', 'without', 'neglecting', 'today', 'FutureOfWork', 'YourStory', 'set', 'bring', 'together', 'CTOs', 'CPOs', 'data', 'science', 'heads', 'amp', 'tech', 'architects', 'help', 'stay', 'ahead', 'curve', 'FOW'] 

['new', 'DSDimensions', 'data', 'analysis', 'HeleneDraux', 'juergenwastl', 'Digital', 'Science', 'Consultancy', 'confirms', 'COVIDs', 'negative', 'impact', 'proportion', 'women', 'first', 'authors', 'journal', 'articles', 'DavidMJourno', 'timeshighered', 'discusses', 'findings'] 

['Basic', 'Data', 'Analysis', 'following', 'PeoplePerHour', 'project', 'posted', 'Monday', 'th', 'December', 'PM', 'httpbitlyeeEXU']
```

While cluster `2` gives us very short tweets about data: 

```
['Data', 'Science', 'httptcoJBiTdO', 'bigdata'] 

['Intro', 'Data', 'Science', 'November'] 

['lil', 'data', 'visualization', 'guys'] 

['data', 'science', 'team', 'culturintel'] 

['Rules', 'Live', 'Work', 'DataScience'] 
```

This indirectly means, that the HashingVectorizer does not only take into account word counts in relation to the entire data, but also somehow gathered that the short tweets above were somehow similar. It's not very intuitive to humans why this works, because it sometimes involves creating a large output for a little input in a high dimensional space, but we thought it was a cool feature nonetheless and added it into column ```tweet_hashvector```. In normal practical cases, this is used with 2^20 features, which are about 1048576 features. In our version, we increased the function parameter from (length) 8 to 2^17 = 131072 features. 

We also know that ```sklearn``` has the ```Tf Idf``` ( Term Frequency Inverse Document Frequency ) function, that also generates sparse matrices based on the overall weight of words in documents. But we chose not to use this, as the HashingVectorizer does almost the same thing and we found it to be more meaningful.

<br />
<br />

### Results and interpretation

As a result of our feature extraction, we successfuly extracted 8 unique features to use in the classification step. We also implemented a ```features.csv``` file to examine if the features were extracted correctly, these final columns for classification are shown below. Important note: feature number 8 (HashingVectorizer) is not included here due to its length. 

tweet_charlength	| hashtags_hashtag_count	| tweet_emoji_count |	photos_bool |	video_bool |	tweet_word2vec |	time_hours
-----------------|-------------------------|-------------------|-------------|------------|----------------|---------
221.0 | 16.0 |	0.0 |	1.0 |	1.0 |	0.10604091733694077 |	10.0
100.0 | 1.0 |	0.0 |	0.0 |	0.0 |	0.07567958533763885 |	13.0
192.0 | 7.0 |	0.0 |	0.0 |	0.0 |	0.0994858369231224 |	20.0
207.0 | 12.0 |	0.0 |	1.0 |	1.0 |	0.13340184092521667 |	9.0
74.0  | 2.0 |	0.0 |	1.0 |	1.0 |	0.09417513012886047 |	4.0
... | ... | ... | ... | ... | ... | ...

Another important point to mention regarding the HashingVectorizer feauture, is that because it outputs multiple values (in our case a list of 131072 features per tweet), it had to fit our framework of unique values per feature column. Due to this, we extracted all 131072 features and added them to individual columns alongside the 7 features above, making the feature space of length ( _ ,131079). We also decided to do this to avoid any kind of feature outweighing that might occur. 

## Dimensionality Reduction

At first, we tried reducing the dimensionality using a few methods like the `sklearn` integrated PCA. But when looking at the before and after results, it did not change much, and even changed crucial parts about the HashingVectorizer which even sometimes affected the performance negatively. At the end, we only kept the dimensionality reductor that was already implemented, namely being the ```K-Best selector``` using mutual information. But we did not use any form of dimensionality reduction in our working pipeline due to the reasons stated. 

## Classification

Since we did not inherently know which type of classifier would preform the best, we chose to implement as many as possible of which their description still fitted the task at hand. Note: some classifiers required a ```StandardScaler()``` function provided form ```sklearn``` to work, this pipeline addition is not stated in the points below, but can be traced in the code structure. 

### Design Decisions

Below are listed all classifiers we used, including their hyperparameter tuning. 

<br />
<br />

1. *Majority classifier* 

`DummyClassifier(strategy="stratified", random_state=args.seed)`

* strategy="stratified" : generates predictions by respecting the training set’s class distribution
* random_state=args.seed : Save the seed for replicability
<br />

2. *Frequency classifier*

`DummyClassifier(strategy="most_frequent", random_state=args.seed)`

* strategy="most_frequent" : always predicts the most frequent label in the training set
* random_state=args.seed : Save the seed for replicability
<br />

3. *SVC (SVM)*

`SVC(probability=True, verbose=verbose)`

* probability=True : Enable probability estimates 
* verbose=verbose : Show progress bar in output
<br />

4. *KNN*

`KNeighborsClassifier(args.knn, n_jobs=-1)`

* args.knn : Number of neighbors (in our case: 4)
* n_jobs=-1 : Use all (computer) processors and run all jobs in parallel 
<br />

5. *SGDC classifier*

`SGDClassifier(class_weight=balanced, random_state=args.seed, n_jobs=-1, verbose=verbose)`

* class_weight=balanced : Use the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as `n_samples / (n_classes * np.bincount(y))`
* random_state=args.seed : Save the seed for replicability
* n_jobs=-1 : Use all (computer) processors and run all jobs in parallel 
* verbose=verbose : Show progress bar in output
<br />

6. *Multinomial NB*

`MultinomialNB(random_state=args.seed)`

* random_state=args.seed : Saving the seed for replicability
<br />

7. *Linear SVC*

`LinearSVC(class_weight=balanced, random_state=args.seed, verbose=verbose)`

* class_weight=balanced : Use the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as `n_samples / (n_classes * np.bincount(y))`
* random_state=args.seed : Save the seed for replicability
* verbose=verbose : Show progress bar in output
<br />

8. *Logistic Regression*

`LogisticRegression(class_weight=balanced, n_jobs=-1, random_state=args.seed, verbose=verbose, max_iter=1000)`

* class_weight=balanced : Use the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as `n_samples / (n_classes * np.bincount(y))`
* n_jobs=-1 : Use all (computer) processors and run all jobs in parallel 
* random_state=args.seed : Save the seed for replicability
* verbose=verbose : Show progress bar in output
* max_iter=1000 : Maximum number of iterations taken for the solvers to converge (in our case: 1000)
<br />
<br />

### Results and interpretation

Most classifiers worked fine but some of them took way longer than expected, which was a little bit of a setback and the reason why we added a new argument: ```--small X``` which would just use X tweets for quick testing. This helped testing out classifiers little by little and also helped with the debugging. 

What we learnt from trying each of the above listed classifiers is that each behaves very differently and not all of them were useful. Starting with the first two, the Majority and Frequency classifier from `sklearn`'s ```DummyClassifier``` were almost completely unusable to us. These are swiftly followed by the `MultinomialNB` classifier which does not take negative inputs, rendering it useless due to the negative values from the HashingVectorizer. The `KNN` classifier worked alright at first, but after tuning it, we did not see any major improvements in performance. It also takes a long time since it keeps the inputs in memory. The normal `SVC (SVM)` worked well with small samples (<10000), but was also almost unusable with the entire dataset, since the time increases quadratically per sample. Using the `LinearSVC` classifier for larger datasets (since it scales better on more samples) turned out to work alright. Another linear classifer was the `SGDClassifier`, which used previous models like the support vector machine (SVM) alongisde stochastic gradient descent (SGD) learning. This classifier was very quick (convergence after 371 epochs took 41.24 seconds) but gave average results. Our best classifer was `LinearRegression` which converged on the training after 3850 iterations and 7.5 min. This is also the classifier that made the most sense for our features since they are mostly linearly separable and we are trying to classify binary outcomes (viral/non-viral).

## Evaluation

### Design Decisions

For our evaluation and to avoid a combinatorial feature evaluation problem, we only picked our top 3 classifers that worked well within our expectations, namely being the SGDClassifier, linear SVC and logistic regression classifier. 

To evaluate our 3 classifiers, we mainly used the integrated ```classification report``` (including precision, recall, f1-score) from ```sklearn.metrics```, as well as single metric functions like the ```accuracy_score```, ```balanced_accuracy_score``` and the ```cohen_kappa_score```. 

We first used all the described functions in our given pipeline. We found that our pipeline had some drawbacks: for example, it could be very complicated, especially for beginners, telling which output files are used as input in the next files since there are so many steps. Also, we had to create a new column in our feature extraction dataset for each dimension to deal with the HashVectorizer. As a result, the pipeline was very slow and our classifier results were unsatisfactory. To overcome these challenges, we created a new pipeline by using the power of the `sklearn` integrated pipeline function in `all_in_one_multiple_input_features.py`.

### Results

The first part of this section is about the results of our old pipeline. In the second part we use the new pipeline, which gave us the opportunity to work faster and giving us better results overall. In the final section, we show some experimental tests using the classifiers and features. 

Note: all evaluation results refer to the _validation_ set. 

<br />
<br />

#### A) *Old Pipeline*

For our 3 classifiers mentioned above, we ran each classifier using _all_ features from the feature extraction. 


<br />

1. *SGDC classifier*

Summary: 
```
Accuracy: 0.631602174834063
Cohen's kappa: 0.10319595346840948
Balanced accuracy: 0.6242586916278406
```

Detail:
```
              precision    recall  f1-score   support

        Flop       0.94      0.63      0.76     51314
       Viral       0.15      0.62      0.24      5334

    accuracy                           0.63     56648
   macro avg       0.55      0.63      0.50     56648
weighted avg       0.87      0.63      0.71     56648

```
<br />

2. *Linear SVC*

Sumary: 
```

Accuracy: 0.8826907687238149
Cohen's kappa: 0.04342920171916376
Balanced accuracy: 0.5156113883206965

```

Detail:
```
              precision    recall  f1-score   support

        Flop       0.91      0.97      0.94     51314
       Viral       0.17      0.06      0.09      5334

    accuracy                           0.88     56648
   macro avg       0.54      0.52      0.51     56648
weighted avg       0.84      0.88      0.86     56648

```

<br />

3. *Logistic Regression*

Summary:
```

Accuracy: 0.6104304947512121
Cohen's kappa: 0.10488089764993025
Balanced accuracy: 0.6337966174766455

```

Detail: 
```
              precision    recall  f1-score   support

        Flop       0.94      0.61      0.74     51314
       Viral       0.15      0.66      0.24      5334

    accuracy                           0.61     56648
   macro avg       0.55      0.63      0.49     56648
weighted avg       0.87      0.61      0.69     56648

```

<br />
<br />

#### B) *New sklearn Pipeline*

For our 3 classifiers we added the following features into our new pipeline: time, video_bool, photo_bool, tweet_length and HashingVectorizer with 2^17 features (see: `all_in_one_multiple_input_features.py`). We didn't use all of our previous features due to lack of time, as we had to re-implement them to fit them into the new pipeline, and the new experiments show that only one feature in particular was critical to the result.

<br />

1. *SGDC classifier*

Summary: 
```
accuracy: 0.5681336785125912
Cohen's kappa: 0.12634914111071838
balanced accuracy: 0.6766037922018122
```

Detail:
```
              precision    recall  f1-score   support

        Flop       0.96      0.54      0.69      7665
       Viral       0.16      0.81      0.27       833
    accuracy                           0.57      8498

   macro avg       0.56      0.68      0.48      8498
weighted avg       0.88      0.57      0.65      8498

```
<br />

2. *Linear SVC*

Sumary: 
```

accuracy: 0.9113909155095317
Cohen's kappa: 0.204992981717679
balanced accuracy: 0.5646044719257566

```

Detail:
```

              precision    recall  f1-score   support

        Flop       0.91      1.00      0.95      7665
       Viral       0.78      0.13      0.23       833
    accuracy                           0.91      8498

   macro avg       0.85      0.56      0.59      8498
weighted avg       0.90      0.91      0.88      8498

```

<br />

3. *Logistic Regression*

Summary:
```

accuracy: 0.8272534714050365
Cohen's kappa: 0.3513706313151349
balanced accuracy: 0.7646028274323429

```

Detail: 
```

               precision    recall  f1-score   support

        Flop       0.96      0.84      0.90      7665
       Viral       0.32      0.69      0.44       833

    accuracy                           0.83      8498

   macro avg       0.64      0.76      0.67      8498
weighted avg       0.90      0.83      0.85      8498

```

<br />
<br />

#### C) *Running tests with out best classifier: LogisticRegression*
<br />

1. *Logistic Regression without HashingVectorizer*

Here we wanted to test how good the classifier is just with our implemented features with information about time, videos, photos and the tweet length without HashingVectorizer.

Summary:
```

accuracy: 0.6114379854083314
Cohen's kappa: 0.10462497749628208
balanced accuracy: 0.6283828599933123

```

Detail:
```

    Test set      precision    recall  f1-score   support

        Flop       0.94      0.61      0.74      7665
       Viral       0.15      0.65      0.25       833

    accuracy                           0.61      8498

   macro avg       0.55      0.63      0.49      8498
weighted avg       0.86      0.61      0.69      8498

```
The training is now extreme fast (2.3s), but the decrease in all metrics is obivious.

<br />

2. *Logistic Regression wth just HashingVectorizer*

Now we checked the outcome just with HashingVectorizer and 2^17 features. This features has proven to be our most important one. 

Summary: 
```

accuracy: 0.8313720875500118
Cohen's kappa: 0.33444561172888765
balanced accuracy: 0.7396004977333399

```

Detail:
```

    Test set      precision    recall  f1-score   support
        Flop       0.95      0.85      0.90      7665
       Viral       0.32      0.63      0.42       833
    accuracy                           0.83      8498
   macro avg       0.64      0.74      0.66      8498
weighted avg       0.89      0.83      0.85      8498

```
The training finished after 28.9s and 200 iterations.

<br />

3. *What about overfitting?*

To see to what extent the classifier overfits, we created a table for the training set for all features with the LogisticRegression classifier. Thus, this is the output for the predicted data previously given to the classifier for training. With regard to the parameters it is comparable to the output of the test set above (B3).

````

Matrix Train set:

              precision    recall  f1-score   support

        Flop       1.00      0.89      0.94    252744
       Viral       0.46      0.96      0.63     26247

    accuracy                           0.89    278991
   macro avg       0.73      0.92      0.78    278991
weighted avg       0.95      0.89      0.91    278991

````

<br />

4. *Cheating Features*

To check if our classifier really works, we tried as a last test to add the features replies_count, retweets_count and likes_count.

Summary:
```

After 1.8 secs:
accuracy: 1.0
Cohen's kappa: 1.0
balanced accuracy: 1.0

```

Detail:
```

       Test Set       precision    recall  f1-score   support

        Flop       1.00      1.00      1.00      7665
       Viral       1.00      1.00      1.00       833

    accuracy                           1.00      8498

   macro avg       1.00      1.00      1.00      8498
weighted avg       1.00      1.00      1.00      8498
```
<br />

### Interpretation

When we did our first tests we ran it successfully with 25 features (including HashingVectorizer), we tried it with the SVM classifier, but that took too much time (nearly endless). We read later that runtime increases with SVM quadratic with the number of samples. So we used KNN with 4 NN on a 20000 sample subset and for the first time our Cohen kappa went from 0.0 to 0.1. That was a big sucess for us.

Later after long time of hyperparameter tuning and running the code on the grid (the big computer network provided by our Institute) we observed the given output metrics.

Things we found interesting:

* Indeed, our Logistic Regression classifier performed the best out of the bunch reaching a Cohen's kappa of 0.35 on the test set.
* Without HashingVectorizer, Logistic Regression learns something but with a big drop in accuracy. This is maybe because of the big drop of information.
* It's really interesting that with just the HashingVectorizer feature, the Logistic Regression classifier is so good compared to itself with all features. 
* Even though there is a small increase in Cohen's kappa when we combine all features, this comes with a big drop in run time. Case C 1 needs 2.3 sec, C 2 needs 28.9 secs, but combined they need 7.5 min. Maybe this is because `sklearns`'s implementation of the FeatureUnion function.
* When we look at the output of the test sets compared to training sets under (C 3), we directly see that the classifier overfits. But as long as the classifier still learns something and can predict new data correctly to some extent, are we satisfied.
* LinearSVC works really good on small dataset, but it still takes quite a long time for all samples.
* To get some insights into the classifier let's have a look at precision and recall of the viral samples:
   * SGDClassifier (B 1) has a high recall and low precision, so predicts most of the viral samples right, but just because he classifies something as viral much more often, than it actually is (low precision).
   * LinearSVC is just the opposite: He tends often to classify new samples not as viral even if they are (low recall), but when he does, he is quite sure about that (high precision).
   * LogisticRegression is something between them both, but still recall is much higher (so similar as SGDClassifier)
* With our Cheating Features (C 4) every classifier is just outstanding after a few seconds.

In conclusion, we are very satisfied with our final result. Cohen's kappa of 0.35 and a balanced accuracy of 0.76 (B 3) on the test set are of course not very high, but it is uncertain to what extent this is even possible in such a task. Future experiments could be conducted with more features (such as title or the author) or even with a different task. One could try to develop an artificial intelligence that predicts the number of likes and retweets of a tweet instead of just a (non) viral threshold.



## Tests

We wrote tests for the HashingVectorizer, because even though the sklearn functions themselves naturally have many tests implemented, we want to double check that we are using them correctly and that we are getting the expected output. Therefore, especially 'test_result_shape' is very important, because it checks if the length of the output list matches the number of input elements. We also wrote test files for bigrams and the tokenizer. 

We added in `run_classifier.py` a number of functions to run this file from the run_classifier_test.py which tests all classifiers, checks if the data is still equal length, tries the classifiers to fit and if not, checks if the file gives the correct error output. 


## Application

At the end, we also extended the application stub that was given to us. You will see that we removed the dimensionality reduction step from the pipeline, as mentioned before. First of all, we kept the part where the user can enter his/her tweet of course. Afterwards, we need to ask the user how many videos the tweet contains. This is due to the fact that in the original data set, there already was a column that contained an exact number of how many videos the tweets contained. For the photos however, it is important to remember that photos in twitter are embedded with a link. Hence, we took the general structure of the link, namely ```https://pbs.twimg.com/media```, and found out that images in Twitter are either in the format of ```.png``` or ```.jpg```. We then search in the user input for all of those parts that contain the general link structure, as well as one of the image formats and append the links to a list.
Since we also included the posting time of the tweet as a feature, we get the current time in the next step. We used the tweet itself, the video input the user has made before, the list of photos and the current time, and finally the remaining text-based features of our feature extraction. To use all those features together, we just had to format them in the right way such that our pipeline handles it to produces meaningful outputs.

Working example of inputs and their corresponding outputs:

Input: | Output: 
-------|--------
`data algorithm free coding https://pbs.twimg.com/media/xyz.png 😀 😃 😄 😁 😆 😅 😂 🤣 🥲 ☺️ 😊 😇 🙂 🙃 😉` | [True] Your tweet will most likely go viral.
`hello there #123` | [False] Your tweet will most likely not go viral.


## Project Organization

Our overall organization went very smoothly. The use of Trello, which none of us had heard before, was a suprisingly pleasent experience. Especially for really bringing that needed structure into the group work. We held meetings every 2 days, in a similar fashion to scrum, where we talked about current Trello sprints and what we should have finished until the next sprint. We really only had to postpone very little things and the overall workflow worked really well. 

We structured our Trello workspace into different cards:

![trello](/Documentation/trello.png)

&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; [7] Our Trello Workspace

Starting from the left, we chose to set the project structure early on as a guiding point throughout the seminar. We used the same card next, to set up checklists with things we wanted to integrate and try under each section. Every section was more or less completed during the 2 days between meetings, starting with the preprocessing work and gradually working up towards the evaluation of the classifier. During these sections, we worked on different subtasks, like we each had different preprocessings steps to implement. The tagging function also helped giving out the tasks. In the subsequent meetings cards, which we stored under 'Next Spring', we wrote the general content of the meeting beforehand. This would include exchanging results form the previous days, new features, issues, etc. In the meeting itself (held on Jitsi or Google Meet), stored under 'Active Sprints', we checked and talked about every point written, and planned the next meeting for the next 2 days. After a meeting was completed and the entire checklist was finished, we stored the card in 'Done Sprint'. Having it organized this way worked really well for us since we always knew what needed to be worked on and what was finished in (almost) real time.

## Closing thoughts

We want to thank our seminar organizer Lucas Bechberger for putting together the entire seminar in an interactive fashion that was easy to understand and follow, and showing us all the different steps in detail for how to apply machine learning within a practical example. We truly had a great learning experience, had a lot of fun and are really happy with our results. 
