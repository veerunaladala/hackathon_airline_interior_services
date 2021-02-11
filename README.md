# Hackathon_Airline_Interior_Services

# About the hackathon

The aim of the hackathon is to understand how the user experience of airplane passengers can be improved.


To start with, We have three main tasks to solve the problem
1) Web Scraping
2) Topic Modelling Analysis
3) Sentiment Analysis.

# Web Scraping

Built a webscraping algorithm using selenium and chromedriver to scrape the data from skytrax. We scraped around 53000 reviews.

# Topic Modelling Analysis

Built a Topic modeling using Latent Dirichlet Allocation(LDA) to find the relevant topics.  We used Coherence score which measures a single topic
by measuring the degree of semantic similarity
between high scoring words in the topic. These
measurements help distinguish between topics
that are semantically interpretable topics and
topics that are artefacts of statistical inference

# Sentiment Analysis

We often use sentiment analysis on textual data to help businesses monitor brand and product sentiment in customer feedback and understand customer needs.
First we clean the comments and then use TF-IDF vectorizer which will tokenize comments, learn the vocabulary and inverse document frequency weightings, and allow you to encode new documents.
Than we used Logistic Regression which takes a regular linear regression and applies a sigmoid to the output of the linear regression topredict the sentiment of the reviews.

# How to Run

1) Please check whether you have installed the necessary packages.
2) Download the chromedriver and update the chromedriver path in the skytrax_scraping.py file.
3) Execute the skytrax_scraping.py file to scrape the reviews data from the skytrax. Please the stop the execution manually if you think you have enough data.
4) Execute topic_modelling.py to check the relevant topics.
5) Execute sentiment_analysis.py which ouput file which consists of the sentiment score for each of the reviews. It also prints the top 20 positive and negative words.

Link to the webscraped data
https://drive.google.com/file/d/1UhiIrOW8eg1WLGPVmFYyQ2G8xcg5VJUA/view?usp=sharing

