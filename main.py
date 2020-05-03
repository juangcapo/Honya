import PyPDF2
import requests
import threading
import pprint
import re
from lxml import html

mainPageLink = 'https://link.springer.com'


PDFFile = open("Springer Ebooks.pdf",'rb')

PDF = PyPDF2.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
ank = '/A'

linkList=[]

for page in range(pages):
    #print("Current Page: {}".format(page))
    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()
    if key in pageObject.keys():
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[ank].keys():
                #print(u[ank][uri])
                linkList.append(u[ank][uri])


def addDownloadItem(downloadLink):

	req=requests.get(downloadLink, stream=True)
	#pprint(f"Headers: {req.headers}")


	list_fname = tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[1]/div/div/div[1]/div[2]/h1/text()')


	print(list_fname)
	fname = ''.join(list_fname) + '.pdf'
	with open(fname,"wb") as fileobj:
		for chunk in req.iter_content(chunk_size=1024):
			if chunk:
				fileobj.write(chunk)




for i in linkList:
	r = requests.get(i)
	tree = html.fromstring(r.content)
	#print(tree)

	if tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a/@href')!=[]:
		link = tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a/@href')
		#print(link)

	elif tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a/@href')!=[]:
		link = tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a/@href')
		#print(link)

	elif tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a/@href')!=[]:
		link = tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a/@href')
		#print(link)


	else:	
		link = tree.xpath('//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a/@href')
		#print(link)



	downloadLink = mainPageLink+''.join(link)
	print(downloadLink)


	downloadThread=threading.Thread(target=lambda:addDownloadItem(downloadLink))
	downloadThread.start()



print("End")
