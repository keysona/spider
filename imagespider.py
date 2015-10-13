import threading
import cv2
from basespider import BaseSpider 
from PIL import Image
import MySQLdb as db
from StringIO import StringIO
from color.colordescriptor import ColorDescriptor
import numpy as np
class ImageSpider(BaseSpider):
    def __init__(self,img_url,number,queue):
        BaseSpider.__init__(self)
	self.image_url = img_url
	self.number = str(number)
	self.queue = queue
	self.cd = ColorDescriptor((8, 12, 3))
    def run(self):
        response = self.getResponse(self.image_url)
	if response == None:
	    return
	try:
	    image = Image.open(StringIO(response.content))
	    imgArr = np.asarray(image)
	    feature = self.cd.describe(imgArr)
            temp = ' '.join((str(i) for i in feature))	
   	    self.queue.put([self.image_url,temp])
        except Exception,e:
	    print e
