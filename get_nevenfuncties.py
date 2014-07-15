import os
import sys
from urllib2 import urlopen
import lxml.html
import itertools

# TiU parser

d = open(sys.argv[1])
details = d.readlines()
# csv with names and URL's or ID's

endfile = open("hoogleraren-scraped.csv","w")

testurl = urlopen("https://www.tilburguniversity.edu/nl/webwijs/show/?uid=l.a.g.oerlemans").read()
geenurl = urlopen("https://www.tilburguniversity.edu/nl/webwijs/show/?uid=m.vanreisen").read()
# testurl for a profilepage

def get_da_nevenfuncties(url):
# parse nevenfuncties (side jobs) - name of function

	doc = lxml.html.document_fromstring(url)

	functie = doc.xpath('//div[@id="content_activiteiten"]/div/descendant::*/text()')

	if functie == []:
	# if no sidejob is found, it gets a value "1"
		functie = "1"
		return functie
	else:

	# get all the nodes, with text and empty ones
		functie = ['0' if x==None else x for x in functie]
		# replace NoneType with '0'
		functie = [f.replace('\n', '|') for f in functie]
		functie = [f.replace(',', ';') for f in functie]

	        return functie

def get_fac(url):

	doc = lxml.html.document_fromstring(url)
	faculty = doc.xpath('//div[@id="expertdetails"]/div/div[1]/descendant::*/text()')
	faculty = [f.replace(',', ';') for f in faculty]
	return faculty

for row in details:
	# details is a csv file with the name, id and url to the personal page of the prof. An example page can be found in variables "testurl" en "geenurl"
	prof = row.split(",")
	prof_id = prof[0]
	prof_url = prof[5].rstrip()
	prof_name = prof[1]+','+prof[2]+','+prof[3]+','+prof[4]
	
	#print prof_name+';'+prof_fac+';'+prof_url

	url_string = str(prof_url)
	naostrourl = urlopen(url_string).read()

	nevenfuncties = get_da_nevenfuncties(naostrourl)
	prof_fac = get_fac(naostrourl)[1]

	for funct in nevenfuncties:
		if funct == ' ':
			continue
		else:
			endfile.write(prof_id+','+prof_name+','+prof_fac+','+funct.encode('utf-8')+','+prof_url+'\n')

endfile.close()
