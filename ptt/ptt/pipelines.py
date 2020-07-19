# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import re

class PttPipeline(object):
    def process_item(self, item, spider):
        match = re.search('[\u4e00-\u9fa5]{2}',item['title']).group()
        if match == '公告':
            raise DropItem('已排除公告')
        else:
            return item
