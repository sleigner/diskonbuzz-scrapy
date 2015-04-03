from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join, Identity
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
import re

from promopedia.items import PromopediaItem

class DiskonbuzzSpider(CrawlSpider):
  name = "diskonbuzz"
  allowed_domains = ["www.diskonbuzz.com"]
  # start_urls = ["http://www.diskonbuzz.com"]
  #
  # for i in range(23840,23896):
  #   start_urls.append("http://www.diskonbuzz.com/promo/" + `i`)

  rules = ( 
      Rule(LinkExtractor(allow=['/promo/\d+\Z']), 'parse_post'),
      # Rule(LinkExtractor(allow=['/category/\d+\Z'])),
      # Rule(LinkExtractor(allow=['/subcategory/\d+\Z'])),
      # Rule(LinkExtractor(allow=['/issuer/\d+\Z'])),
      # Rule(LinkExtractor(allow=['/merchant/\d+\Z']))
  )

  def start_requests(self):
    for i in range(23840, 23896):
      yield Request('http://www.diskonbuzz.com/promo/%d' % i, callback=self.parse_post)

  def parse_post(self, response):
    post = ItemLoader(item=PromopediaItem(), response=response)
    post.default_output_processor = TakeFirst()
    post.default_input_processor = Identity()
    post.description_out = Join()
    post.locations_out = Identity()
    post.locations2_out = Identity()

    post.add_value('url', response.url)
    post.add_value('promo_id', response.url[response.url.rindex("/")+1:])
    post.add_xpath('title', '//*[@id="content"]/div/table/tr/td/table[1]/tr[1]/td[2]/h1/text()')
    post.add_xpath('description', '//*[@id="content"]/div/table/tr/td/table[2]//td/p/text()')
    post.add_xpath('start_date', '//*[@id="content"]/div/table/tr/td/table[2]/tr[4]/td[2]/strong[1]/text()')
    post.add_xpath('expiry_date', '//*[@id="content"]/div/table/tr/td/table[2]/tr[4]/td[2]/strong[2]/text()')
    post.add_xpath('issuer', '//*[@id="content"]/div/table//tr/td/table[2]/tr[2]/td[2]/font/a/text()')
    post.add_xpath('store_name', '//*[@id="content"]/div/table/tr/td/table[2]/tr[1]/td[2]/font/a/text()')
    post.add_xpath('store_id', '//*[@id="content"]/div/table/tr/td/table[2]/tr[1]/td[2]/font/a/@href')
    post.add_xpath('locations', '//*[@id="content"]/div/table/tr/td/table[2]/tr[8]/td/table/tr/td[1]/ul/li')
    post.add_xpath('locations2', '//*[@id="content"]/div/table/tr/td/table[2]/tr[9]/td/table/tr/td[1]/ul/li')
    return post.load_item()
