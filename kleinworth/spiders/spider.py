import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import KleinworthItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class KleinworthSpider(scrapy.Spider):
	name = 'kleinworth'
	start_urls = ['https://www.kleinworthambros.com/en/tags/tag/press-releases/',
				  'https://www.kleinworthambros.com/en/tags/tag/news/'
				  ]

	def parse(self, response):
		post_links = response.xpath('//div[contains(@id,"card2")]/@data-href | //div[@class="taxoWrap"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="sgnews_single_date"]/text()').get()
		title = response.xpath('(//h1//text())[last()]').get()
		content = response.xpath('//div[@class="intro"]//text()').getall() + response.xpath('//div[@class="sgnews_single_content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=KleinworthItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
