# -*- coding: utf-8 -*-

import pymongo
from items import InformationItem, TweetsItem, FollowsItem, FansItem, InfoDetailsItem
from scrapy.exceptions import DropItem
import os
import urllib

def save_img(img_url,file_name,file_path):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的  ~/weiboImgs文件夹
    try:
        if not os.path.exists(file_path):
            print '文件夹',file_path,'不存在，重新建立'
            #os.mkdir(file_path)
            os.makedirs(file_path)
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
       #下载图片，并保存到文件夹中
        urllib.urlretrieve(img_url,filename=filename)
        print '已将',filename,'保存到',file_path,'中'
    except IOError as e:
        print '文件操作失败',e
    except Exception as e:
        print '错误 ：',e


class MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]
        self.Details = db["Details"]

    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
            self.Information.update(
                {'_id': item['_id']}, dict(item), upsert=True)
            info_path = os.path.expanduser('~') + '/weiboimgs/' + item['NickName'] + '/info'
            if item['Avatar']:
                avatar_name = item['NickName']
                save_img(item['Avatar'],avatar_name,info_path)
            if item['Cover']:
                cover_name = item['NickName']+'-cover'
                save_img(item['Cover'],cover_name,info_path)

        elif isinstance(item, TweetsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
            self.Tweets.update({'_id': item['_id']}, dict(item), upsert=True)
            file_path = os.path.expanduser('~')+'/weiboimgs/'+item['Owner']+'/'+item['_id']
            # print file_path
            if item['Imgs']:
                for index, img in enumerate(item['Imgs']):
                    save_img(img,index,file_path)
            else:
                pass
                # print index, img

        elif isinstance(item, FollowsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
            self.Follows.update({'_id': item['_id']}, dict(item), upsert=True)
        elif isinstance(item, FansItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
            self.Fans.update({'_id': item['_id']}, dict(item), upsert=True)
        elif isinstance(item, InfoDetailsItem):
            for data in item:
                if not data:
                    raise DropItem("Missing data!")
            self.Details.update({'_id': item['_id']}, dict(item), upsert=True)
        return item
