import sys
import copy
import json
import re
import time
from urllib.parse import urljoin
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

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1

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
        'user-agent': user_agent_list[randint(0, len(user_agent_list)-1)]
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                   
    }

    
    def get_proxy_response(self):
        if sys.version_info[0] == 3:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(
                    {'http': 'http://brd-customer-hl_4d1c7dbf-zone-residential:5qgj4rnvh9g0@brd.superproxy.io:22225',
                    'https': 'http://brd-customer-hl_4d1c7dbf-zone-residential:5qgj4rnvh9g0@brd.superproxy.io:22225'}))

            response = urllib.request.urlopen('http://lumtest.com/myip.json').read()
            print(response)
            return response
        
    def get_proxy_ip(self,response):
        response_data = json.loads(response.decode('utf-8'))
        ip_address = response_data.get('ip')
        print(ip_address)
        return ip_address

    def wait_between(self, a, b):
        rand=uniform(a, b)
        time.sleep(rand)
        
    def start_requests(self):
        proxy_response = self.get_proxy_response()
        print("proxy_response", proxy_response)
        proxy_ip = self.get_proxy_ip(proxy_response)
        print("proxy_ip", proxy_ip)
        
        if proxy_ip:
            # Use the extracted IP address as the proxy for Scrapy
            proxy = f"http://{proxy_ip}:22225"
            self.log(f"Using proxy: {proxy}")
            page_no = 1
            payload = copy.deepcopy(self.payload)
            payload['CurrentPage'] = page_no
            print("page_no",page_no)
            print(self.listing_headers)
            # wait_no = randint(1,5)
            self.log("Wait")
            self.wait_between(MIN_RAND, MAX_RAND)
            
            yield scrapy.Request(url=self.site_url, callback=self.parse_listing_page,
                                meta={'page_no': page_no, 'payload': payload, 'proxy': proxy_ip})
            # wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'quote'))

    def parse_listing_page(self, response):
        # self.logger.info('IP address: %s' % response.text)
        self.logger.info(f"HTML content for URL {response.url}: {response.text}")
        proxy_ip = response.meta['proxy']
        print(proxy_ip)
        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
        # print(response.meta['proxy'])
        # print (response.body) 
        # self.browser = Chrome()
        # self.browser = response.url
        # After scrolling the link into view
        # script = "arguments[0].scrollIntoView();"
        # self.browser.execute_script(script, self.site_url)
        a = randint(1,100)
        b = randint(a + 1, 500)
         
        x_offset = randrange(a, b)
        y_offset = randrange(a, b)
        
        print("x_offset:", x_offset)
        print("y_offset:", y_offset)
        # Simulate mouse movement
        browser = response.meta['driver']
        
        element = browser.find_element(By.XPATH,'/html/body')
        actions = ActionChains(browser)
        # actions.send_keys(Keys.ARROW_DOWN)
        # actions.perform()
        actions.move_to_element(element)
        actions.move_by_offset(x_offset, y_offset)  # Move the mouse 100 pixels to the right
        print(x_offset,y_offset)
        print("Action: ", actions)
        actions.perform()

        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
        
        # wait = WebDriverWait(self.browser, 10)
        print("Path: " + response.request.url)
        print("Response: " + response.text)
        
        print("logo: ",response.xpath("/html/body/section/header/div[2]/div/div[1]/a/@href").get())
        
        payload = response.meta.get('payload')
        page_no = response.meta.get('page_no')
        print("page_no",page_no)
        # print("payload",payload)
        
        # Wait until a list of detail URLs is present
        # Wait until a list of detail URLs is present
        # try:
        #     detail_urls = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[contains(@class,"table-body border")]/div//h4/a')))
        #     detail_urls = [url.get_attribute("href") for url in detail_urls]

        # except TimeoutException:
        #     print("Timed out waiting for element to be present")

        # try:
        #     wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[contains(@class,"table-body border")]/div//h4/a/@href')))
        
        # except TimeoutException:
        #     print("Timed out waiting for element to be clickable")
        
        detail_urls = response.xpath('.//div[contains(@class,"table-body border")]/div//h4/a/@href').getall()
        print("detail_urls",detail_urls)
        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
        
        if detail_urls:
            for url in detail_urls:
                # Scroll the link into view
                print("url:", url)
                # script = "arguments[0].scrollIntoView();"
                # self.execute_script(script, url)
                                    
                self.log("Wait")
                self.wait_between(MIN_RAND, MAX_RAND) 
                yield scrapy.Request(url=urljoin(self.base_url, url), callback=self.parse_detail_page,
                                     meta={'listing_url': f'{response.url} -> (page_no {page_no})'})

            page_no += 1
            payload['CurrentPage'] = page_no
            
            yield scrapy.Request(method='POST', url=response.url, callback=self.parse_listing_page,
                                     headers=self.listing_headers, body=json.dumps(payload),
                                     meta={'page_no': page_no, 'payload': payload})

    def parse_detail_page(self, response):
        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
        # wait = WebDriverWait(self.browser, 10)
        # # Wait until a specific script element is present
        # script_element = wait.until(EC.presence_of_element_located((By.XPATH, './/script[@id="ProductDetailsVM"]/text()')))
        # json_data = script_element.get('{}')
    
        # wait.until(EC.presence_of_element_located((By.XPATH, './/script[@id="ProductDetailsVM"]/text()')))
        json_data = response.xpath('.//script[@id="ProductDetailsVM"]/text()').get('{}')
        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
         
        json_data = json.loads(json_data)
        print(json_data)
        images, video = self.get_media_urls(json_data)
        print(f"images is {images} video is {video}")
        
        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)
        
        item = dict()
        item['Listing_Url'] = response.meta.get('listing_url')
        item['Detail_Url'] = response.url
        
        item['Title'] = response.xpath('.//section[@class="section section--vehicle-title"]//h1/text()').get('').strip()
        
        ###### Vehicle_Information #####
        item['Vehicle_Information'] = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        
        # Vehicle_Information_data = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li').get_all()
        # print(Vehicle_Information_data)
        
        # # Iterate over each field
        # for data in Vehicle_Information_data:
        # # Get the text of the field
        #     field_text = ' '.join(data.xpath('./span/text()').getall()).strip()

        #     # Split the field text into title and value
        #     title, value = field_text.split(':', 1)

        #     # Clean up the title and value by removing extra spaces
        #     title = re.sub('\s+', ' ', title).strip()
        #     value = re.sub('\s+', ' ', value).strip()

        #     print(f"Title is {title} and value is {value}")
            
        #     # Store the field in the item dictionary
        #     item[title] = value

        # # Check if the 'Stock' field is available and store it separately
        # if 'Stock' in item:
        #     item['Stock'] = item['Stock']
        
        item['Stock'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Stock #:"]/following-sibling::*//text()"').get()
        print("item['Stock'] :", item['Stock'])
        
        item['Selling_Branch'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Selling Branch:"]/following-sibling::*//text()').get()
        print("item['Selling_Branch']:", item['Selling_Branch'])
        
        item['Loss'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Loss:"]/following-sibling::*//text()').get()
        print("item['Loss']:", item['Loss'])
        
        item['Primary_Damage'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Primary Damage:"]/following-sibling::*//text()').get()
        print("item['Primary_Damage']:", item['Primary_Damage'])
        
        item['Title/Sale_Doc'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Title/Sale Doc:"]/following-sibling::*//text()').get()
        print("item['Title/Sale_Doc']:", item['Title/Sale_Doc'])
        
        item['Start_Code'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Start Code:"]/following-sibling::*//text()').get()
        print("item['Start_Code']:", item['Start_Code'])
        
        item['Key'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Key:"]/following-sibling::*//text()').get()
        # //h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[@id="key_image_div"]
        print("item['Key']: ", item['Key'])
        
        item['Odometer'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Odometer:"]/following-sibling::*//text()').get()
        print("item['Odometer']:", item['Odometer'])
        
        item['Airbags'] = response.xpath('.//h2[text()="Vehicle Information"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Airbags:"]/following-sibling::*//text()').get()
        print("item['Airbags']:", item['Airbags'])
        
        #### Price ####
        item['Price'] = response.xpath('.//div[@class="action-area__secondary-info"]//span[text()="Buy Now Price:"]'
                                       '/following-sibling::span/text()').get('').strip()
        # Vehicle_Description #######
        
        item['Vehicle_Description'] = '\n'.join(
            [re.sub('\s+', ' ', ' '.join(data.xpath('./span/text()').getall())).strip() for data in response.xpath(
                './/h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li')]).strip()
        
        Vehicle_Description = response.xpath('.//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li').get_all()
        print(Vehicle_Description)
        
        # item['VIN_Status'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="VIN (Status):"]/following-sibling::*//text()').get()
        # .//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li/span/following-sibling::*//text()
        item['Vehicle'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Vehicle:"]/following-sibling::*//text()').get()
        print("item['Vehicle']", item['Vehicle'] )
        
        item['Body_Style'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Body Style:"]/following-sibling::*//text()').get()
        print("item['Body_Style']:", item['Body_Style'])
        
        item['Engine'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Engine:"]/following-sibling::*//text()').get()
        print("item['Engine']:", item['Engine'])
        
        item['Transmission'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Transmission:"]/following-sibling::*//text()').get()
        print("item['Transmission']:", item['Transmission'])
        
        item['Drive_Line_Type'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Drive Line Type:"]/following-sibling::*//text()').get()
        print("item['Drive_Line_Type']:", item['Drive_Line_Type'])
        
        item['Fuel_Type'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Fuel Type:"]/following-sibling::*//text()').get()
        print("item['Fuel_Type']: ", item['Fuel_Type'])
        
        item['Cylinders'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Cylinders:"]/following-sibling::*//text()').get()
        print("item['Cylinders']:", item['Cylinders'])
        
        item['Restraint_System'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Restraint System:"]/following-sibling::*//text()').get()
        print("item['Restraint_System']:", item['Restraint_System'] )
        
        item['Exterior/Interior'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Exterior/Interior:"]/following-sibling::*//text()').get()
        print("item['Exterior/Interior']: ", item['Exterior/Interior'])
        
        item['Options'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Options:"]/following-sibling::*//text()').get()
        print("item['Options']", item['Options'])
        
        item['Manufactured_In'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Manufactured In:"]/following-sibling::*//text()').get()
        print("item['Manufactured_In']:", item['Manufactured_In'])
        
        item['Vehicle_Class'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Vehicle Class:"]/following-sibling::*//text()').get()
        print("item['Vehicle_Class']:", item['Vehicle_Class'])
        
        item['Model'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Model:"]/following-sibling::*//text()').get()
        print("item['Model']", item['Model'])
        
        item['Series'] = response.xpath('//h2[text()="Vehicle Description"]/../..//ul[@class="data-list data-list--details"]/li//span[text()="Series:"]/following-sibling::*//text()').get()
        print("item['Series']:", item['Series'])

        # SALE INFORMATION ###
        item['Auction_Date_Time'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Auction Date and Time:"]/following-sibling::*//text()').getall())).strip()
        item['Actual_Cash_Value'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Actual Cash Value:"]/following-sibling::*//text()').getall())).strip()
       
        item['Seller'] = re.sub('\s+', ' ', ' '.join(
            response.xpath('.//span[text()="Seller:"]/following-sibling::*//text()').getall())).strip()
        
        # Images and Videos #############
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
