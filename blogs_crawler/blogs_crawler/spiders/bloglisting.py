from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

DOMAIN = "http://www.bloglisting.net"
class Bloglistings(BaseSpider):
        name = "bloglistings"
        start_urls = ['http://www.bloglisting.net/']
        f = open('/home/bibeejan/Desktop/bloglistings.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="catBox"]//h2//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = DOMAIN +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//table//tr//td//span[@class="link"]')
                for node in nodes:
                        url = "".join(node.select('.//text()').extract())
			data = (title, url)
			self.f.write('%s\n'%repr(data))
                	print data
                cat_node= hxs.select('//div[@class="catBoxa"]//h2//a')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = DOMAIN +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
                        yield Request(ref, callback=self.parse_cat, meta={'title': cat_title})
	def parse_cat(self, response):
		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//table//tr//td//span[@class="link"]')
                for node in nodes:
                        url = "".join(node.select('.//text()').extract())
                        data = (title, url)
                        self.f.write('%s\n'%repr(data))
                        print data


