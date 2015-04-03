# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from string import capwords
from elasticsearch import Elasticsearch
from HTMLParser import HTMLParser

import ConfigParser
import re

# -*- coding: utf-8 -*-
import MySQLdb as mdb

class PromopediaPipeline(object):
    def process_item(self, item, spider):
        return item

class DiskonBuzzLocationParser(HTMLParser):
    def __init__ (self, store_name, location_index):
      HTMLParser.__init__(self)
      self.location_id = None
      self.store_name = store_name
      self.location_index = location_index
      self.location_details = []

    def handle_starttag(self, tag, attrs):
      if tag == 'a':
        self.location_id = attrs[0][1]

    def handle_data(self, data):
      if data == "Other Location":
        data = self.store_name + ' ' + `self.location_index`

      self.location_details.append(data)

class SanitizeTitlePipeline(object):
    def process_item(self, item, spider):
      title = item['title']
      item['title'] = title[title.index(":")+1:title.rindex("(")].strip()
      item['store_name'] = capwords(item['store_name'])

      return item

class ParseLocationsPipeline(object):
    def process_item(self, item, spider):

      if 'locations2' in item:
        # item['locations'] = list(item['locations2'])
        item['locations'] = item['locations2']

      locations = []

      if 'locations' in item:
          for i in range(len(item['locations'])):
              location_parser = DiskonBuzzLocationParser(item['store_name'], i+1)
              location_parser.feed(item['locations'][i])
              locations.append(location_parser.location_details)
          item['locations_parsed'] = locations

      return item

class DiskonbuzzSleignerelasticPipeline(object):
    def __init__ (self):
      self.es = Elasticsearch()

    def process_item(self, item, spider):
      self.es.index(index='promotion', doc_type='diskonbuzz_v1', id=item['promo_id'], body = { 'description': item['description'], 'title': item['title'], 'url': item['url'], 'store_name': item['store_name'], 'issuer': item['issuer'], 'start_date': item['start_date'], 'expiry_date': item['expiry_date'] })

      self.es.index(index='store', doc_type='diskonbuzz_v2', id=item['store_id'], 
          body = { 'store_name': item['store_name'], 'locations': item['locations'] } )

      return item

class ImportIntoMysqlPipeline(object):
      def __init__ (self):
        config = ConfigParser.ConfigParser()
        config.read('/home/sleigner/scrapy/promopedia/database.ini')
        self.mysqlCon = mdb.connect(host=config.get('MySql', 'host'), port=config.getint('MySql', 'port'), user=config.get('MySql', 'user'), passwd=config.get('MySql', 'passwd'), db=config.get('MySql', 'db'));
        self.mysqlCon.autocommit(False)

      def process_item(self, item, spider):

        with self.mysqlCon:
            cur = self.mysqlCon.cursor(mdb.cursors.DictCursor)
            store_name = item['store_name']
            cur.execute("SELECT * from stores where title LIKE '%" + store_name + "%'")
            rows = cur.fetchall()

            if len (rows) > 0:
              print "Store exists: " + rows[0]['title']
              return item

            print "Adding store: " + store_name
            store_name = "'" + store_name + "'"
            query = "INSERT INTO stores(title,description) VALUES(" + ','.join([store_name, store_name]) + ")"
            print query
            cur.execute(query)
            new_store_id = cur.lastrowid
            # cur.execute("INSERT into stores(title, description) VALUES(" + ','.join([store_name, store_name]) + ")")
            for location in item['locations_parsed']:

              location_name = None
              location_address = None
              location_city = None

              for i in range(len(location)):
                if i == 0:
                  location_name = location[i]
                  # print location[i]


                jlMatch = re.match( r'^jl', location[i], re.I )
                if jlMatch:
                  location_address = location[i]
                  # print location[i]

                jakartaMatch = re.match( r'jakarta', location[i], re.I )
                if jakartaMatch:
                  location_city = location[i]
                  # print location[i]


              cur.execute("SELECT * from locations where name = '" + location_name + "'")
              rows = cur.fetchall()

              location_id = 0
              if len (rows) > 0:
                print "Location exists: " + rows[0]['name']
                location_id = rows[0]['id']
              else:
                print "Adding location: " + location_name
                location_name = "'" + location_name + "'" if (location_name is not None) else "''"
                location_address = "'" + location_address + "'" if (location_address is not None) else "''"
                query = "INSERT INTO locations(name,address,district_id,city_id) VALUES(" + location_name + "," + location_address + ",0,10)"
                print query
                cur.execute(query)
                location_id = cur.lastrowid

              cur.execute("SELECT * from store_locations where store_id=" + str(new_store_id) + " AND location_id=" + str(location_id))
              rows = cur.fetchall()
              if len (rows) > 0:
                print "Store's location have been added: " + str(new_store_id) + "," + str(location_id)
                location_id = rows[0]['id']
              else:
                query = "INSERT INTO store_locations(store_id,location_id) VALUES(" + ",".join([str(id) for id in [new_store_id, location_id]]) + ")"
                print query
                cur.execute(query)

        return item

