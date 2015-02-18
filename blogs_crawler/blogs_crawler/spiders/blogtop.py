from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class Blogtopsite(BaseSpider):
        name = "blogsite_sample"
        start_urls = ['http://www.blogtopsites.com/']
        f = open('/home/bibeejan/Desktop/blogtopsite.txt', 'a+')
        data ={}
        def parse(self, response):
               	hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@id="blogDirectory"]//ul//li//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://www.blogtopsites.com" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="info"]//h2//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        url = "http://www.blogtopsites.com" + url
			yield Request(url, callback=self.parse_ne, meta = {'title': title})
                refere = hxs.select('//div[@class="pages"]//ul//li//a[contains(@href, "page")]')
                for ref in refere: 
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.blogtopsites.com" +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
		cat_node= hxs.select('//div[@class="related-tags"]//p//a')
		for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = "http://www.blogtopsites.com" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
                        yield Request(ref, callback=self.parse_cat, meta={'title': cat_title})
	def parse_cat(self, response):
		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="info"]//h2//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        url = "http://www.blogtopsites.com" + url
                        yield Request(url, callback=self.parse_ne, meta = {'title': title})
                refere = hxs.select('//div[@class="pages"]//ul//li//a[contains(@href, "page")]')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.blogtopsites.com" +ref_
                        yield Request(ref_, callback = self.parse_cat, meta = {'title': title})	


	def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = "".join(hxs.select('//div[@class="width-80per floatLeft"]//h2/a//@href').extract())
		url = "http://www.blogtopsites.com" + nodes
		yield Request(url, callback = self.parse_det, meta = {'title': title})
	def parse_det(self, response):
		hxs = HtmlXPathSelector(response)
		title = response.meta['title']
		url = response.url
		data = (title, url)
		self.f.write('%s\n'%repr(data))
		print data


