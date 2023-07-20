# Scrapy settings for Iaai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Iaai'

SPIDER_MODULES = ['Iaai.spiders']
NEWSPIDER_MODULE = 'Iaai.spiders'



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Iaai (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Iaai.middlewares.IaaiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Iaai.middlewares.IaaiDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Iaai.pipelines.IaaiPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# settings.py
# for chrome driver 
# AUTOTHROTTLE_ENABLED = True
# # ROTATING_PROXY_LIST_PATH = 'proxies.txt'
# ROTATING_PROXY_LIST = [
#    '208.180.237.55:31012','54.160.234.152:8080'
# ]

# from shutil import which
  
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = r'C:\Users\BAPS\.wdm\drivers\chromedriver\win32\113.0.5672.63\chromedriver.exe'
# # SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
# # SELENIUM_DRIVER_ARGUMENTS=['--headless']  
# SELENIUM_DRIVER_ARGUMENTS=['--disable-dev-shm-usage']  
# SELENIUM_DRIVER_ARGUMENTS=['--disable-extentions']  
# SELENIUM_DRIVER_ARGUMENTS=['--no-sandbox']  
# SELENIUM_DRIVER_ARGUMENTS=['--start-maximized']  
# SELENIUM_DRIVER_ARGUMENTS=['--remote-debugging-port=9222']  
# SELENIUM_DRIVER_ARGUMENTS=['user-data-dir=C:\\Users\\BAPS\\AppData\\Local\\Google\\Chrome\\User Data']  
# SELENIUM_DRIVER_ARGUMENTS=['--profile-directory=Profile 5']  
  
# DOWNLOADER_MIDDLEWARES = {
#      'scrapy_selenium.SeleniumMiddleware': 800,
#      # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
# #      'scrapy_rotating_proxies.middlewares.RotatingProxyMiddleware': 350,
#      # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#      'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
#      'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#      'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
     
#      }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
    # 'scrapy_brightdata.BrightDataProxyMiddleware': 610,
    

    
}

HTTP_PROXY = 'http://brd-customer-hl_4d1c7dbf-zone-residential:5qgj4rnvh9g0@brd.superproxy.io:22225'