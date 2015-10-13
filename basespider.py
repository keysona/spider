#! -*- coding:utf-8 -*-
import threading
import requests as req

class BaseSpider(threading.Thread):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
	cookies = dict(is_click='1')
	timeout_urls = []
       
        def __init__(self):
	    threading.Thread.__init__(self)
    
	def getResponse(self,url):
		try:
			return req.get(url,cookies = BaseSpider.cookies,timeout=3,headers=BaseSpider.headers)
		except Exception as e:
			BaseSpider.timeout_urls.append(url)
			with open('./errorurl/%s.txt'%self.number,'a+') as f:
  				f.write('%s\n'%url)



	
