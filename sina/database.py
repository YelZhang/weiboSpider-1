# -*- coding: utf-8 -*-
import pymongo
from sina.settings import SHENGHUI_KEYS,SCHOOL_KEYS
from account import DBADDRESS

class MongoDB():
    def __init__(self):
        client = pymongo.MongoClient(DBADDRESS, 27017)
        db = client["Sina"]
        self.Information = db["Information"] #某个具体ID的微博信息
        self.Tweets = db["Tweets"] #一张Tweets的表记录所有的微博
        self.Follows = db["Follows"] #关注的人的记录
        self.Fans = db["Fans"] #粉丝的记录
        self.Details = db["Details"] #某个具体ID的一些信息细节
        self.Aims = db['Aims'] #用来记录准备爬取还没爬取的微博ID
        self.Searchs = db['Searchs'] #用来记录搜索关键词
        self.Finished = db['Finished'] #用来记录爬完的ID
        self.Cookies = db['Cookies'] #用来记录爬取的cookies

    def add_searchs(self,item):
        if self.Searchs.find_one({'key':item['key'],'isv':item['isv'],'searched':item['searched'],'scho':item['scho']}) == None:
            self.Searchs.insert_one(item)
            print '-----------------------------------------'
            print 'insert_one_search', item['key']
            print '-----------------------------------------'
        else:
            print '-----------------------------------------'
            print 'Searchs already have'
            print '-----------------------------------------'

    def add_searched(self,item):
        # item['searched'] = True
        self.Searchs.update_one({'_id':item['_id']},{'$set':{'searched':True}})
        print 'key: ',item['key'],' isv:',item['isv'],' searched: ',item['searched']

    def add_finished(self,item):
        #aim->finished
        self.Finished.insert_one(item)
        print '-----------------------------------------'
        print item['ID'],' finished'
        print '-----------------------------------------'

    def findin_finished(self,item):
        if self.Finished.find_one({'ID':item['ID']}) == None:
            return False
        else:
            return True

    def find_cookie(self,item):
        if self.Cookies.find_one({'account':item['account']}) == None:
            return False
        else:
            return True

    def set_all_unsearched(self):
        if self.Searchs.find({'searched':True}) == None:
            pass
        else:
            cursor = self.Searchs.find({'searched':True})
            for key in cursor:
                self.Searchs.find_one_and_update(key,{'$set':{'searched':False}})
                print key['_id']

def set_keys():
    db = MongoDB()
    for key in SCHOOL_KEYS:
        item = {'key': '摄影', 'isv': '0', 'gender': '2', 'sbirth': '1992', 'ebirth': '1998', 'searched':False,'scho':key}
        item2 = {'key': '摄影', 'isv': '2', 'gender': '2', 'sbirth': '1992', 'ebirth': '1998', 'searched':False,'scho':key}

        # print key
        # key_str = str(key)
        # print key_str
        # print type(key_str)
        # print type('约拍')
        # key_str = key_str + '摄影'
        # print key_str
        # item['key'] = key_str
        print 'item: ',item
        db.add_searchs(item)
        # item2 = item
        # item2['isv'] = '2'
        print 'item2:', item2
        db.add_searchs(item2)

def set_allkeys_unsearched():
    db = MongoDB()
    db.set_all_unsearched()

if __name__ == '__main__':
    set_keys()
    # set_allkeys_unsearched()