# -*- coding: utf-8 -*-
import json
import scrapy
import requests
from scrapy.http import FormRequest
from together.items import UserItem


class YiQiSpider(scrapy.Spider):
    name = 'yiqi'
    allowed_domains = ['wondertech.com.cn']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.getUserById = 'http://api.wondertech.com.cn/user/v2/users/getById'
        # self.likeUser = 'http://api.wondertech.com.cn/fmvoice/v1/voice/vlike'
        self.token = 'eyJhbGciOiJIUzUxMiJ9.eyJwaG9uZSI6IjEzNzA5NjQxNzEzIiwiZXhw' \
                     'IjoxNTQ4OTAxMDM4LCJ1c2VySWQiOjU4NjQzfQ.-N6EqLyAU_NvXqcNTT' \
                     'awkpfY_6lidC_XjvYJAnHr-AfBTCz2kT1-Sht_sTDZZOB_lDX6bruHTTJ8SzfZyX1JkA'
        self.formData = {'token': self.token}

    def start_requests(self):
        for user_id in range(307478, 320000):
            self.formData['id'] = str(user_id)
            yield FormRequest(self.getUserById, formdata=self.formData,
                              callback=self.parse, meta={'uid': user_id})

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())

        code, success, uid = resp.get('code'), resp.get('success'), response.meta['uid']
        self.logger.info('uid {} , resp code {} and success {}'.format(uid, code, success))
        if code == 1 or success:
            data = resp.get('data')

            item = UserItem()
            item['uid'] = uid
            item['sex'] = data.get('sex')
            item['age'] = data.get('age')
            item['phone'] = data.get('phone')
            item['nickname'] = data.get('nickName')
            item['birthday'] = data.get('birthday')
            head_pic = data.get('headPic')
            item['head_pic'] = head_pic
            if head_pic:
                item['source'] = 'ios' if 'ios' in head_pic else 'android'
            item['voice'] = data.get('voice')
            item['available_voice'] = data.get('availableVoice')
            item['user_last_fm_voice'] = data.get('userLastFmVoice')
            item['region_code'] = data.get('regionCode')
            info = data.get('regionInformation')
            if info:
                text = info.get('regionText')
                if text:
                    item['region_information'] = ''.join(text)
            item['last_app_version'] = data.get('lastAppVersion')
            item['create_time'] = data.get('createTime')
            item['netease_accid'] = data.get('neteaseAccid')
            item['netease_token'] = data.get('neteaseToken')
            item['netease_status'] = data.get('neteaseStatus')
            item['user_status'] = data.get('userStatus')
            yield item
