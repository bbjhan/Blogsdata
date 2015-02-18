from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class SearchSample(BaseSpider):
        name = "search_sample"
        start_urls = ['http://www.blogsearchengine.com/']
        f = open('/home/bibeejan/Desktop/search.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//aside[@class="widget widget-categories"]//ul//li//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
	
	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="content"]//a[@class="entry-link"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
			yield Request(url, callback=self.parse_ne, meta={'title': title})
		pags = hxs.select('//div[@class="nav-next"]//a')
                for page in pags:
                        url = "".join(node.select('.//@href').extract())
                        yield Request(url, callback=self.parse_next, meta={'title': title})
	def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="entry-content"]//p//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

