from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class SpillSample(BaseSpider):
        name = "spill_sample"
        start_urls = ['http://www.spillbean.com/']
        f = open('/home/bibeejan/Desktop/spill.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//table//tr/td/a')
                for node in nodes:
                        ref_url = "".join(node.select('./@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://www.spillbean.com/" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
	def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//span[@class="sub-text"]/a[not(contains(@href, "http://www.spillbean.com/more.php?"))]')
                for node in nodes:
                        url = "".join(node.select('./@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
		cat_node = hxs.select('//table[@align="center"]//tr//td//a')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
			yield Request(ref, callback=self.parse_ne, meta={'title': cat_title})
        def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//span[@class="sub-text"]/a[not(contains(@href, "http://www.spillbean.com/more.php?"))]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

