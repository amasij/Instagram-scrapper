import time,re,random,sys,math
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import pymysql

pages=['maxi_jonez','phoneshopng','shedrackk','wears_boss','theshoeshopnig','dennisss._','the_kicksman_','thewavenigeria','phonesvendor','canoonstore','gadgetfreakzng','techsourcesng']

def cleanCaption(string):
	newstring=''
	for char in string:
		if char.isalpha():
			newstring+=char
		elif char.isdigit():
			newstring+=char
		else:
			newstring+=' '
	return newstring

conn = pymysql.connect(host='localhost',user='root', passwd='',db='mytable',cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

driver = webdriver.Chrome()
for username in pages:

	try:
		driver.get('https://www.instagram.com/'+username+'/')

		numofpost=driver.execute_script("return document.getElementsByClassName('g47SY')[0].innerHTML;")
		numofpost=int(numofpost.replace(",",""))
		numofscroll=math.floor(numofpost/5)
		LINKS=[]

		for i in range(numofscroll):
			driver.execute_script("return window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			html=driver.execute_script("return document.getElementsByClassName('FyNDV')[0].innerHTML;")
			bsObj=BeautifulSoup(html,"html.parser")
			all_links=bsObj.findAll('a', attrs={'href': re.compile("^/p")});

			for link in all_links:
				if link['href'] in LINKS:
					pass
				else:
					LINKS.append(link['href'])
			time.sleep(1)


		f = open('C:/wamp64/www/ig/logs/'+username+".txt", "a")
		for link in LINKS:
			f.write(link+"\n") 
		f.close()
	except:
		pass


	for link in LINKS:
		try:
			driver.get('https://www.instagram.com/'+link)
			time.sleep(2)

			url=driver.execute_script("return document.getElementsByClassName('FFVAD')[0].srcset").split(',')
			[-1].replace("1080w","").strip()

			imagename='pics/'+str(random.randint(1,1000000))+str(int(round(time.time() * 1000)))+'.jpg'
			imageloc='C:/wamp64/www/ig/'+imagename

			urllib.request.urlretrieve(url,imageloc)

			caption=driver.execute_script("return document.getElementsByClassName('C4VMK')[0].childNodes[1].innerHTML")
			caption=cleanCaption(caption)

			query="INSERT INTO ig VALUES(NULL,'"+username+"','"+imagename+"','"+caption+"')"
			cur.execute(query)
		except:
			pass
driver.close()
sys.exit()
	

	