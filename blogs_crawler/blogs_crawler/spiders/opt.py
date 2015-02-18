from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class OptSample(BaseSpider):
        name = "opt_sample"
        start_urls = ['http://www.ontoplist.com/blog-directory/']
        f = open('/home/bibeejan/Desktop/ontop.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@class="FL "]//a[@class="Nounderline"]')
                for node in nodes:
                        title =  "".join(node.select('.//text()').extract())
			ref_url = "".join(node.select('.//text()').extract())
                        ref_url = "http://www.ontoplist.com" +ref_url
                        print ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="FL "]//p//a[@target="_blank"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@class="paginator"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.ontoplist.com" +ref_        
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
                cat_node = hxs.select('//div[@class="LPadXX TPadXX BPadXX"]//div[@class="LPadXXXX"]//a')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
			ref = "http://www.ontoplist.com" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
			yield Request(ref, callback=self.parse_ne, meta={'title': cat_title})
        def parse_ne(self, response):                                                 
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="FL "]//p//a[@target="_blank"]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))
                refere = hxs.select('//div[@class="paginator"]//a')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.ontoplist.com" +ref_        
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
