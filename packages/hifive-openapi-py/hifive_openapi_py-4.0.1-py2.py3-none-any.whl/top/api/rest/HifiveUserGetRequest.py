'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi


class HifiveUserGetRequest(RestApi):
    def __init__(self, domain='hifive-gateway-test.hifiveai.com', port=80,method="POST"):
        RestApi.__init__(self, domain, port,method)
        self.clientId = None
        self.nickname = None
        self.gender = None
        self.birthday = None
        self.location = None
        self.education = None
        self.profession = None
        self.isOrganization = None
        self.favoriteSinger = None
        self.favoriteGenre = None
        self.country = None
        self.province = None
        self.reserve = None


    def getapiname(self):
        return 'BaseLogin'
