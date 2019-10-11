from scrapy import Spider
from zipcode.items import ZipcodeItem


class ZipcodeSpider(Spider):
    name = "zipcode_spider"
    allowed_urls = ['https://www.zipcodestogo.com/']
    start_urls = ['https://www.zipcodestogo.com/New%20Jersey/']

    def parse(self, response):
    	rows = response.xpath('//table[@class="inner_table"]//tr')

    	for row in rows[2:]:
    		
    		item = ZipcodeItem()
    		item['zipcode'] = row.xpath('./td[1]/a/text()').extract_first()
    		item['city'] = row.xpath('./td[2]/text()').extract_first()
    		item['county'] = row.xpath('./td[3]/a/text()').extract_first()

    		yield item 
