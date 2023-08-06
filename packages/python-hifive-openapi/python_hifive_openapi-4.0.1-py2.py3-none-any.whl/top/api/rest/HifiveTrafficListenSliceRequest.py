'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi


class HifiveTrafficListenSliceRequest(RestApi):
    def __init__(self, domain='hifive-gateway-test.hifiveai.com', port=80):
        RestApi.__init__(self, domain, port)
        self.clientId = None
        self.musicId = None
        self.audioFormat = None
        self.audioRate = None
        self.isMixed = None
        self.auditionBegin = None
        self.auditionEnd = None

    def getapiname(self):
        return 'TrafficListenSlice'
