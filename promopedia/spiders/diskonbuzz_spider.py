from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join, Identity
from scrapy.contrib.linkextractors import LinkExtractor
import re

from promopedia.items import PromopediaItem

class DiskonbuzzSpider(CrawlSpider):
  name = "diskonbuzz"
  allowed_domains = ["www.diskonbuzz.com"]
  start_urls = ["http://www.diskonbuzz.com"]

  rules = ( 
      Rule(LinkExtractor(allow=['/promo/\d+\Z']), 'parse_post'),
      Rule(LinkExtractor(allow=['/category/\d+\Z'])),
      Rule(LinkExtractor(allow=['/subcategory/\d+\Z'])),
      Rule(LinkExtractor(allow=['/issuer/\d+\Z'])),
      Rule(LinkExtractor(allow=['/merchant/\d+\Z']))
  )

  # def start_requests(self):
  #   # POST request
  #   # s_category_id=&s_merchant_location_id=&s_issuer_id=1&search_keyword=search+for&search=1
  #   return [scrapy.FormRequest("http://www.diskonbuzz.com",
  #     formdata={'s_issuer_id': '1', 'search': '1'},
  #     callback=self.issuer_selected)]
  #
  # def issuer_selected(self, response):
  #
  #   pass

  def parse_post(self, response):
    post = ItemLoader(item=PromopediaItem(), response=response)
    post.default_output_processor = TakeFirst()
    post.default_input_processor = Identity()
    post.description_out = Join()

    post.add_value('url', response.url)
    post.add_value('promo_id', response.url[response.url.rindex("/")+1:])
    post.add_xpath('title', '//*[@id="content"]/div/table/tr/td/table[1]/tr[1]/td[2]/h1/text()')
    post.add_xpath('description', '//*[@id="content"]/div/table/tr/td/table[2]//td/p/text()')
    post.add_xpath('start_date', '//*[@id="content"]/div/table/tr/td/table[2]/tr[4]/td[2]/strong[1]/text()')
    post.add_xpath('expiry_date', '//*[@id="content"]/div/table/tr/td/table[2]/tr[4]/td[2]/strong[2]/text()')
    post.add_xpath('issuer', '//*[@id="content"]/div/table//tr/td/table[2]/tr[2]/td[2]/font/a/text()')
    post.add_xpath('store', '//*[@id="content"]/div/table/tr/td/table[2]/tr[1]/td[2]/font/a/text()')
    return post.load_item()
