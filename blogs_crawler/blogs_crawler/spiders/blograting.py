from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

DOMAIN = "http://blogratings.com"
class BlogRating(BaseSpider):
        name = "blograting_sample"
        start_urls = ['http://blogratings.com/']
        f = open('/home/bibeejan/Desktop/blograting.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//ul[@id="linklist"]//li//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('./text()').extract())
                        ref_url = DOMAIN +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="info"]//h3//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        url = DOMAIN + url
                        yield Request(url, callback=self.parse_ne, meta = {'title': title})
                refere = hxs.select('//div[@class="pagination"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = DOMAIN +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
        def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = "".join(hxs.select('//div[@class="formnice"]//p//a[@rel="nofollow"]//text()').extract())
		data = (title, nodes)
		self.f.write('%s\n'%repr(data))
		
                print data

