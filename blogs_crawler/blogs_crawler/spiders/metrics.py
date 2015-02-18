'''from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import requests
import urllib2
from scrapy.http import FormRequest, Request
import csv, sys
filename = 'blogerpedia - pedia.csv'

class Blogssample(BaseSpider):
        name = "blogsample"
        start_urls = []
	f = open('simple.txt', 'w')

	DICT = {}
	def start_requests(self):
		import pdb;pdb.set_trace()
		with open('blogerpedia - pedia.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				url = row[1]
				
        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                urlss = "".join(hxs.select('//div[@class="leftimg"]/a/@href').extract())
                urls = urlss.replace('http://', '')
                return [FormRequest(url="https://pingler.com/seo-tools/tools/google-indexed-pages-checker/", method="post",
                        formdata={'f_url': urls, 'a': 'submit'}, callback=self.parse_next, meta= {'urls': urlss})]


        def parse_next(self, response):
                hxs = HtmlXPathSelector(response)
                urlss = response.meta['urls']
                hxs = HtmlXPathSelector(response)
                index = hxs.select('//table[@width="100%"]//tr//td//text()').extract()
                if index:
                        index = index[-1]
                else:
                        index = ""
                urls = "http://tools.seochat.com/tools/page-link-analyzer-seo//?imageverify=&timehsh=415673355053303d&go=1&tool=13&url=%s&display=both&rel=1&submit=Show+Links" %(urlss)
                yield Request(urls, callback = self.parse_details, meta = {'urls': urlss, 'index': index})

        def parse_details(self, response):
                urlss = response.meta['urls']
     		hxs = HtmlXPathSelector(response)
                index = response.meta['index']
                ex_data = "".join(hxs.select('//tr//th[contains(text(), "External Links")]//text()').extract()).replace('External Links: ', '').strip()
                in_data = "".join(hxs.select('//tr//th[contains(text(), "Internal Links")]//text()').extract()).replace('Internal Links: ', '').strip()
                urls = urlss.replace('http://', '')
                web_ref = "http://my.websiteanalysis.com/get-stats/?div=site&id=%s" %(urls)
                web_desc = urllib2.urlopen(web_ref).read()
                sel = HtmlXPathSelector(text = web_desc)
                details = sel.select('//div[@class="stat-info-table"]//table/tr/td[2]//text()').extract()
                page_rank = details[0]
                domain_authority = details[1]
                mozrank = details[2]
                moztrust = details[3]
                alax_rank = details[4]
                ref = "http://my.websiteanalysis.com/get-content/?div=site&id=%s" %(urls)
                desc = urllib2.urlopen(ref).read()
                sel = HtmlXPathSelector(text = desc)
                detail = sel.select('//table[@class="content-table"]//td[3]/text()').extract()
                title = detail[1].strip()
                descr = detail[2].strip()
                reference = "http://www.alexa.com/siteinfo/%s" %(urls)
                referen = urllib2.urlopen(reference).read()
                refe = HtmlXPathSelector(text = referen)
                alx_country = "".join(refe.select('//div[@class="rank-row"]//a//@title').extract())
                alx_traffic = refe.select('//strong[@class="metrics-data align-vmiddle"]//text()').extract()
                alx_globrank = alx_traffic[0]
                status = requests.head(urlss)
                who = "http://who.is/whois/%s" %(urls)
                who_is = urllib2.urlopen(who).read()
                sel = HtmlXPathSelector(text = who_is)
                ip_add = "".join(sel.select('//td[@data-bind-domain="ip_address"]//a[contains(@href, "/whois-ip/ip-address")]//text()').extract())
                data_ = (urlss, page_rank, domain_authority, mozrank, moztrust, alax_rank, title, descr, alx_country, alx_globrank, status, ip_add, ex_data, in_data, index)
                print data_
		self.f.write('%s\n'%repr(data_))'''
