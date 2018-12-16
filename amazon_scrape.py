# Written for Data Mining 472 Project 2
# author: Seth Turnage
# date: 11/25/2018
# id: 1210810585
# desc: scrapes product details and reviews from Amazon using brute force xml and css queries
from urllib.request import urlopen as urlRequest
from decimal import Decimal
from lxml import html
import json
import pprint
import os
from json import dump, loads
from re import sub
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as Soup 

star_ratings = ["five_star","four_star","three_star","two_star","one_star"]

def item_compare_scrape(asins,formatReviewed,maxRatingToSave,minRatingToSave, PagesOfRatings=4, compare = True, dumpDirectory="json/"):
    Point_Labels = []
    Avg_Rating_Axis = [] 
    Sales_Rank_Axis = []

    for current_Index, ASIN in enumerate(asins):
        ##################### Scrape Product Information #############################
        producturltobeimplemented = "https://www.amazon.com/dp/"+ASIN+"/"
        review_list=[]

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        r = requests.get(producturltobeimplemented, headers=headers)
        soup = Soup(r.content, "lxml")

        EbookProductTitle = soup.select('span[id="ebooksProductTitle"]')
        ebookTitleText = EbookProductTitle[0].text
        EbookProductAuthor = soup.select('a[class="a-link-normal contributorNameID"]')
        ebookAuthorText = EbookProductAuthor[0].text
        try:
            KindlePriceData = soup.select('div > table > tr[class="kindle-price"] > td')[1].text.split("\n")
            KindlePrice = float(KindlePriceData[1].strip().split("$")[1])
            KindleDiscountPercentage = float(KindlePriceData[5].strip().split("(")[1].replace("%)",""))
        except:
            KindlePriceData = soup.select('span[class="a-size-base a-color-price a-color-price"]')[0].text.split("\n")
            KindlePrice = float(KindlePriceData[1].strip().split("$")[1])
            KindleDiscountPercentage = 0.00
        RatingData = soup.select('div > table > tr > td > div > ul > li[id="SalesRank"]')[0].text.strip().split("\n")
        SalesRanking = int(float(RatingData[23].split(" ")[0].replace("#","").replace(",","")))
        ProductAverageReview = soup.select('span[data-hook="rating-out-of-text"]')
        ProductAverageReviewText = float(ProductAverageReview[0].text.split(" ")[0])

        r.close()

        ######################### Scrape Reviews #############################
        
        for starNumberIndex in range(minRatingToSave-1,maxRatingToSave):         
            for pageNumber in range(1, PagesOfRatings):
                reviewurl= "https://www.amazon.com/dp/product-reviews/"+ASIN+"/ref=cm_cr_arp_d_hist_3?pageNumber="+str(pageNumber)+"&filterByStar="+star_ratings[starNumberIndex]

                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                    r = requests.get(reviewurl, headers=headers)
                    #cleaned_Response = r.text.replace('\x00', '')
                    parser = html.fromstring(r.text)
                    
                    reviews = parser.xpath('//div[@data-hook="review"]')
                    
                    for review in reviews:
                        ReviewRating = review.xpath('.//i[@data-hook="review-star-rating"]//text()')
                        ReviewHeader = review.xpath('.//a[@data-hook="review-title"]//text()')
                        try:
                            ReviewHeaderText = ReviewHeader[0]
                        except:
                            ReviewHeaderText = "Header not scraped"
                        ReviewDate = review.xpath('.//span[@data-hook="review-date"]//text()')
                        ReviewType = review.xpath('.//a[@data-hook="format-strip"]//text()')
                        try:
                            ReviewTypeText = ReviewType[0]
                        except:
                            ReviewTypeText = "Type not scraped"
                        ReviewText = review.xpath('.//span[@data-hook="review-body"]//text()')
                        try: 
                            RatingFloat = float(ReviewRating[0].split(" ")[0])
                        except:
                            RatingFloat = float(starNumberIndex+1)
                        try:
                            ReviewDateText = ReviewDate[0]
                        except:
                            ReviewDateText = "Date not scraped"
                        try:
                            ReviewTextScraped = ReviewText[0]
                        except:
                            ReviewTextScraped = "text not scraped"
                        #rawReviewText_2 = parser.xpath('.//div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview')
                        #rawReviewText_3 = parser.xpath('.//div[contains(@id,"dpReviews")]/div/text()')
                    #    if rawReviewText_2:
                    #        json_reviewText_2_data = loads(rawReviewText_2[0])
                    #        review_2_text = json_reviewText_2_data['rest']
                    #        full_review_text = (' '.join(' '.join(rawReviewText_1).split()))+(sub('<.*?>', '', review_2_text))
                    #    else:
                    #        full_review_text = (' '.join(' '.join(rawReviewText_1).split()))
                    #    if not rawReviewText_1:
                    #        full_review_text = (' '.join(' '.join(rawReviewText_3).split()))

                        reviewToBeAdded = {'Header':ReviewHeaderText,'ReviewType':ReviewTypeText,'Rating':RatingFloat,'Date':ReviewDateText,'Text':ReviewTextScraped,}
                        if (ReviewTypeText == formatReviewed or ReviewTypeText == ""):
                            review_list.append(reviewToBeAdded)
                except:
                    print("no review page found")
            #print(review_list)

        Avg_Rating_Axis.append(ProductAverageReviewText)
        Sales_Rank_Axis.append(SalesRanking)
        Point_Labels.append(ebookTitleText)
        data = {
            'Name': ebookTitleText,
            'Author': ebookAuthorText,
            'Average Rating': ProductAverageReviewText,
            'Sales Rank': SalesRanking,
            'Price': KindlePrice,
            'Discount': KindleDiscountPercentage,
            'Reviews': review_list
        }

        try:
            os.remove(dumpDirectory+ASIN+'.json')
        except OSError:
            pass

        f=open(dumpDirectory+ASIN+'.json','w')
        json.dump(data,f,indent=4)
        print('>>>'+dumpDirectory+ASIN+'.json','w')
        loadingbar = ""


        for index in range (0,int( 100*((current_Index+1)/len(asins)) )) :
            loadingbar+="|"

        loadingbar+=str(((current_Index+1)/len(asins))*100)+"%\n"

        print(loadingbar)
        pprint.pprint(data)
    if(compare == True):
        print(Avg_Rating_Axis)
        print(Sales_Rank_Axis)
        plt.scatter(Avg_Rating_Axis, Sales_Rank_Axis, marker="o",cmap=plt.get_cmap('Spectral'))
        for label, x, y in zip(Point_Labels, Avg_Rating_Axis, Sales_Rank_Axis):
             plt.annotate(
                label,
                xy=(x, y), xytext=(50, 20),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
        plt.title('Salesrank vs Average Star Rating')  
        plt.xlabel('Avg. Star Rating')  
        plt.ylabel('Amazon Salesrank')  
        plt.axis([1, 5, 1, 1000000])
        plt.show()

