'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi


HFBehaviorRequest(RestApi):
    def __init__(self, domain='hifive-gateway-test.hifiveai.com', port=80,method="POST"):
        RestApi.__init__(self, domain, port,method)
        self.clientId = None
        self.TargetId = None
        self.Action = None




    def getapiname(self):
        return 'BaseReport'
