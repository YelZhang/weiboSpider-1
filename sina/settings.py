# -*- coding: utf-8 -*-

# Scrapy settings for sina project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'
DOWNLOAD_DELAY = 0.25

DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    "sina.middlewares.UserAgentMiddleware": 401,
    "sina.middlewares.CookiesMiddleware": 402,
    "sina.middlewares.RandomProxyMiddleware":403,
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipleline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
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
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sina.middlewares.SinaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'sina.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'sina.pipelines.SinaPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


Tweets_Num = 10 #每个人爬取的微博数目
#要爬取的微博列表
IDS = [
        # "2693420092",'5328954059','2557885734','3703890107','2639867183',
        # '2261711905','1986228780','3752596494','2571174542','2588915485',
        # '2230590702','2230590702','3135217391','2003976183','2339556763',
        # '6066035966','5110131420','1789126750','1796999941','3645733454',
        # '1940631755','3645733454','1933527560','2525313413','2821525763',
        # '2318087163','2625816705','5119046205','6012212811','5442606278',
]

SEARCH_KEYS = [ #{'key':'旅行','isv':'0','gender':'2','sbirth':'1992','ebirth':'1998','scho':'南京大学','tags':'旅行'},
               # {'key': '旅行', 'isv': '2', 'gender': '2', 'sbirth': '1992', 'ebirth': '1998', 'scho': '南京大学',},
               ]

SCHOOL_KEYS = ["西安交通大学","南开大学","国防科学技术大学","中山大学","兰州大学","清华大学","中央民族大学","东南大学","中南大学","四川大学","电子科技大学","湖南大学","南京大学","复旦大学","中国人民大学","大连理工大学","吉林大学","北京理工大学","北京大学","中国科学技术大学","华南理工大学","西北农林科技大学","哈尔滨工业大学","西北工业大学","重庆大学","华东师范大学","武汉大学","浙江大学","上海交通大学","同济大学","北京航空航天大学","中国海洋大学","东北大学","山东大学","北京师范大学","厦门大学","天津大学","中国农业大学"]

SHENGHUI_KEYS = ["合肥","太原","沈阳","银川","昆明","武汉","贵阳","长春","兰州","广州","西宁","南昌","西安","成都","海口","拉萨","福州","南京","杭州","南宁","郑州","乌鲁木齐","呼和浩特","济南","哈尔滨","石家庄","长沙",]
KEYS = ['旅行','摄影','美食','健身','旅游']


