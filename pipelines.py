from itemadapter import ItemAdapter
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
from scrapy.exceptions import NotConfigured

load_dotenv()

config = os.environ

class MongoPipeline:
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MONGOPIPELINE_ENABLED'):
            # if this isn't specified in settings, the pipeline will be completely disabled
            raise NotConfigured
        return cls()

    def process_item(self, item, spider):
        # change my item
        return item
    def open_spider(self, spider):
        hostname = config['hostname']
        port = int(config['port'])
        database = config['database']
        
        self.client = MongoClient(hostname, port)
        self.db = self.client[database]
        self.collection = self.db['sightings']
    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = ItemAdapter(item).asdict()
        # Create a unique index for (date, city, state, shape) to avoid duplicate entries
        self.collection.create_index([('occured', 1), ('city', 1), ('state', 1), ('summary', 1)], unique=True)
        
        try:
            self.collection.insert_one(item)
        except errors.DuplicateKeyError:
            spider.logger.info('Duplicate item found: %s', item)
        except Exception as e:
            spider.logger.error('An error occurred: %s', e)

        return item




