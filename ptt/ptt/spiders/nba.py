# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime


class NbaSpider(scrapy.Spider):
    name = 'nba'
    url = 'https://www.ptt.cc/bbs/NBA/'
    
    # 指定爬取頁數
    count = 10
    
    def start_requests(self):
        yield scrapy.Request(url=self.url)


    def parse(self, response):
        urlList = response.css('.r-ent .title a::attr(href)').getall()
        for i in urlList:
            contentUrl = response.urljoin(i.split('/')[-1])
            yield scrapy.Request(url=contentUrl,callback=self.parse_content)

        # 找到下一頁的連結
        next = response.css('.wide:nth-child(2)::attr(href)').get()
        url = response.urljoin(next.split('/')[-1])
        
        # 如果滿足指定頁數就停止
        if self.count  <= 0:
            raise  CloseSpider('close it')
        self.count -= 1
        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        try:
            meta = response.css('.article-metaline')
            author = meta[0].css('.article-meta-value::text').get()
            title = meta[1].css('.article-meta-value::text').get()
            time =  meta[2].css('.article-meta-value::text').get()
            

            contentList = response.css("#main-content::text").getall()

            text = ''
            for i in contentList:
                text += "".join(i.split())
            
            item = {
                'author': author,
                'title': title,
                'time': datetime.strptime(time, '%a %b %d %H:%M:%S %Y'),
                'text': text[0:30] + '...'
            }

            yield item

        except:
            pass