from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class EBloglog(BaseSpider):
        name = "bloglogs_sample"
        start_urls = ['http://www.bloglog.com/']
        f = open('/home/bibeejan/Desktop/blogss.txt', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//div[@id="blogDirectory"]//ul//li//a')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = "http://www.bloglog.com" +ref_url
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})

        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//div[@class="info"]//a[contains(@href, "/blog")]')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
			url = "http://www.bloglog.com" +url
			yield Request(url, callback = self.parse_ne, meta = {'title': title})
			
                refere = hxs.select('//div[@class="pages"]//ul//li//a[contains(@href, "page")]')
                for ref in refere: 
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = "http://www.bloglog.com" +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})


	def parse_ne(self, response):
		hxs = HtmlXPathSelector(response)
                title = response.meta['title']
		nodes = "".join(hxs.select('//h1//a[@rel="nofollow"]//@href').extract())
		url = "http://www.bloglog.com" + nodes
		yield Request(url, callback = self.parse_det, meta = {'title': title})

	def parse_det(self, response):
		hxs = HtmlXPathSelector(response)
		title = response.meta['title']
		url = response.url
		data = (title, url)
		print data
		self.f.write('%s\n'%repr(data))
