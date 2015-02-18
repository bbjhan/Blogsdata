from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class FusionSample(BaseSpider):
        name = "fusion_sample"
        start_urls = ['http://www.bloggingfusion.com/']
        f = open('/home/bibeejan/Desktop/fusion.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//table[@id="cats"]//tr//td//div[@class="vline"]//h2//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://www.bloggingfusion.com/" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="links"]//table//tr//td//div[@class="pr"]//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        yield Request(url, callback=self.parse_ne, meta= {'title': title})
                refere = hxs.select('//div[@class="paging-links"]/a')
                for ref in refere:
                        ref_ = "".join(ref.select('./@href').extract())
                        ref_ = "http://www.bloggingfusion.com" +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
                cat_node = hxs.select('//table[@id="cats"]//tr//td//a/')
                for cat_nodes in cat_node:
                        ref = "".join(cat_nodes.select('.//@href').extract())
                        ref = "http://www.bloggingfusion.com/" +ref
                        cat_title = "".join(cat_nodes.select('.//text()').extract())
                        yield Request(ref, callback=self.parse_cat, meta={'title': cat_title})
	def parse_cat(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@id="links"]//table//tr//td//div[@class="pr"]//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        yield Request(url, callback=self.parse_ne, meta= {'title': title})
                refere = hxs.select('//div[@class="paging-links"]/a')
                for ref in refere:
                        ref_ = "".join(ref.select('./@href').extract())
                        ref_ = "http://www.bloggingfusion.com" +ref_
                        yield Request(ref_, callback = self.cat, meta = {'title': title})


        def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//table//tr/td[@valign="middle"]/a[@target="_blank"]')
                for node in nodes:
                        url = "".join(node.select('./@href').extract())
                        data = (url, title)
                        print data
                        self.f.write('%s\n'%repr(data))

