from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class PediaSample(BaseSpider):
        name = "pedia_sample"
        start_urls = ['http://directory.bloggapedia.com/']
        f = open('/home/bibeejan/Desktop/pedia.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="innerwrapper"]//ul//li//span//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})

        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="actions clearfix"]//a[@target="_blank"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
		pags = hxs.select('//div[@id="subcategories"]//ul//li//span//a')
		for page in pags:
			url = "".join(node.select('.//@href').extract())
			sub_title = "".join(node.select('.//text()').extract())
			yield Request(url, callback=self.parse_ne, meta={'title': sub_title})
        def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
		nodes = hxs.select('//div[@class="actions clearfix"]//a[@target="_blank"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

