# -*- coding: utf-8 -*-
import scrapy

from scrapy import Item, Field


class InformationItem(Item):
    _id = Field()  # 用户ID
    NickName = Field()  # 昵称
    Signature = Field()  # 个性签名
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    User_Url = Field() #用户的微博url
    Used = Field()
    Avatar = Field() #用户的头像url
    LocalAvatar = Field() #头像的本地url
    Cover = Field() #用户的背景
    LocalCover = Field() #用户的本地cover

class InfoDetailsItem(Item):
    _id = Field()  # detail_ID
    NickName = Field()  # 昵称
    WeiboTag = Field()  # 微博标签
    Gender = Field()  # 性别
    Place = Field()  # 住址
    Intro = Field()  # 简介
    School = Field()  # 学校
    Rank = Field()  # 等级
    RegTime = Field()  # 注册时间
    ID = Field() #用户ID


class TweetsItem(Item):
    _id = Field()  # 微博ID
    ID = Field()  # 用户ID
    Content = Field()  # 微博内容
    PubTime = Field()  # 发表时间
    Like = Field()  # 点赞数
    Comment = Field()  # 评论数
    Transfer = Field()  # 转载数
    TweetsText = Field()  # 微博的具体文字
    Imgs = Field()  # 微博中图片的链接
    SmallImgs = Field() #微博图片缩略图
    LocalImgs = Field() #微博图片的本地存储目录
    Owner = Field() #发微博的主人
    Used = Field() #这条微博是否发过

class FollowsItem(Item):
    _id = Field()  # 好友ID
    ID = Field()  # 用户ID
    NickName = Field()  # 昵称
    Signature = Field()  # 个性签名
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    profile_url = Field()  # 主页链接


class FansItem(Item):
    _id = Field()  # 粉丝ID
    ID = Field()  # 用户ID
    NickName = Field()  # 昵称
    Signature = Field()  # 个性签名
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    profile_url = Field()  # 主页链接


class AimUserItem(Item):
    ID = Field()  # 微博ID
    NickName = Field()  # 昵称
    Signature = Field()  # 个人简介
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 她关注的人数
    Num_Fans = Field()  # 粉丝数
    profile_url = Field()  # 主页链接