from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from tutorial.items import DmozItem
from scrapy.http import Request

class DmozSpider(CrawlSpider):
	name = "dmoz"
	
	allowed_domains = ["wikisource.org"]
	start_urls = ["http://wikisource.org/wiki/Category:%E0%A4%95%E0%A4%B9%E0%A4%BE%E0%A4%A8%E0%A4%BF%E0%A4%AF%E0%A4%BE%E0%A4%81"]
	
	rules = (Rule(SgmlLinkExtractor(allow=("index\d00\.html", ), restrict_xpaths=('//p[@class="nextpage"]',))
        , callback="parse_items", follow=True),)
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		#sites = hxs.select('//h3/text()').extract()
		#hindi = hxs.select('//li/a/text()').extract()
		#urls = hxs.select('//li/a/@href').extract()
		u  = hxs.select('//li')
		i=0;
		#global t	
		t = open('a.txt','w')	
		items = []
		for h in u:
			if i==85:
				break;
			item = DmozItem()
			url = h.select('a/@href').extract()
			title =  h.select('a/text()').extract()
			if not url or not title:
				continue;
			add=url[0].encode('utf8')
			tit = title[0].encode('utf8')
			add = 'http://wikisource.org' + add 			
			#item['url'] =  add
			#item['title'] = tit
			i = i+1
			#t.write(tit + '\n' + add + '\n\n')
			#items.append(item)
			yield Request(url=add, meta={'url': url}, callback=self.parse_items)
		#t.close();
		#return items;

	def parse_items(self,response):
		t = open('a.txt','a')
		#print "second function\n"
		hxs = HtmlXPathSelector(response)
		#t.write(response.body,'\n\n')
		title = hxs.select('//title/text()').extract()[0].encode('utf8')
		title = title[:-10] 
		t.write(title + "\n\n");
		paras = hxs.select('//p/text()').extract()
		#parags = paras[0].encode('utf8')
		#t.write(parags + '\n\n')
		for p in paras:	
			p = p.encode('utf8')
			if not p or len(p) < 20:
				continue	
			t.write(p + '\n\n')
			#print p
		t.write('\n\n\n\nEnd of Story\n\n\n\n\n')		
		t.close()
