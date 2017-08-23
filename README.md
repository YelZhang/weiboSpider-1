# weiboSpider
A spider based on scrapy to get infomation from https://m.weibo.cn/

### requirements
- you need: Python2.7 Scrapy 1.4.0 MongoDB Selenium  Pycharm

### before you start to craw
- make a new file `account.py` in root file
- add following code
    ```
    WEIBO_ACCOUNT = [
    {'no':'your-account','psw':'your-password'},
    {'no':'your-account','psw':'your-password'},
    {'no':'your-account','psw':'your-password'},
    ]
    ```
- And then you run this order in the derectory under CFG file: scrapy crawl sinaSpider

## Finally  
Do not forget to give a STAR~ Thank you
###Todo List
- [ ] add search spider
- [ ] delete same infos
- [ ] get basic infos of Hust stars
- [ ] use FE pages to mongodb
- [ ] distributed crawler
