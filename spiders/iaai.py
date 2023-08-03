import base64
import sys
import copy
import json
import re
import time
from urllib.parse import urljoin, urlparse
import pandas as pd
import scrapy
from selenium.webdriver import Chrome
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random import uniform, randint, randrange
import urllib.request
import six
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1

PROXY_IP ='brd.superproxy.io'
PROXY_PORT = 22225
USERNAME = 'brd-customer-hl_4d1c7dbf-zone-unblocker'
PASSWORD = 't61t6izqysqt'

class IaaiSpider(scrapy.Spider):
    name = 'iaai'
    base_url = 'https://www.iaai.com/'
    # site_url = 'https://lumtest.com/myip.json'
    site_url = 'https://www.iaai.com/Search?url=QcS%2bxh3YwCeDU1vr3fjt1Dj1kxr2PKw62TMD4KYIpIA%3d'
    today = f'output/iaai.csv'
    custom_settings = {
        'FEED_URI': today,
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'ITEM_PIPELINES': {
            'Iaai.pipelines.StoreDataToMySQL': 1,
            'Iaai.pipelines.CustomMediaPipeline': 2,
        },
        'IMAGES_STORE': 'media',
        'RETRY_TIMES': 5,
        'HTTPERROR_ALLOW_ALL': True,
        'ROBOTSTXT_OBEY': False,
        'PROXY_AUTHENTICATION_ENABLED':True
    }
    payload = {
        'Searches': [
            {
                'Facets': [
                    {
                        'Group': 'AuctionType',
                        'Value': 'Buy Now',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
            {
                'Facets': [
                    {
                        'Group': 'InventoryTypes',
                        'Value': 'SUVs',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
            {
                'Facets': [
                    {
                        'Group': 'Market',
                        'Value': 'United States',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
            {
                'Facets': [
                    {
                        'Group': 'WhoCanBuy',
                        'Value': 'Available to the public',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
            {
                'Facets': None,
                'FullSearch': None,
                'LongRanges': [
                    {
                        'From': 2018,
                        'Name': 'Year',
                        'To': 2024,
                    },
                ],
            },
            {
                'Facets': [
                    {
                        'Group': 'IsDemo',
                        'Value': 'False',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
            {
                'Facets': [
                    {
                        'Group': 'InventoryTypes',
                        'Value': 'Automobiles',
                    },
                ],
                'FullSearch': None,
                'LongRanges': None,
            },
        ],
        'ZipCode': '',
        'miles': 0,
        'PageSize': 100,
        'CurrentPage': 0,
        'Sort': [
            {
                'IsGeoSort': False,
                'SortField': 'AuctionDateTime',
                'IsDescending': False,
            },
        ],
        'SaleStatus': 0,
        'BidStatus': 6,
    }

    user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    ]
    listing_headers = {
        'authority': 'www.iaai.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.iaai.com',
        'Referer': 'https://www.iaai.com',
        # 'user-agent': user_agent_list[randint(0, len(user_agent_list)-1)]
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                   
    }

    def wait_between(self, a, b):
        rand=uniform(a, b)
        time.sleep(rand)
    
    def start_requests(self):
        
        # Add the proxy with authentication to ChromeOptions
        # proxy = f"http://{USERNAME}:{PASSWORD}@{PROXY_IP}:{PROXY_PORT}"
        proxy = 'http://brd-customer-hl_4d1c7dbf-zone-unblocker:t61t6izqysqt@brd.superproxy.io:22225'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.site_url)
        
        page_no = 1
        payload = copy.deepcopy(self.payload)
        payload['CurrentPage'] = page_no
        
        # Generate proxy authorization headers
        username, password = proxy.split('@')[0].split('://')[1].split(':')
        encoded_auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {'Proxy-Authorization': f'Basic {encoded_auth}'}
        
        yield scrapy.Request(url=self.site_url, callback=self.parse_listing_page,
                            meta={'page_no': page_no, 'driver': driver, 'proxy': proxy, 'headers': headers})
   
    def parse_listing_page(self, response):
        driver = response.meta['driver']
        proxy = response.meta['proxy']
        headers = response.meta['headers']
        
        # print("Path: " + response.request.url)
        # print("Response: " + response.text)
        # print("logo: ",response.xpath("/html/body/section/header/div[2]/div/div[1]/a/@href").get())
        
        payload = response.meta.get('payload')
        page_no = response.meta.get('page_no')
        print("page_no",page_no)
        
        detail_urls = response.xpath('.//div[contains(@class,"table-body border")]/div//h4/a/@href').getall()
        # print("detail_urls",detail_urls)
        # self.log("Wait")
        # self.wait_between(MIN_RAND, MAX_RAND)
        url_data = []
        if detail_urls:
            for url in detail_urls:
                # Scroll the link into view
                # print("url:", url)
                d_url = urljoin(self.base_url, url)
                url_data.append(d_url)
                df = pd.DataFrame(url_data)
                df.to_csv('car_data.csv', header=False, index=False)
                # print(df)
                # next_btn = response.xpath("/html/body/section/main/main/section[3]/div/div/div[2]/div[2]/div/div/div/button[3]")
                # next_btn.click()
                # script = "arguments[0].scrollIntoView();"
                # self.execute_script(script, url)
                                    
    #             self.log("Wait")
    #             self.wait_between(MIN_RAND, MAX_RAND) 
                yield scrapy.Request(url=d_url, callback=self.parse_detail_page,
                                     headers=headers,
                                     meta={'proxy': proxy} )

            page_no += 1
            # payload['CurrentPage'] = page_no
            
            yield scrapy.Request(method='POST', url=response.url, callback=self.parse_listing_page,
                                     headers=self.listing_headers, body=json.dumps(payload),
                                     meta={'page_no': page_no, 'payload': payload})

    def parse_detail_page(self, response):
        print("parse_detail_page")
        proxy = response.meta['proxy']
        # print("Proxy: ", proxy)
        
        # You need to use Selenium to get the page content, as Scrapy's downloader won't use the proxy
        print(response.url)
        # print("Response: " + response.text)
        time.sleep(5)
    
        json_data = response.xpath('.//script[@id="ProductDetailsVM"]/text()').get('{}')
        # self.log("Wait")
        time.sleep(5)
        json_data = json.loads(json_data)
        images, video = self.get_media_urls(json_data)
        # print(f"images is {images} video is {video}")
        
        item = dict()
        # item['Listing_Url'] = response.meta.get('listing_url')
        item['Detail_Url'] = response.url
        time.sleep(5)
        item['Title'] = response.xpath('.//section[@class="section section--vehicle-title"]//h1/text()').get('').strip()
        
    #     ###### Vehicle_Information #####
        vehicle_info = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        
        # vehicle_info = item['Vehicle_Information']

        lines = vehicle_info.split('\n')
        for line in lines:
            key_value = line.split(': ')
            if len(key_value) == 2:
                key, value = key_value
                item[key.strip()] = value.strip()
                # print(item)
        
    #     #### Price ####
        item['Price'] = response.xpath('.//div[@class="action-area__secondary-info"]//span[text()="Buy Now Price:"]'
                                       '/following-sibling::span/text()').get('').strip()
    #     # Vehicle_Description #######
        
        Vehicle_Description = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        print("Vehicle_Description", Vehicle_Description)
        
        lines = Vehicle_Description.split('\n')
        for line in lines:
            key_value = line.split(': ')
            if len(key_value) == 2:
                key, value = key_value
                item[key.strip()] = value.strip()
                # print(item)
 
    #     # SALE INFORMATION ###
        item['Auction_Date_Time'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Auction Date and Time:"]/following-sibling::*//text()').getall())).strip()
        item['Actual_Cash_Value'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Actual Cash Value:"]/following-sibling::*//text()').getall())).strip()
       
        item['Seller'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Seller:"]/following-sibling::*//text()').getall())).strip()
        
    #     # Images and Videos #############
        item['Images_Urls'] = images
        item['Video_Url'] = video
        name = '_'.join(re.findall('\w+', item.get('Title')))
        item['Images_Names'] = ', '.join([f'{name}_{index + 1}.jpg' for index, img in enumerate(images.split(', '))])
        item['Video_Name'] = f'{name}.mp4' if item.get('Video Url') != '' else ''
        # print("item: ", item)
        
        yield item

    @staticmethod
    def get_media_urls(json_data):
        images = list()
        json_data = json_data.get('inventoryView', {}).get('imageDimensions', {})
        for img in json_data.get('keys', {}).get('$values', []):
            height = img.get('h') // 3
            width = img.get('w') // 3
            images.append(f'https://vis.iaai.com/resizer?imageKeys={img.get("k")}&width={width}&height={height}')
        return ', '.join(images), json_data.get('vrdUrl', '')

    def closed(self, reason):
        if hasattr(self, 'driver'):
            self.driver.quit()