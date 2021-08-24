import re
import urllib.request
from urllib import error


class User:
	def __init__(self):
		self.opener=urllib.request.build_opener()
		self.opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
		self.identity=urllib.request.install_opener(self.opener)




class Search(User):
	def __init__(self,query=None,numberOfResults=15):
		User.__init__(self)
		self.numberOfResults=numberOfResults

	def search(self,query):
		self.query=query
		return self.getResults()

	def printProperties(self):
		print(self.identity)



	def generateURL(self,state)->str:
		d={"fine":["-",r"https://wallpaperaccess.com/"],"error":["+",r"https://wallpaperaccess.com/search?q="]}
		return d[state][1]+d[state][0].join(self.query.split())

	def getHTML(self,url):
		return str(urllib.request.urlopen(url).read())[2:-1]

	def getResults(self,state="fine")->list:
		url = self.generateURL(state)
		#error handling
		try:
			html=self.getHTML(url)
		except urllib.error.HTTPError:
			self.getResults("error")
		if state=="error":
			divTerm=r'<div id="collections_segment">[<>"=_:./;!&\s\d\w-]+</div>'
			div=re.findall(divTerm,html)
			self.html=html
			print(html)
			print(div)
			div=div[0]
			print(div)
			pat=r'^href="[/w/d_./-]+"'
			l=re.findall(pat,div)
			for i in l:print("https://wallpaperaccess.com/"+i)
			url="https://wallpaperaccess.com/"+l[0]
			html=self.getHTML(url)


		downloadTerm=r"(/download/"+"-".join(self.query.split())+r"-[0-9]+)"
		linkList=[]
		for i in set(re.findall(downloadTerm,html)):linkList+=["https://wallpaperaccess.com"+str(i)]
		return linkList




if __name__=="__main__":
	browse=Search()
	walls=browse.search(input("enter query:"))

	for i in walls:print(i)
