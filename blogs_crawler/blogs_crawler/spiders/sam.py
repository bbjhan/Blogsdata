from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import requests
import urllib2
from scrapy.http import FormRequest, Request
import csv, sys

class Blogssam(BaseSpider):
        name = "blogsampl"
        start_urls = []
        DATA= {}
	f1 = open('/home/bibeejan/Desktop/blogadda1.txt', 'a+')
        def start_requests(self):
		file_ = [i.strip() for i in open('blodsdomain.txt.csv', 'r').readlines()]
		for filee in file_:
			url = filee.split(',')[-1]
			print url
			yield Request(url, callback= self.parse)
	def parse(self, response):
                hxs = HtmlXPathSelector(response)
                urlss = response.url
                urls = urlss.replace('http://', '')
                return [FormRequest(url="https://pingler.com/seo-tools/tools/google-indexed-pages-checker/", method="post",
                        formdata={'f_url': urls, 'a': 'submit'}, callback=self.parse_index, meta= {'urls': urlss})]
	
	def parse_index(self, response):
                hxs = HtmlXPathSelector(response)
                urlss = response.meta['urls']
                hxs = HtmlXPathSelector(response)
                index = hxs.select('//table[@width="100%"]//tr//td//text()').extract()
                if index:
                        index = index[-1]
                else:
                        index = ''
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
		data = {'index': index, 'ex_data': ex_data, 'in_data' : in_data}
		yield Request(web_ref, callback = self.parse_deta, meta = {'urls': urlss, 'data': data})
			
	def parse_deta(self, response):
		urlss = response.meta['urls']
		urls = urlss.replace('http://', '')
                sel = HtmlXPathSelector(response)
		data = response.meta['data']
		details = sel.select('//div[@class="stat-info-table"]//table/tr/td[2]//text()').extract()
                page_rank = details[0]
                domain_authority = details[1]
                mozrank = details[2]
                moztrust = details[3]
                alax_rank = details[4]
		data.update({'mozrank': mozrank, 'alax_rank': alax_rank, 'domain_authority': domain_authority, 'page_rank': page_rank})
		ref = "http://my.websiteanalysis.com/get-content/?div=site&id=%s" %(urls)
		yield Request(ref, callback = self.parse_title, meta = {'urls': urlss, 'data':data})
	def parse_title(self, response):
		urlss = response.meta['urls']
                urls = urlss.replace('http://', '')
                sel = HtmlXPathSelector(response)
	        data = response.meta['data']
                detail = sel.select('//table[@class="content-table"]//td[3]/text()').extract()
                title = detail[1].strip()
                descr = detail[2].strip()
		data.update({'title': title, 'descr': descr})
		reference = "http://www.alexa.com/siteinfo/%s" %(urls)
		yield Request(reference, callback = self.parse_rank, meta = {'urls': urlss, 'data':data})
		
	def parse_rank(self, response):
		urlss = response.meta['urls']
		urls = urlss.replace('http://', '')
		data = response.meta['data']
		refe = HtmlXPathSelector(response)
                alx_country = "".join(refe.select('//div[@class="rank-row"]//a//@title').extract())
                alx_traffic = refe.select('//strong[@class="metrics-data align-vmiddle"]//text()').extract()
                alx_globrank = alx_traffic[0]
                status = requests.head(urlss)
		data.update({'alx_country': alx_country, 'alx_traffic': alx_traffic, 'alx_globrank': alx_globrank, 'status': status})
		who = "http://who.is/whois/%s" %(urls)
		yield Request(who, callback = self.parse_ip, meta = {'urls': urlss, 'data':data})
	def parse_ip(self, response):
		urlss = response.meta['urls']
		urls = urlss.replace('http://', '')
                data = response.meta['data']
		sel = HtmlXPathSelector(response)
                ip_add = "".join(sel.select('//td[@data-bind-domain="ip_address"]//a[contains(@href, "/whois-ip/ip-address")]//text()').extract())
		data.update({'ip_add':ip_add})
		return [FormRequest(url="http://www.checkmoz.com/", method="post",
                        formdata={'f_urls': urls}, callback=self.parse_page, meta= {'urls': urlss, 'data': data})]
	def parse_page(self, response):
		sel = HtmlXPathSelector(response)
		urlss = response.meta['urls']
		data = response.meta['data']
		details = sel.select('//table[@id="tblstats"]//tr//td//text()').extract()
		DA = details[1]
		PA = details[2]
		BACK = details[4]
		data_ = (urlss, data['page_rank'], data['domain_authority'], data['mozrank'], data['alax_rank'], data['title'], data['descr'], data['alx_country'], data['alx_globrank'], data['status'], data['ip_add'], data['ex_data'], data['in_data'], data['index'], PA, BACK)
                print data_
		self.f1.write('%s\n'%repr(data_))
		
