# encoding=utf-8
import sys
import time
from selenium import webdriver
from account import WEIBO_ACCOUNT
from database import MongoDB
reload(sys)
sys.setdefaultencoding('utf8')
# myWeiBo=[
# 	{'no':'your account','psw':'your password'},
# ]
myWeiBo = WEIBO_ACCOUNT
# 存到数据库里面方便使用


def getCookies(weibo):
    db = MongoDB()
    cookies = []
    loginURL = 'https://passport.weibo.cn/signin/login'

    if db.Cookies.count() < 10:

        print '-----------------------------------------'
        print 'Start crawl cookies'
        print '-----------------------------------------'

        for elem in weibo:
            account = elem['no']
            password = elem['psw']
            item = {'account':account}
            if db.find_cookie(item):
                continue
            try:
                driver = webdriver.Chrome()
                driver.get(loginURL)
                time.sleep(2)

                failure = 0
                while "登录 - 新浪微博" in driver.title and failure < 5:
                    failure += 1
                    driver.set_window_size(1920, 1080)
                    username = driver.find_element_by_id("loginName")
                    username.clear()
                    username.send_keys(account)

                    psd = driver.find_element_by_id("loginPassword")
                    psd.clear()
                    psd.send_keys(password)

                    commit = driver.find_element_by_id("loginAction")
                    commit.click()
                    time.sleep(10)

                # cookie=driver.get_cookies()
                # print cookie
                cookie = {}
                if "微博 - 随时随地发现新鲜事" in driver.title:
                    for elem in driver.get_cookies():
                        cookie[elem["name"]] = elem["value"]
                    if len(cookie) > 0:
                        item = {'account': account,
                                'password': password, 'cookie': cookie}
                        db.Cookies.insert_one(item)
                        cookies.append(cookie)
                        print "*******************************"
                        print "Get Cookie Successful: %s!!!!!!" % account
                        print "*******************************"
                        continue
                print "*******************************"
                print "Get Cookie Failed: %s!" % account
                print "*******************************"

            except Exception, e:
                print "*******************************"
                print "%s Failure!!!!!" % account
                print e
                print "*******************************"

            finally:
                try:
                    driver.quit()
                except Exception, e:
                    pass


    else:
        db_cookies = db.Cookies.find()
        for cookie in db_cookies:
            cookies.append(cookie['cookie'])
            print "*******************************"
            print "Get Cookie from db Successful: %s!!!!!!" % cookie['account']
            print "*******************************"
    return cookies


cookies = getCookies(myWeiBo)
# cookies = {}
print "Get Cookies Finish!( Num:%d)\n" % len(cookies)
