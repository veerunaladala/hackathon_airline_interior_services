# -*- coding: utf-8 -*-
"""Sentiment_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lsHthW1szk-m6LBpO3VpSEr6u0yKOxye
"""

import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
import spacy
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score

#spacy_nlp=spacy.load('en_core_web_sm') 

# importing the data
df=pd.read_csv('/content/drive/MyDrive/hackathon/reviews_data.csv')
# finding unique values in review_type
# df["review_type"].unique()
# finding unique values in power supply 
# df["Power Supply"].unique() 
# dropping the column as we dont have any useful information
# df=df.drop(['review_type','Power Supply'], axis = 1)

# removing selected characters
def removing_special_characters(raw_string):               
  string = raw_string.lower()
  string = string.replace('ý', '')
  string = string.replace('|', '')
  return string


# cleaning the comments and storing as a seperate column
def cleaned_comment(df, column_name):
  clean_comment=[]
  for comment in df[column_name]:
    #string= raw_to_tokens(comment,spacy_nlp)
    string=removing_special_characters(comment)
    clean_comment.append(string)
  return clean_comment

# extracting adjectives and verbs 
def extract_sentiment_terms(df):
    sentiment_terms = []
    for comment in spacy_nlp.pipe(df["cleaned_comment"]):
        if comment.is_parsed:
            sentiment_terms.append(' '.join([token.lemma_ for token in comment if (not token.is_stop and not token.is_punct and (token.pos_ == "ADJ" or token.pos_ == "VERB"))]))
        else:
            sentiment_terms.append('')
    return sentiment_terms

def pre_processing(df,column_name):
  # filling NAn values with zero
  df=df.fillna(0) 

  # cleaning all the comments
  df["cleaned_comment"]= cleaned_comment(df,column_name)
  df["sentiment_terms"]= extract_sentiment_terms(df)
  return df

# mapping reviews 0 to 5 as negative(negative is taken as 0) and else is positive(positive is taken as 1)
def review_mapping(df,column_name):
  y_map = {0:0,1:0, 2:0, 3:0, 4:0, 5:0, 6:1, 7:1, 8:1, 9:1, 10:1}
  df["simplified_rating"] = df[column_name].map(y_map)
  df["simplified_rating"].astype(int)
  return df 

def model_fit_transform(X_train,y_train, X_test, vectorizer, classifier):
    # vectorizing the sentiment terms
    train_matrix = vectorizer.fit_transform(X_train)
    test_matrix =  vectorizer.transform(X_test)
    print('# features: {}'.format(train_matrix.shape[1]))
    print('# train records: {}'.format(train_matrix.shape[0]))
    print('# test records: {}'.format(test_matrix.shape[0]))
    #fitting the model
    model = classifier.fit(train_matrix, y_train) 
    # calculating accuracy
    predictions = model.predict(test_matrix)              
    # scores = cross_val_score(logreg, X_train, y_train, cv=5)
    # print('maximum Cross-Validation Accuracy Scores', scores.max())
    k = vectorizer.get_feature_names()
    coef = model.coef_.tolist()[0]
    coeff_df = pd.DataFrame({'Word' : k, 'Coefficient' : coef})
    coeff_df = coeff_df.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
    print('')
    print('-Top 20 positive-')
    print(coeff_df.head(20).to_string(index=False))
    print('')
    print('-Top 20 negative-')        
    print(coeff_df.tail(20).to_string(index=False))
    return predictions


df= pre_processing(df,"comment")
df= review_mapping(df,"rating")

data=pd.read_csv('final_test_data.csv')
data= pre_processing(data,"full_message")
X_train = df['sentiment_terms']
y_train = df["simplified_rating"]
X_test = data['sentiment_terms']
logreg=LogisticRegression(max_iter=1000) 
tfidf = TfidfVectorizer(stop_words = 'english')
#c= CountVectorizer(stop_words = 'english')
predictions = model_fit_transform(X_train,y_train, X_test, tfidf, logreg)
data['predictions']=predictions
data.to_csv('sentiment_analysis_output.csv')

