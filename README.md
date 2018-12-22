# scrapy-webscrapper-for-bbcnews
A scrapy webscraper that can scrape articles and videos of bbc

# Running the spiders
### To create a scrapy project:
```
scrapy startproject bbcnews
cd bbcnews
scrapy genspider bbc bbc.com
```
### Start scrapping
```
scrapy crawl bbc
```
### Save the data in a json file
```
scrapy crawl bbc -o bbc.json
```
This will crawl bbc and save the data in a file called bbc.json.

# The structure of bbc spider
This spider can mainly scrape the articles and media contents from the home page of bbc. It has two items, a Bbcnewsitem and a Bbcmediaitem.

The extracted data of a Bbcnewsitem is in this form:
```
{
  "title": "Mars: Pictures reveal 'winter wonderland' on the red planet", 
  "url": "https://www.bbc.com/news/science-environment-46645321", 
  "type": "Science & Environment", 
  "time": "21 December 2018", 
  "related_topics": "Mars"
}
```
The extracted data of a Bbcmediaitem is in this form:
```
{
  "url": "/news/stories-46633914", 
  "title": "When a child experiment goes wrong", 
  "type": "Stories"
}
```

There is also a log file that can be used for debug. Write anything that you want in the log file by importing logging:
```
import logging
```
