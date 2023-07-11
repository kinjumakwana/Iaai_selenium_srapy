import os
import re
import urllib.request

import mysql.connector
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class CustomMediaPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        name = '_'.join(re.findall('\w+', item.get('Title')))
        for key, value in item.items():
            if key == 'Images_Urls':
                for index, url in enumerate(value.split(', ')):
                    yield scrapy.Request(url=url, meta={'file_name': f'{name}_{index + 1}.jpg'})
            if key == 'Video_Url' and value != '':
                self.download_video(value, f'media/{name}.mp4')

    @staticmethod
    def download_video(url, file_name):
        print('Please Wait Downloading the Video')
        urllib.request.urlretrieve(url, file_name)

    def file_path(self, request, response=None, info=None, *, item=None):
        return os.path.basename(request.meta.get('file_name'))

    def item_completed(self, results, item, info):
        return item


class StoreDataToMySQL:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.table_name = 'yoewalle_a2wp169_tb'
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='yoewalle_a2wp169',
            password='yoewalle_a2wp169_2020',
            database='yoewalle_a2wp169'
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name}(
                    Listing_Url VARCHAR(255),
                    Detail_Url VARCHAR(255),
                    Title VARCHAR(255),
                    Vehicle_Information LONGTEXT,
                    Price VARCHAR(255),
                    Vehicle_Description LONGTEXT,
                    Auction_Date_Time VARCHAR(255),
                    Actual_Cash_Value VARCHAR(255),
                    Seller VARCHAR(255),
                    Images_Urls LONGTEXT,
                    Video_Url LONGTEXT,
                    Images_Names LONGTEXT,
                    Video_Name VARCHAR(255)
        )""")

    def store_db(self, item):
        command = (f"INSERT INTO {self.table_name} "
                   f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (
            item['Listing_Url'],
            item['Detail_Url'],
            item['Title'],
            item['Vehicle_Information'],
            item['Price'],
            item['Vehicle_Description'],
            item['Auction_Date_Time'],
            item['Actual_Cash_Value'],
            item['Seller'],
            item['Images_Urls'],
            item['Video_Url'],
            item['Images_Names'],
            item['Video_Name'])
        self.cursor.execute(command, data)
        self.connection.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def close_spider(self, spider):
        self.connection.close()
        self.cursor.close()
