from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import re

DOMAIN = "http://blogtoplist.com"
class BlogToplists(BaseSpider):
        name = "blogtoplist"
        start_urls = ['http://blogtoplist.com/']
        f = open('/home/bibeejan/Desktop/blogtoplists.tx', 'a+')
        data ={}
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                nodes = hxs.select('//a[contains(@class, "Item")]')
                for node in nodes:
                        ref_url = "".join(node.select('.//@href').extract())
                        title =  "".join(node.select('.//text()').extract())
                        ref_url = DOMAIN +ref_url
			if title in ['Show All', 'Submit Blog', 'Edit Account', 'How it works', 'FAQ']:
				continue
                        yield Request(ref_url, callback=self.parse_next, meta = {'title': title})
        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
                nodes = hxs.select('//tr//td[@class="bloginfo"]//a')
                for node in nodes:
                        url = "".join(node.select('.//@href').extract())
                        url = DOMAIN + url
                        yield Request(url, callback=self.parse_ne, meta = {'title': title})
                refere = hxs.select('//a[contains(@href, "page")]')
                for ref in refere:
                        ref_ = "".join(ref.select('.//@href').extract())
                        ref_ = DOMAIN +ref_
                        yield Request(ref_, callback = self.parse_next, meta = {'title': title})
	def parse_ne(self, response):
                hxs = HtmlXPathSelector(response)
                title = response.meta['title']
		url = "".join(re.findall('href\=\"(.*)\"', response.body))
		print url
                data = (title, url)
                self.f.write('%s\n'%repr(data))
                print data


