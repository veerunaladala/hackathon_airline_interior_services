# hackathon_airline_interior_services

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



Link to the webscraped data
https://drive.google.com/file/d/1UhiIrOW8eg1WLGPVmFYyQ2G8xcg5VJUA/view?usp=sharing
