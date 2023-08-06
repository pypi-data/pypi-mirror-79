'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi


class HifiveTrafficSheetMusicRequest(RestApi):
    def __init__(self, domain='hifive-gateway-test.hifiveai.com', port=80):
        RestApi.__init__(self, domain, port)
        self.clientId = None
        self.sheetId = None
        self.language = None
        self.Page = None
        self.PageSize = None

    def getapiname(self):
        return 'TrafficSheetMusic'
