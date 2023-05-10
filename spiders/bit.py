import scrapy
import os
from urllib.parse import urlparse

class BITSpider(scrapy.Spider):
    name = "bit"
    with open ('other_utility/bitrenLinks.txt') as f:
        start_urls=f.readlines()
    # start_urls = [
    #     'https://www.bit.edu.cn/',
    # ]

    dead_links=set()

    subdir='htmlSource'
    if not os.path.exists(subdir):
        os.mkdir(subdir)

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u,callback=self.parse,errback=self.errorback,dont_filter=True)

    def errorback(self,failure):
        self.dead_links.add(failure.request.url)
        yield{
            'error response': failure.value.response,
            'url': failure.request.url
        }
        
        
    def parse(self, response):
        # if url end with docx, doc, xls, zip, or pdf, then do something else.
        if response.url.split('.')[-1] in {'pdf','doc','docx','ppt','pptx','xls','xlsx','zip'}:
            pass
        else:
            filename = response.url.replace("/",'_')[7:]
            if filename[0]=='_':
                filename=filename[1:]
            if filename[-1]=='_':
                filename=filename[:-1]+'.html'
            filepath=os.path.join(self.subdir,filename)
            with open(filepath, 'wb') as f:
                f.write(response.body)

        yield {     # return some results
            'url': response.url,
            # 'title': response.css('title::text')
        }

        urls = response.css('a::attr(href)')   # find all sub urls
        for url in urls:
            text=url.get()
            if 'http' not in text:# it's a relative url
                yield response.follow(url, callback=self.parse)  
            elif 'bit' in text: # do not crawl non-bit domains
                yield response.follow(url, callback=self.parse)  