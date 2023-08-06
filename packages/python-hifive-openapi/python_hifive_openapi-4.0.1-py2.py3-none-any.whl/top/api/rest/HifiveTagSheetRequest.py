'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi
class HifiveTagSheetRequest(RestApi):
	def __init__(self,domain='hifive-gateway-test.hifiveai.com',port=80):
		RestApi.__init__(self,domain, port)
		self.clientId = None
		self.tagId = None
		self.type = None
		self.recoNum = None
		self.language = None

	def getapiname(self):
		return 'TagSheet'
