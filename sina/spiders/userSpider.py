# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from sina.items import AimUserItem
import re
from sina.database import MongoDB

class UserspiderSpider(scrapy.Spider):
    db = MongoDB()
    name = 'userSpider'
    # allowed_domains = ['https://m.weibo.cn']

    # keys = SEARCH_KEYS
    scrawl_keys = list(db.Searchs.find({'searched':False}))  # 记录待爬的微博关键字

    # finish_keys = []

    def start_requests(self):
        while self.scrawl_keys.__len__():
            key_word = self.scrawl_keys.pop(0)
            print key_word
            self.db.add_searched(dict(key_word))
            # self.finish_keys.append(key_word)

            # 信息列表
            search_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type=3{key}{isv}%26specfilter=1%26{gender}' \
                         '{sbirth}{ebirth}{scho}{tags}'.format(
                             key='%26q=' +
                                 key_word['key'] if key_word.has_key(
                                     'key') else '',  # 搜索关键字
                             # 0表示普通用户，2表示个人认证
                             isv='%26isv=' + \
                                 key_word['isv'] if key_word.has_key(
                                     'isv') else '',
                             # gender = 1表示男生，2表示女生
                             gender='%26gender=' + \
                                 key_word['gender'] if key_word.has_key(
                                     'gender') else '',
                             sbirth='%26sbirth=' + \
                                 key_word['sbirth'] if key_word.has_key(
                                     'sbirth') else '',  # 1995 22默认
                             ebirth='%26ebirth=' + \
                                 key_word['ebirth'] if key_word.has_key(
                                     'ebirth') else '',  # 1998 19岁
                             scho='%26scho=' + \
                                 key_word['scho'] if key_word.has_key(
                                     'scho') else '',  # 学校
                             tags='%26tags=' + \
                                 key_word['tags'] if key_word.has_key(
                                     'tags') else '',  # 标签
                         )
            # url_information0 = "https://m.weibo.cn/api/container/getIndex?type=uid%26value=%s" % ID
            print search_url
            yield Request(url=search_url, meta={"key_word": key_word}, callback=self.parseInfo)

    def parseInfo(self, response):
        # checkWanghong()
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Users Success"
            print "###########################"

            aim_infos = json.loads(response.body)

            if aim_infos.get('msg',''):
                if aim_infos['msg'] == '这里还没有内容':
                    print aim_infos['msg']
                    return
                else:
                    print aim_infos['msg']
                    return

            if aim_infos.get("cards", ""):
                # print aim_infos['cards']
                if aim_infos['cards'][0].get('card_group',''):
                    for card in aim_infos['cards'][0]['card_group']:
                        aim_user = AimUserItem()
                        aim_user['ID'] =  card['user']['id'] # 微博ID
                        aim_user['NickName'] = card['user']['screen_name']  # 昵称
                        aim_user['Signature'] = card['user']['description']  # 个人简介
                        aim_user['Num_Tweets'] = card['user']['statuses_count']  # 微博数
                        aim_user['Num_Follows'] = card['user']['follow_count']  # 她关注的人数
                        aim_user['Num_Fans'] = card['user']['followers_count']  # 粉丝数
                        aim_user['profile_url'] = card['user']['profile_url']  # 主页链接

                        if check_fans(aim_user['Num_Fans']) or find_weishang(aim_user['Signature']):
                            pass
                        else:
                            yield aim_user

            if aim_infos.get("cardlistInfo", ""):
                if aim_infos['cardlistInfo']['page']:
                    print "###########################"
                    print "Next page is",aim_infos['cardlistInfo']['page']
                    print "###########################"
                    next_url = response.url + '&page=' + str(aim_infos['cardlistInfo']['page'])
                    yield Request(url=next_url, callback=self.parseInfo)
                else:
                    print "###########################"
                    print "Fetch Users Finished"
                    print "###########################"
                    return

        # saveID()

        # print response.body
        pass


#剔除微信和微商等等
def find_weishang(str):
    if str.find('微信')>-1:
        return True
    if str.find('微商')>-1:
        return True

    return False

#500粉丝以上 3万粉以下
def check_fans(num):
    if type(num) == type(1):
        if num<500:
            return True
        else:
            return False
    if type(num) == type('a'):
        int_str = re.findall(r'\d+',num)
        int_num = int(int_str[0])
        if int_num>2:
            return True
        else:
            return False


if __name__ == '__main__':
    print check_fans('32万')


