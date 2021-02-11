#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from math import floor
import time

# def get_links():
links = list()
# review_list = list()
# air_list= list()
#opening the chrome driver
driver = webdriver.Chrome('C:/Users/veeru/Documents/chromedriver')
# looping through A-Z pages of airline & seat reviews
for review_link in ['https://www.airlinequality.com/review-pages/a-z-{review_type}-reviews/'
                    .format(review_type=review_type) for review_type in ('airline', 'seat')]:
    #review_list.append(review_link)
    # going to the review link
    driver.get(review_link)
    airline_lists = [airline_list.find_elements_by_tag_name('li')
                     for airline_list in driver.find_elements_by_class_name('items')]
    #air_list.append(airline_lists)
    for airline_list in airline_lists:
        for airline in airline_list:
            # review link of each airline
            link = airline.find_element_by_tag_name('a').get_attribute('href')
            links.append(link)
driver.close()
links = sorted(list(set(links)))
# Save unique links in text file
link_file = open("html_links.txt", 'w+')
link_file.write('\n'.join(links))


try:
    #trying to open the csv file
    data = pd.read_csv("reviews_data.csv", index_col=None) 
except FileNotFoundError:
    #as the file doesn't exist, we are creating a new one
    data = pd.DataFrame(columns=['Aircraft',                    
                                 'Cabin Staff Service',
                                 'Date Flown',
                                 'Food & Beverages',
                                 'Ground Service',
                                 'Inflight Entertainment',
                                 'Recommended',
                                 'Route',
                                 'Seat Comfort',
                                 'Seat Type',
                                 'Type Of Traveller',
                                 'Value For Money',
                                 'Wifi & Connectivity',
                                 'airline',
                                 'best_rating',
                                 'comment',
                                 'comment_date',
                                 'header',
                                 'rating',
                                 'review_type'])
    data.to_csv("reviews_data.csv")
    
#opening the chromedriver
driver = webdriver.Chrome('C:/Users/veeru/Documents/chromedriver')
reviews_per_page = 50
for link in links:
    # starting the clock
    tic = time.time()
    # setting the link to get 50 reviews per page
    driver.get(link + '/?sortby=post_date%3ADesc&pagesize={}'.format(reviews_per_page))
    #finding the name of the airline by tage name 'h1' in the class "info" of the html page
    airline_name = driver.find_element_by_class_name('info').find_element_by_tag_name('h1').text
    # in the same class as above at tage nale 'h2' we get the review type
    review_type = driver.find_element_by_class_name('info').find_element_by_tag_name('h2').text
    # extracting total number of reviews the airline has to decide the number of pages to scrape
    total_reviews= int(driver.find_element_by_class_name('review-count').text.split(' ')[-2])
    # checking whether the particular airline has been already scraped or not
    if review_type in data[data.airline == airline_name].review_type.unique():
        print('Already scraped {review_type} for {airline_name}'
              .format(review_type=review_type, airline_name=airline_name))
        continue    
    print('Scraping {airline} {review}'.format(airline=airline_name, review=review_type))

    data_lines = []
    # counting number of pages 
    number_of_pages = total_reviews//reviews_per_page + 1 if total_reviews % reviews_per_page != 0         else total_reviews//reviews_per_page
    for page_number in range(1, number_of_pages + 1):
        print('scraping page {} out of {}'.format(page_number, number_of_pages))
        #getting review article container in the particular page
        reviews_container = driver.find_element_by_tag_name('article')
        # getting each of the reviews from the container
        reviews = reviews_container.find_elements_by_tag_name('article')
        # looping to get the required info from particular review 
        for review in reviews:
            # adding the airline name and reviewtype to dictionary
            data_line = {'airline': airline_name, 'review_type': review_type}
            try:
                #finidng the rating given by the customer and maximum rating possible
                data_line['rating'], data_line['best_rating'] = review.find_element_by_class_name('rating-10').text.split('/')
            except ValueError:
                pass
            # extracting the header of the review
            data_line['header'] = review.find_element_by_class_name('text_header').text
            # extracting the comment_date of the review
            data_line['comment_date'] = review.find_element_by_tag_name('time').get_attribute('datetime')
            # extracting the comment
            data_line['comment'] = review.find_element_by_class_name('text_content').text
            # accessing the rating table of particular review
            ratings_table = review.find_element_by_class_name('review-ratings').find_element_by_tag_name('tbody')
            for rating in ratings_table.find_elements_by_tag_name('tr'):
                try:
                    key_value = rating.find_elements_by_tag_name('td')
                     # if the rating for each service is given then we will extract it                                                                                    
                    if 'stars' in key_value[1].get_attribute('class'):
                        number_of_stars = len(key_value[1].find_elements_by_class_name('star.fill '))
                        data_line[key_value[0].text] = number_of_stars
                    else:
                        data_line[key_value[0].text] = key_value[1].text
                except Exception:
                    pass
            # appending the particular review data complete data
            data_lines.append(data_line)
            # waiting for 0.5 seconds
            time.sleep(0.5)
        # going to the next link
        driver.get(link + '/page/{}/?sortby=post_date%3ADesc&pagesize={}'.format(page_number, reviews_per_page))
    # writing all the data to dataframe
    data = data.append(pd.DataFrame(data_lines))
    # storing the data as csv file
    data.to_csv("reviews_data.csv", index=None)
    toc = time.time()
    # time taken to scrape information from one airline and number of reviews scraped 
    print('Scraped {n_records} in {seconds} seconds'.format(n_records=len(data_lines), seconds=floor(toc-tic)))
    time.sleep(1)


