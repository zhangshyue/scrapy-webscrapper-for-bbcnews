# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bbcnews.loaders import *
from scrapy import Request
from bbcnews.items import *
import logging
from pyquery import PyQuery as pq

class BbcSpider(CrawlSpider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/']

    rules=(Rule(LinkExtractor(restrict_xpaths="//li[contains(@class,'orb-nav-home')]//a",process_value=lambda x:x[0:16]+'com'), callback='parse_home'),
           Rule(LinkExtractor(allow='bbc.com', restrict_xpaths='//div[contains(@class,"module__content")]'
                                                               '//div[contains(@class,"media") and not (contains(@class,"media--icon"))]'
                                                               '//a[contains(@class,"block-link__overlay-link")]'
                              , process_value=lambda x: 'https://www.bbc.com' + x if x[0:1] == "/" else x),
                callback='parse_item'),
           )
    
#parse the home page of bbc and get the infomation of the media contents
    def parse_home(self,response):
        #logging.warning("the response of parse_home "+response.url)
        if response.status==200:
            #use pyquery to extract the wanted infomation
            doc = pq(response.text)
            medias = doc('div.media--video').items()
            for media in medias:
                item=BbcmediaItem()
                item['url'] = media.find('a.media__link').attr('href')
                item['title']=media.find('a.media__link').text().strip()
                item['type']=media.find('a.media__tag').text()
                yield item
                
#parse the infomation of the articles on bbc home page
    def parse_item(self, response):
        #logging.warning("the response of parse_item "+response.url)
        if response.status==200:
            item=BbcnewsItem()
            #use xpath to extract the wanted infomation
            item['title']=response.xpath('//div[@class="story-body"]//h1/text()').extract_first()
            item['url']= response.url
            item['type']=response.xpath('//div[contains(@class,"secondary-navigation")]//a[contains(@class,"secondary-navigation__title")]/span/text()').extract_first()
            if item['type'] is None:
                item['type'] = response.xpath("//div[@class='container-width-only']//span[@class='index-title__container']//a/text()").extract_first()
                #two ways to get type
            item['time']=response.xpath('//div[@class="story-body"]//ul[@class="mini-info-list"]//div/text()').extract_first()
            item['related_topics']= response.xpath('//div[@id="topic-tags"]//li/a/text()').extract_first()
            if item['time'] is not None:
                yield item
