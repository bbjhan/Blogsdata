from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class ListSample(BaseSpider):
        name = "list_sample"
        start_urls = ['http://www.bloglisting.net/']
        f = open('/home/bibeejan/Desktop/list.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//table//tr//td[@valign="top"]//div[@class="catBox"]//h2//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://www.bloglisting.net" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})

	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//table[@border="0"]//tr//td//span[@class="link"]')
                for node in nodes:
                        url = "".join(node.select('.//text()').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

		cat_node = hxs.select('//table[@id="categories"]//tr//td[@valign="top"]//h2')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = "http://www.bloglisting.net" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
                        yield Request(ref, callback=self.parse_ne, meta={'title': cat_title})
	def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//table[@border="0"]//tr//td//span[@class="link"]')
                for node in nodes:
                        url = "".join(node.select('.//text()').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

