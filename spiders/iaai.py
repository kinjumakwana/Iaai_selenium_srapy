import copy
import json
import re
import time
from urllib.parse import urljoin
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import random

class IaaiSpider(scrapy.Spider):
    name = 'iaai'
    base_url = 'https://www.iaai.com/'
    site_url = 'https://www.iaai.com/Search?url=QcS%2bxh3YwCeDU1vr3fjt1Dj1kxr2PKw62TMD4KYIpIA%3d'
    today = f'output/iaai.csv'
    custom_settings = {
        'FEED_URI': today,
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'ITEM_PIPELINES': {
            'Iaai.pipelines.StoreDataToMySQL': 1,
            'Iaai.pipelines.CustomMediaPipeline': 2
        },
        'IMAGES_STORE': 'media',
        'RETRY_TIMES': 5,
        'HTTPERROR_ALLOW_ALL': True,
        'ROBOTSTXT_OBEY': False,
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

    listing_headers = {
        'authority': 'www.iaai.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.iaai.com',
        'Referer': 'https://www.iaai.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                   
    }

    def start_requests(self):
        page_no = 1
        payload = copy.deepcopy(self.payload)
        payload['CurrentPage'] = page_no
        print("page_no",page_no)
        
        wait_no = random.randint(1,5)
        print("start_requests",wait_no)
        
        yield SeleniumRequest(url=self.site_url, callback=self.parse_listing_page,
                             meta={'page_no': page_no, 'payload': payload}, wait_time=wait_no)
        # wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'quote'))

    def parse_listing_page(self, response):
        # print (response.body) 
        wait_no = random.randint(1,5)
        print("parse_listing_page",wait_no)
        
        # wait = WebDriverWait(self.browser, 10)
        print("Path: " + response.request.url)
        print("Response: " + response.text)
        
        print("logo: ",response.xpath("/html/body/section/header/div[2]/div/div[1]/a/@href").get())
        
        payload = response.meta.get('payload')
        page_no = response.meta.get('page_no')
        print("page_no",page_no)
        # print("payload",payload)
        
        one_url = response.xpath(".//div[contains(@class,'table-body border')]").get()
        print(one_url)
        
        # Wait until a list of detail URLs is present
        # Wait until a list of detail URLs is present
        # try:
        #     detail_urls = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[contains(@class,"table-body border")]/div//h4/a')))
        #     detail_urls = [url.get_attribute("href") for url in detail_urls]

        # except TimeoutException:
        #     print("Timed out waiting for element to be present")

        print("detail_urls", detail_urls)

        # try:
        #     wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[contains(@class,"table-body border")]/div//h4/a/@href')))
        
        # except TimeoutException:
        #     print("Timed out waiting for element to be clickable")
        
        detail_urls = response.xpath('.//div[contains(@class,"table-body border")]/div//h4/a/@href').getall()
        print("detail_urls",detail_urls)
        time.sleep(wait_no)  
        
        if detail_urls:
            for url in detail_urls:
                # Scroll the link into view
                print("url:", url)
                script = "arguments[0].scrollIntoView();"
                self.execute_script(script, url)
                                    
                time.sleep(wait_no)  
                yield scrapy.Request(url=urljoin(self.base_url, url), callback=self.parse_detail_page,
                                     meta={'listing_url': f'{response.url} -> (page_no {page_no})'})

            page_no += 1
            payload['CurrentPage'] = page_no
            print(f"wait for {wait_no} min")
            
            yield SeleniumRequest(method='POST', url=response.url, callback=self.parse_listing_page,
                                     headers=self.listing_headers, body=json.dumps(payload),
                                     meta={'page_no': page_no, 'payload': payload}, wait_time=wait_no)

    def parse_detail_page(self, response):
        wait_no = random.randint(1,5)
        print("parse_detail_page",wait_no)
        
        # wait = WebDriverWait(self.browser, 10)
        # # Wait until a specific script element is present
        # script_element = wait.until(EC.presence_of_element_located((By.XPATH, './/script[@id="ProductDetailsVM"]/text()')))
        # json_data = script_element.get('{}')
    
        # wait.until(EC.presence_of_element_located((By.XPATH, './/script[@id="ProductDetailsVM"]/text()')))
        json_data = response.xpath('.//script[@id="ProductDetailsVM"]/text()').get('{}')
        time.sleep(wait_no)
         
        json_data = json.loads(json_data)
        print(json_data)
        images, video = self.get_media_urls(json_data)
        print(f"images is {images} video is {video}")
        
        time.sleep(wait_no)
        
        item = dict()
        item['Listing_Url'] = response.meta.get('listing_url')
        item['Detail_Url'] = response.url
        
        item['Title'] = response.xpath('.//section[@class="section section--vehicle-title"]//h1/text()').get('').strip()
        item['Vehicle_Information'] = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        item['Price'] = response.xpath('.//div[@class="action-area__secondary-info"]//span[text()="Buy Now Price:"]'
                                       '/following-sibling::span/text()').get('').strip()
        item['Vehicle_Description'] = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        item['Auction_Date_Time'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Auction Date and Time:"]/following-sibling::*//text()').getall())).strip()
        item['Actual_Cash_Value'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Actual Cash Value:"]/following-sibling::*//text()').getall())).strip()
       
        item['Seller'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Seller:"]/following-sibling::*//text()').getall())).strip()
        
        item['Images_Urls'] = images
        item['Video_Url'] = video
        name = '_'.join(re.findall('\w+', item.get('Title')))
        item['Images_Names'] = ', '.join([f'{name}_{index + 1}.jpg' for index, img in enumerate(images.split(', '))])
        item['Video_Name'] = f'{name}.mp4' if item.get('Video Url') != '' else ''
        print("item: ", item)
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
