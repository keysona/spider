import threading
import MySQLdb as db
import time

class DBOperation(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
	self.conn = None
	self.cur = None
    def openDB(self):
        self.conn = db.connect(host='localhost',user='root',passwd='123',db='test2')
	self.cur = self.conn.cursor()
    def closeDB(self):
        self.cur.close()
	self.conn.close()
    
    def run(self):
	self.openDB()
        while True:
	    print 'Queue size:',self.queue.qsize()
	    time.sleep(5)
	    if self.queue.qsize() >= 50:
		for i in range(50):
		     temp = self.queue.get()
		     print self.queue.qsize()
		     try:
			self.cur.execute("insert into image(url,hist) value('%s','%s')"%(temp[0],temp[1]))
			self.conn.commit()
			print 'success into database'
			print 'url :',temp[0]
		     except Exception,e:
		         print e
			 return
  		         
        
