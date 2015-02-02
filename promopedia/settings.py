# -*- coding: utf-8 -*-

# Scrapy settings for promopedia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'promopedia'

SPIDER_MODULES = ['promopedia.spiders']
NEWSPIDER_MODULE = 'promopedia.spiders'
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'promopedia (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
DEPTH_LIMIT = 1


ITEM_PIPELINES = {
    # 'kaskusfjb.pipelines.KaskusFjbFilterOutDuplicate': 100,
    # 'kaskusfjb.pipelines.KaskusFjbMySQLStorePipeline': 110
    # 'kaskusfjb.pipelines.JsonWriterPipeline': 100
    'promopedia.pipelines.SanitizeTitlePipeline': 100,
    # 'promopedia.pipelines.CompileStoreLocationPipeline': 105,
    'promopedia.pipelines.DiskonbuzzSleignerelasticPipeline': 120,
    'promopedia.pipelines.ImportIntoMysqlPipeline': 125
}
