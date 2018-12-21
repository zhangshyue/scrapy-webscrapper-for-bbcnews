# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bbcnews.loaders import *
from scrapy import Request
from bbcnews.items import *
import logging

class BbcscienceSpider(CrawlSpider):
    name='science'
    allowed_domains = ['bbc.com']
    start_urls=['https://www.bbc.com/news/science_and_environment']

    rules = (Rule(LinkExtractor(allow='/news/',restrict_xpaths='//div[not(contains(@class,"condor-item__body"))]'
                                                                      '/a[@class="title-link"]'),callback='parse_item'),)

    def parse_item(self,response):
        logging.warning("the url of the response " + response.url)
        if response.status == 200:
            # self.logger.warning("%%%")
            item = BbcscienceItem()
            # loader = BbcLoader(item=BbcnewsItem(), response=response)
            item['title'] = response.xpath('//div[@class="story-body"]//h1/text()').extract_first()
            item['url'] = response.url
            item['type'] = response.xpath(
                '//div[contains(@class,"secondary-navigation")]//a[contains(@class,"secondary-navigation__title")]/span/text()').extract_first()
            if item['type'] is None:
                item['type'] = response.xpath("//div[@class='container-width-only']//span[@class='index-title__container']//a/text()").extract_first()
            item['time'] = response.xpath(
                '//div[@class="story-body"]//ul[@class="mini-info-list"]//div/text()').extract_first()
            item['related_topics'] = response.xpath('//div[@id="topic-tags"]//li/a/text()').extract_first()
            if item['time'] is not None:
                yield item

class BbcSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com/']

    rules=(Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"module__content")]'
                                                                      '//div[contains(@class,"media") and not (contains(@class,"media--icon"))]'
                                                                      '//a[contains(@class,"block-link__overlay-link")]'
                              ,process_value=lambda x:'https://www.bbc.com'+x if x[0:1]=="/" else x), callback='parse_item'),)
    #only crawl article or pictures not videos
    def link_parse(self, response):
        logging.warning("url of response# "+response.url)
        yield Request(response.url, self.parse_item)

    def parse_error(self,failure):
        logging.warning("failure@ ")

    def parse_item(self, response):
        logging.warning("the url of the response "+response.url)
        if response.status==200:
            #self.logger.warning("%%%")
            item=BbcnewsItem()
            #loader = BbcLoader(item=BbcnewsItem(), response=response)
            item['title']=response.xpath('//div[@class="story-body"]//h1/text()').extract_first()
            item['url']= response.url
            item['type']=response.xpath('//div[contains(@class,"secondary-navigation")]//a[contains(@class,"secondary-navigation__title")]/span/text()').extract_first()
            item['time']=response.xpath('//div[@class="story-body"]//ul[@class="mini-info-list"]//div/text()').extract_first()
            item['related_topics']= response.xpath('//div[@id="topic-tags"]//li/a/text()').extract_first()
            if item['time'] is not None:
                yield item
