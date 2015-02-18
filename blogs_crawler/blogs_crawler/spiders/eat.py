from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class EATSample(BaseSpider):
        name = "eat_sample"
        start_urls = ['http://portal.eatonweb.com/']
        f = open('/home/bibeejan/Desktop/eat.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@id="directory"]//div[@class="standard"]//span[@class="subject"]//a')
                for node in nodes:
	                ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://portal.eatonweb.com/" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})

	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="catpage"]//div[@id="catpageblog"]//p/small/a[contains(@href, "http")]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@id="pagenav"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://portal.eatonweb.com" +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
                cat_node = hxs.select('//p//a[contains(@href, "category/")]')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = "http://portal.eatonweb.com" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
			if "Overall" in cat_title:
				continue
                        yield Request(ref, callback=self.parse_ne, meta={'title': cat_title})
        def parse_ne(self, response):
		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="catpage"]//div[@id="catpageblog"]//p/small/a[contains(@href, "http")]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@id="pagenav"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://portal.eatonweb.com" +ref_
                        yield Request(ref_, callback = self.parse_ne, meta = {'title': title})

