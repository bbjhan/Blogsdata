from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class GlobeSample(BaseSpider):
        name = "globe_sample"
        start_urls = ['http://globeofblogs.com/topic']
        f = open('/home/bibeejan/Desktop/globe.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="textcontent"]//ul//li//p//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://globeofblogs.com/" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="textcontent"]//ul//li//p//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
			url = "http://globeofblogs.com/" + url
			sub_title = "".join(node.select('.//text()').extract())
			yield Request(url, callback=self.parse_ne, meta = {'title': title, 'sub_title': sub_title})
	def parse_ne(self, response):
		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
		sub_title = response.meta['sub_title']
		nodes = hxs.select('//div[@class="textcontent"]//ul//li//p//em')
		for node in nodes:
			url = "".join(node.select('.//text()').extract())
			data = (url, title, sub_title)
                        print data
                        self.f.write('%s\n'%repr(data))
		pag_nodes = hxs.select('//p[@class="pagination"]/a')
		for page_node in pag_nodes:
			url = "".join(node.select('.//@href').extract())
			url = "http://globeofblogs.com/" + url
			yield Request(url, callback=self.parse_ne, meta = {'tilte': title, 'sub_title': sub_title})

