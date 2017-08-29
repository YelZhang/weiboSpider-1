# encoding=utf-8
import random
from cookies import cookies
from user_agents import agents
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  

class UserAgentMiddleware(UserAgentMiddleware):

    def process_request(self,request,spider):
        agent=random.choice(agents)        
        request.headers.setdefault('User-Agent',agent)

class CookiesMiddleware(object):

    def process_request(self,request,spider):
        cookie=random.choice(cookies)       
        request.cookies=cookie

class RandomProxyMiddleware(object):
    #动态设置ip代理
    def process_request(self, request, spider):
        request.meta["proxy"] = "http://lum-customer-qifanliu-zone-static:ogzwqi0a7qx8@zproxy.luminati.io:22225"
        print request.url
