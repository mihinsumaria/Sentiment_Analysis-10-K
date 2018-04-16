import os, bs4
import requests
from bs4 import BeautifulSoup
from operator import methodcaller

class SECCrawler(object):

	def __init__(self):
		os.chdir(".")
		print "Download directory will be created here: ", os.getcwd()

	def make_directory(self, company_code, cik, priorto, filing_type):
		current_directory = os.getcwd()
		path = os.path.join(current_directory, company_code)

		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except OSError as exception:
				if exception.errno != errno.EEXIST:
					raise

	def save_in_directory(self, company_code, cik, priorto, doc_list, 
		doc_name_list, filing_type):
		for j in range(len(doc_list)):
			base_url = doc_list[j]
			r = requests.get(base_url)
			data = r.text
			current_directory = os.getcwd()
			path = os.path.join(current_directory, company_code, 
				doc_name_list[j])
			with open(path, "ab") as f:
				f.write(data.encode('ascii', 'ignore'))

	def filing_10K(self, company_code, cik, priorto, count):
		self.make_directory(company_code, cik, priorto, '10-K')
		base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+\
		"&type=10-K&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
		print ("started 10-K " + str(company_code))

		r = requests.get(base_url)
		data = r.text

		# get doc list data
		doc_list, doc_name_list = self.create_document_list(data)

		try:
			self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '10-K')
		except Exception as e:
			print (str(e))

		print ("Successfully downloaded all the files")


	def create_document_list(self, data):
		# parse fetched data using beatifulsoup
		soup = BeautifulSoup(data, "html.parser")
		# store the link in the list
		link_list = list()

		# If the link is .htm convert it to .html
		for link in soup.find_all('filinghref'):
			url = link.string
			if link.string.split(".")[len(link.string.split("."))-1] == "htm":
				url += "l"
			link_list.append(url)
		link_list_final = link_list

		print ("Number of files to download {0}".format(len(link_list_final)))
		print ("Starting download....")

		# List of url to the text documents
		doc_list = list()
		# List of document names
		doc_name_list = list()

		# Get all the doc
		for k in range(len(link_list_final)):
			required_url = link_list_final[k].replace('-index.html', '')
			txtdoc = required_url + ".txt"
			docname = txtdoc.split("/")[-1]
			doc_list.append(txtdoc)
			doc_name_list.append(docname)
		return doc_list, doc_name_list

def get_companies():
	with open('companylist.txt', 'rb') as file:
		clist = file.read().split('\n')
		clist = map(methodcaller("split"," "), clist)
		return clist

def download_all_10_K():
	clist = get_companies()
	s = SECCrawler()
	priorto = '20180101'
	count = '10'
	for company in clist:
		print "Downloading for", company[0]
		s.filing_10K(company[0], company[1], priorto, count)