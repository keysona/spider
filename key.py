import MySQLdb as db
from bs4 import BeautifulSoup
import requests as req
import re
import cv2
from StringIO import StringIO
from color.colordescriptor import ColorDescriptor
from PIL import Image
import numpy as np
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.    0) Gecko/20100101 Firefox/40.0'}
cookies = dict(is_click='1')

url = 'http://www.topit.me/album/2026272?p='
page = 80
conn = db.connect(host='localhost',user='root',passwd='123',db='test2')
cur = conn.cursor()
cd = ColorDescriptor((8, 12, 3))
for i in range(42):
    current_url = url+str(i+1)
    print 'page:',i
    try:
        response = req.get(current_url,headers=headers,cookies=cookies)
    except Exception,e:
        print e,'12'
	continue
    soup = BeautifulSoup(response.text)
    atags = soup.find_all('a',href=re.compile('item'))
    for temp in set(atags):
        a = temp.get('href')
	print a
	try:
            response = req.get(a,headers=headers,cookies=cookies)
	    soup = BeautifulSoup(response.text)
        except Exception,e:
	    print e,'13'
	    continue
	try:
	    img_url = soup.find_all('a',rel=re.compile('light'))[0].get('href')
        except IndexError,e:
	    print e,'list'
	    continue
	try:
            response = req.get(img_url,headers=headers,cookies=cookies)
	except Exception,e:
	    print e,'14'
	    continue
	image = Image.open(StringIO(response.content))
	imgArr = np.asarray(image)
	try:
	    feature = cd.describe(imgArr)
	except Exception,e:
	    print e
	    continue
	temp = ' '.join((str(i) for i in feature))	
        if  not cur.execute('select url from image where url="%s"'%img_url):
	    cur.execute("insert into image(url,hist) value('%s','%s')"%(img_url,temp))
	    conn.commit()
	
