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