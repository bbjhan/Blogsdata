from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class CATSample(BaseSpider):
        name = "cat_sample"
        start_urls = ['http://www.blogcatalog.com/category']
        f = open('/home/bibeejan/Desktop/catlog.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="page_column_588"]//ul[@id="parents"]//li//a')
                for node in nodes:
                        title =  "".join(node.select('.//h3//text()').extract())
                        ref_url = "".join(node.select('.//@href').extract())
                        ref_url = "http://www.blogcatalog.com" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="blogs_ren"]//p[@class="url"]//a[@rel="nofollow"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@class="pagination"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.blogcatalog.com" +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
                cat_node = hxs.select('//div[@style="margin: 10px auto 10px auto;"]//ul//li//a')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = "http://www.blogcatalog.com" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
                        yield Request(ref, callback=self.parse_ne, meta={'title': cat_title})
	def parse_ne(self, response):
 		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="blogs_ren"]//p[@class="url"]//a[@rel="nofollow"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@class="pagination"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.blogcatalog.com" +ref_
                        yield Request(ref_, callback = self.parse_ne, meta = {'title': title})

		
