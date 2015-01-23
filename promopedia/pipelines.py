# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch

class PromopediaPipeline(object):
    def process_item(self, item, spider):
        return item

class SanitizeTitlePipeline(object):
    def process_item(self, item, spider):
      title = item['title']
      item['title'] = title[title.index(":")+1:title.rindex("(")].strip()

      return item

class DiskonbuzzSleignerelasticPipeline(object):
    def __init__ (self):
      self.es = Elasticsearch()

    def process_item(self, item, spider):
      self.es.index(index='promotion', doc_type='diskonbuzz_v1', id=item['promo_id'], body = { 'description': item['description'], 'title': item['title'], 'url': item['url'], 'store': item['store'], 'issuer': item['issuer'], 'start_date': item['start_date'], 'expiry_date': item['expiry_date'] })
