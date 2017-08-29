# -*- coding: utf-8 -*-
import re
import datetime
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import json
from sina.items import InformationItem, TweetsItem, FollowsItem, FansItem, InfoDetailsItem
from sina.settings import Tweets_Num, IDS
from sina.database import MongoDB

class SinaspiderSpider(CrawlSpider):
    name = "sinaSpider"
    # allowed_domains = ['https://m.weibo.cn']
    # start_urls=[
    # 	5340337769,1642630543,1704116960,1310630777,
    # ]
    # headers={
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en,zh-CN;q=0.8,zh;q=0.6",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    #     "Host": "www.douban.com",
    # }
    db = MongoDB()
    # ids = IDS
    # scrawl_ID = set(ids)  # 记录待爬的微博ID
    # finish_ID = set()  # 记录已爬的微博ID

    # scrawl_KEYS = set(SEARCH_KEYS)
    def start_requests(self):
        #从aims取出目标ID
        #爬取之后放在finished中去
        while self.db.Aims.find_one()!=None:
            ID_item = self.db.Aims.find_one()
            self.db.Aims.delete_one({'ID': ID_item['ID']})
            print '-----------------------------------------'
            print ID_item['ID']
            print '-----------------------------------------'
            ID = str(ID_item['ID'])
            # self.finish_ID.add(ID)
            #判断是否已经finish
            if self.db.findin_finished(ID_item):
                print '-----------------------------------------'
                print 'WARNING:  ', ID, ' already finished'
                print '-----------------------------------------'
                self.db.Aims.delete_one(ID_item)
                continue
            else:
            # 个人信息
                url_information0 = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s" % ID
                print url_information0
                yield Request(url=url_information0, meta={"ID": ID_item['ID']}, callback=self.parseInformation)



    def parseInformation(self, response):
        """ 抓取个人信息1 """
        if len(response.body) > 50:
            print "###########################"
            print "Fetch information0 Success"
            print "###########################"
            ID = response.meta['ID']
            # self.db.Aims.delete_one({'ID': ID})
            self.db.Finished.insert_one({'ID':ID})
            informationItems = InformationItem()
            informations = json.loads(response.body)
            # print informations
            if informations.get("userInfo", ""):
                # print informations["userInfo"]
                informationItems["_id"] = informations["userInfo"]["id"]
                informationItems["NickName"] = informations["userInfo"]["screen_name"]
                informationItems["Signature"] = informations["userInfo"]["description"]
                informationItems["Num_Tweets"] = informations["userInfo"]["statuses_count"]
                informationItems["Num_Follows"] = informations["userInfo"]["follow_count"]
                informationItems["Num_Fans"] = informations["userInfo"]["followers_count"]
                informationItems["User_Url"] = informations["userInfo"]["profile_url"]
                informationItems['Avatar'] = informations["userInfo"]["profile_image_url"]
                informationItems['LocalAvatar'] = ''
                informationItems['Cover'] = informations["userInfo"]['cover_image_phone']
                informationItems['LocalCover'] = ''
                informationItems['Used'] = False
                yield informationItems

            # # 微博入口
            # tweets_container_id = informations["tabsInfo"]["tabs"][1]["containerid"]
            # url_tweets = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s" % (
            #     response.meta["ID"], tweets_container_id)
            # yield Request(url=url_tweets, meta={"ID": response.meta["ID"],'owner':informations["userInfo"]["screen_name"]},
            # callback=self.parseTweets, dont_filter=True)

            # 原创微博入口
            # 先请求一次获得微博主页


            # 详细信息入口
            info_container_tabs = informations["tabsInfo"]["tabs"]


            #原创微博入口
            #先获取一个主页的url

            # info_container_id = ''
            info_raw_id = ''
            for tab in info_container_tabs:
                if tab['tab_type'] == "profile":
                    info_container_id = tab['containerid'] + \
                        '_' + '-' + '_INFO'
                    # print info_container_id
                    info_raw_id = tab['containerid']
                    home_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s' % (
                        response.meta["ID"], info_raw_id)
                    yield Request(url=home_url, meta={"detail_id": info_raw_id, 'ID': response.meta["ID"],
                                                'owner': informations["userInfo"]["screen_name"]},
                            callback=self.parseHome, dont_filter=True)


                    url_details = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s' % (
                        response.meta["ID"], info_container_id)
                    yield Request(url=url_details, meta={"detail_id": info_container_id,'ID':response.meta["ID"],'owner':informations["userInfo"]["screen_name"]},
                                  callback=self.parseDetails, dont_filter=True)
                    break

            #处理主页获取原创微博的ID

            # 关注者入口
            # if informations.get("follow_scheme", ""):
            #     follow_scheme = informations["follow_scheme"]
            #     follow_container_id = re.findall(
            #         r"containerid=(.*)", follow_scheme)
            #     follow_container_id[0] = follow_container_id[0].replace(
            #         'followersrecomm', 'followers')
            #     url_follow = "https://m.weibo.cn/api/container/getIndex?containerid=" + \
            #         follow_container_id[0]
            #     yield Request(url=url_follow, meta={"ID": response.meta["ID"]}, callback=self.parseFollows, dont_filter=True)

            # 粉丝入口
            # if informations.get("fans_scheme", ""):
            #     fans_scheme = informations["fans_scheme"]
            #     fans_container_id = re.findall(
            #         r"containerid=(.*)", fans_scheme)
            #     fans_container_id[0] = fans_container_id[0].replace(
            #         'fansrecomm', 'fans')
            #     url_fans = "https://m.weibo.cn/api/container/getIndex?containerid=" + \
            #         fans_container_id[0]
            #     yield Request(url=url_fans, meta={"ID": response.meta["ID"]}, callback=self.parseFans, dont_filter=True)
        else:
            print "###########################"
            print "Fetch information0 Fail"
            print "###########################"
            return

    def parseHome(self,response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Home Success"
            print "###########################"
            infos = json.loads(response.body)
            if infos.get('cards', ''):
                cards = infos['cards']
                for card in cards:
                    if card['card_type'] == 6:
                        print '========================================='
                        #获得原创ID的那一串数字
                        ori_ID = re.findall(r'\d+',card['actionlog']['oid'])[0]
                        ori_url = 'https://m.weibo.cn/api/container/getIndex?containerid={ori_id}_-_WEIBO_SECOND_PROFILE_WEIBO_ORI&type=uid&page_type=03&value={value}'.format(
                            ori_id = ori_ID,value=response.meta['ID']
                        )
                        print 'ori_ID:',ori_ID
                        yield Request(url=ori_url, meta={'ID': response.meta["ID"],'ori_id': ori_ID, 'owner':response.meta['owner']},
                                      callback=self.parseTweets, dont_filter=True)

    def parseDetails(self, response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch InfoDetails Success"
            print "###########################"
            print response.url
            infos = json.loads(response.body)
            details = InfoDetailsItem()
            details['_id'] = response.meta['detail_id']
            details['ID'] = response.meta['ID']
            if infos.get('cards', ''):
                cards = infos['cards']
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                print json.dumps(cards)
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                print '========================================='
                for card in cards:
                    if card.get('card_group', ''):
                        card_group = card['card_group']
                        for group in card_group:
                            if group.get('item_name', ''):
                                if group['item_name'] == '昵称':
                                    details['NickName'] = group['item_content']
                                    print details['NickName']
                                elif group['item_name'] == '标签':
                                    print group['item_content']
                                    details['WeiboTag'] = group['item_content']
                                elif group['item_name'] == '性别':
                                    details['Gender'] = group['item_content']
                                elif group['item_name'] == '所在地':
                                    details['Place'] = group['item_content']
                                elif group['item_name'] == '简介':
                                    details['Intro'] = group['item_content']
                                elif group['item_name'] == '等级':
                                    details['Rank'] = group['item_content']
                                elif group['item_name'] == '学校':
                                    details['School'] = group['item_content']
                                elif group['item_name'] == '注册时间':
                                    details['RegTime'] = group['item_content']
                                else:
                                    pass
            yield details


    def parseTweets(self, response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Tweets Success"
            print "###########################"
            ori_ID = response.meta['ori_id']
            tweets = json.loads(response.body)
            ID = response.meta["ID"]
            Owner = response.meta["owner"]
            page = ''
            containerid = ''
            if tweets.get("cards", ""):
                cards = tweets["cards"]
                if tweets["cardlistInfo"].get("page", ""):
                    page = tweets["cardlistInfo"]["page"]
                    page = str(page)
                else:
                    return
                # if tweets["cardlistInfo"].get("containerid", ""):
                #     containerid = tweets["cardlistInfo"]["containerid"]
                for card in cards:
                    mblog = card.get('mblog', '')
                    if mblog:
                        tweetsItems = TweetsItem()
                        tweetsItems["_id"] = mblog["id"]
                        tweetsItems["ID"] = ID
                        tweetsItems["Owner"] = Owner
                        tweetsItems["Used"] = False
                        tweetsItems['LocalImgs'] = []
                        tweetsItems["Content"] = json.dumps(mblog).decode('unicode-escape')
                        tweetsItems["PubTime"] = mblog["created_at"]
                        tweetsItems["Like"] = mblog["attitudes_count"]
                        tweetsItems["Comment"] = mblog["comments_count"]
                        tweetsItems["Transfer"] = mblog["reposts_count"]
                        tweetsItems["TweetsText"] = mblog["text"]
                        pics = mblog.get('pics', '')
                        if pics:
                            img_urls = []
                            small_img_urls = []
                            # print mblog["pics"]
                            for pic in pics:
                                url = pic["large"]['url']
                                surl = pic['url']
                                # print url
                                img_urls.append(url)
                                small_img_urls.append(surl)
                            tweetsItems["Imgs"] = img_urls
                            tweetsItems['SmallImgs'] = small_img_urls
                        else:
                            tweetsItems["Imgs"] = []
                            tweetsItems['SmallImgs'] = []
                    yield tweetsItems
                print "###########################"
                print "Tweetspage: " + page
                print "###########################"
                if page >= Tweets_Num:
                    print "###########################"
                    print "Fetch Tweets Finish"
                    print "###########################"
                    return
                # url_tweets = "https://m.weibo.cn/api/container/getIndex?type=uid&value={value}&containerid={ori_id}&page=%s" % (
                    # ID, containerid, page)
                ori_url = 'https://m.weibo.cn/api/container/getIndex?containerid={ori_id}_-_WEIBO_SECOND_PROFILE_WEIBO_ORI' \
                          '&type=uid&page_type=03&value={value}&page={page}'.format(
                    ori_id=ori_ID, value=response.meta['ID'],page=page
                )
                yield Request(url=ori_url, meta={"ID": ID}, callback=self.parseTweets, dont_filter=True)
            else:
                return
        else:
            print "###########################"
            print "Fetch Tweets Finish"
            print "###########################"
            return

    def parseFollows(self, response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Follows Success"
            print "###########################"

            page = ''
            containerid = ''
            follow = json.loads(response.body)
            if follow.get("cardlistInfo", ""):
                if follow["cardlistInfo"].get("page", ""):
                    page = follow["cardlistInfo"]["page"]
                    page = str(page)
                else:
                    return
                if follow["cardlistInfo"].get("containerid", ""):
                    containerid = follow["cardlistInfo"]["containerid"]
            else:
                return

            ID = response.meta["ID"]
            if follow.get("cards", ""):
                cards = follow["cards"]
                card_group = cards[len(cards) - 1]["card_group"]
                for card in card_group:
                    if card:
                        followsItems = FollowsItem()
                        followsItems["ID"] = ID
                        followsItems["_id"] = card["user"]["id"]
                        followsItems["NickName"] = card["user"]["screen_name"]
                        followsItems["Signature"] = card["desc1"]
                        followsItems["Num_Tweets"] = card["user"]["statuses_count"]
                        followsItems["Num_Follows"] = card["user"]["follow_count"]
                        followsItems["Num_Fans"] = card["user"]["followers_count"]
                        followsItems["profile_url"] = card["user"]["profile_url"]
                        yield followsItems
                print "###########################"
                print "Followspage: " + page
                print "###########################"
                url_follow = "https://m.weibo.cn/api/container/getIndex?containerid=%s&page=%s" % (
                    containerid, page)
                yield Request(url=url_follow, meta={"ID": ID}, callback=self.parseFollows, dont_filter=True)
            else:
                return
        else:
            print "###########################"
            print "Fetch Follows Finish"
            print "###########################"
            return

    def parseFans(self, response):
        if len(response.body) > 50:
            print "###########################"
            print "Fetch Fans Success"
            print "###########################"

            fans = json.loads(response.body)
            ID = response.meta["ID"]
            containerid = ''
            since_id = ''
            if fans.get("cardlistInfo", ""):
                if fans["cardlistInfo"].get("since_id", ""):
                    since_id = fans["cardlistInfo"]["since_id"]
                    since_id = str(since_id)
                else:
                    return
                    if fans["cardlistInfo"].get("containerid", ""):
                        containerid = fans["cardlistInfo"]["containerid"]

            if fans.get("cards", ""):
                cards = fans["cards"]
                for card in cards:
                    card_group = card["card_group"]
                    for element in card_group:
                        if element:
                            fansItems = FansItem()
                            fansItems["_id"] = element["user"]["id"]
                            fansItems["ID"] = ID
                            fansItems["NickName"] = element["user"]["screen_name"]
                            fansItems["Signature"] = element["user"]["description"]
                            fansItems["Num_Tweets"] = element["user"]["statuses_count"]
                            fansItems["Num_Follows"] = element["user"]["follow_count"]
                            fansItems["Num_Fans"] = element["user"]["followers_count"]
                            fansItems["profile_url"] = element["user"]["profile_url"]
                            yield fansItems

                print "###########################"
                print "Fas_since_id: " + since_id
                print "###########################"
                fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=%s&since_id=%s" % (
                    containerid, since_id)
                yield Request(url=fans_url, meta={'ID': ID}, callback=self.parseFans, dont_filter=True)
            else:
                return
        else:
            print "###########################"
            print "Fetch Fans Finish"
            print "###########################"
            return
