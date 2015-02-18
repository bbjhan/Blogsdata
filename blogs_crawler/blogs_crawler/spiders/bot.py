from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class BotwSample(BaseSpider):
        name = "bot_sample"
        start_urls = ['http://blogs.botw.org/']
        f = open('/home/bibeejan/Desktop/botw.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="categories-holder"]//ul//li//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://blogs.botw.org" +ref_url
                        print ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="TopLevelCategories"]//ul//li//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        url = "http://blogs.botw.org" + url
                        sub_title = "".join(node.select('.//text()').extract())
                        yield Request(url, callback=self.parse_ne, meta = {'title': title, 'sub_title': sub_title})
		sub_nodes = hxs.select('//div[@class="categories"]//ul//li//a')
		for sub_node in sub_nodes:
			url = "".join(sub_node.select('.//@href').extract())
			sub_title = "".join(sub_node.select('.//text()').extract())
			url = "http://blogs.botw.org" + url
			yield Request(url, callback=self.parse_ne, meta = {'title': title, 'sub_title': sub_title})
        def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                sub_title = response.meta['sub_title']
                refere = hxs.select('//div[@id="Listings"]//div[@class="listing"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        data = (ref_, sub_title, title)
                        print data
                        self.f.write('%s\n'%repr(data))

