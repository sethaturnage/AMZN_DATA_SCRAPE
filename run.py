import amazon_scrape
import pandas
from amazon_scrape import item_compare_scrape as Scrape
import textual_analysis
from textual_analysis import TF_IDF
import data_model
import pprint
from data_model import regressionFrom_TF_IDF
#name: Seth Turnage
#id: 1210810585
#date: 11/23/2018
#Desc:
#   All "modules" are just separate python scripts written by me
#   1. amazon_scrape
#       *- Amazon Scraper uses xml queries for reviews, and css queries for product information. 
#           *- It collects reviewMin to reviewMax star reviews for textual analysis, as long as they are in the 'Kindle' category
#           *- Product information is also collected
#           *- Product descriptons are not collected because they have VERY LITTLE intelligible relevance to review ratings.
#   2. textual_analysis
#       *- reads and categorizes json files from amazon_scraper
#       *- performs TF-IDF categorization on them
#       *- outputs results in a graph
#   3. data_model
#       *- randomly splits data into train and test
#       *- builds regression model
#       *- evaluates regression model
#   4. run.py
#       *- imports these programs as modules
#       *- stores basic configuration information
#       *- runs modules
#           *-first: amazon_scrape
#           *-second: textual_analysis

#Where amazon_scrape will store product info, and textual_analysis will retrieve it
DumpDirectory='json/'

DisplayChartsFromAmazonScrape = True
DisplayGraphsFromTextualAnalysis = True


#ASIN's are product id's from Amazon
#In this case, we are focusing on Kindle eBooks
#We are comparing works from the philosopher "Friedrick Nietzsche"
#In this case, we are comparing Kindle copies of the work: "Beyond Good and Evil"
#I have pulled Amazon id's for each of the pages and we are filtering for Kindle Reviews only
Amazon_Product_ASIN=['B075189T6C','B00FF76POI','B01J4WF9PU','B00DO1HFLE','B002RI9DFG']
Desired_Review_Format='Format: Kindle Edition'

#Since we are looking for the reasons why Kindle Editions are being rated badly, we will record ratings between one and three stars
MaximumRatingToSaveToJson = 5
MinimumRatingToSaveToJson = 1
#We will rip 10 pages of ratings. Riping more that this will take a tremendous amount of time
PagesOfRatings = 10

Scrape(Amazon_Product_ASIN,Desired_Review_Format,MaximumRatingToSaveToJson,MinimumRatingToSaveToJson,PagesOfRatings,DisplayChartsFromAmazonScrape,DumpDirectory)
TF_IDF_FROM_AMAZON = TF_IDF(DumpDirectory, DisplayGraphsFromTextualAnalysis)
TF_IDF_GOOD_REVIEWS = TF_IDF_FROM_AMAZON[0]
TF_IDF_BAD_REVIEWS = TF_IDF_FROM_AMAZON[1]

EvaluateModel = True

regressionFrom_TF_IDF(TF_IDF_GOOD_REVIEWS,EvaluateModel,"Good Reviews Regression Model")

regressionFrom_TF_IDF(TF_IDF_BAD_REVIEWS,EvaluateModel,"Bad Reviews Regression Model")