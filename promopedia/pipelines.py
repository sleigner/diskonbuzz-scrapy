# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from string import capwords
from elasticsearch import Elasticsearch

class PromopediaPipeline(object):
    def process_item(self, item, spider):
        return item

class SanitizeTitlePipeline(object):
    def process_item(self, item, spider):
      title = item['title']
      item['title'] = title[title.index(":")+1:title.rindex("(")].strip()
      item['store_name'] = capwords(item['store_name'])

      return item

class CompileStoreLocationPipeline(object):
    

    def process_item(self, item, spider):
      item['store_locations'] = []

      for i in range (len(item['location_name'])):
        item['store_locations'].append({
              'location_name': item['location_name'][i],
              'location_address': item['location_address'][i],
              'location_district': item['location_district'][i],
              'location_city': item['location_city'][i],
              # 'location_extra_1': item['location_extra_1'][i],
              # 'location_extra_2': item['location_extra_2'][i]
            })

      return item

class DiskonbuzzSleignerelasticPipeline(object):
    def __init__ (self):
      self.es = Elasticsearch()

    def process_item(self, item, spider):
      self.es.index(index='promotion', doc_type='diskonbuzz_v1', id=item['promo_id'], body = { 'description': item['description'], 'title': item['title'], 'url': item['url'], 'store_name': item['store_name'], 'issuer': item['issuer'], 'start_date': item['start_date'], 'expiry_date': item['expiry_date'] })

      self.es.index(index='store', doc_type='diskonbuzz_v1', id=item['store_id'], 
          body = { 'store_name': item['store_name'], 'locations': item['store_locations'] } )
