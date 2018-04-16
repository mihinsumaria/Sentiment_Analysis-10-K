import os, glob, nltk, bs4
from textblob import TextBlob
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from SECEdgar import get_companies

CURRENT_DIRECTORY = os.getcwd()
print "Current Directory:" ,CURRENT_DIRECTORY

def tag_visible(element):
	"""
	Input: element, bs4.element (object), HTML element received from the BS4 HTML parser

	Output: boolean, True if HTML element is visible, False otherwise
	"""
	if element.parent.name in ['style', 'script', 'head',\
	 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def cleanhtml(path):
	"""
	Input: path, str, Path to the HTML file that needs to be cleaned

	Output: cleanedhtml, str, Text extracted from the given HTML file
	"""
	file = open(path, "rb")
	html = file.read().decode('utf-8')
	
	# BeautifulSoup getting text from the document
	soup = BeautifulSoup(html, 'lxml')
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)
	BScleanedhtml = " ".join(t.strip() for t in visible_texts)

	# Getting NLTK's corpus
	words = set(nltk.corpus.words.words())

	# Tokenizing the string
	tokenized = nltk.wordpunct_tokenize(BScleanedhtml)

	# Getting words from the semi-cleaned html file
	cleanedhtml = " ".join(w.lower() for w in tokenized if w.lower()\
	 in words and w.isalpha() and len(w) > 1)

	file.close()

	return cleanedhtml

def polarity(cleanedhtml):
	"""
	Input: cleanedhtml, str, Text extracted from the given HTML file

	Output: polarity, float, Sentiment polarity of the document
	"""
	return TextBlob(cleanedhtml).polarity

def get_date(path):
	"""
	Input: path, str, Path to the HTML file containing the 10-K report

	Output: date, str, End date of the fiscal year
	"""
	file = open(path, 'rb')
	html = file.read()
	substring = 'CONFORMED PERIOD OF REPORT'
	date_start = html.find(substring) + len(substring) + 2
	date = html[date_start:date_start + 8]
	file.close()
	return datetime.strptime(date, '%Y%m%d').year

def plot_line_chart(company_code, polarities, dates):
	path = os.path.join(CURRENT_DIRECTORY, 'Plots')
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
	sns.set_style("darkgrid")
	figure = plt.figure(1)
	ax = sns.pointplot(x=dates, y=polarities)
	ax.set(xlabel='Year', ylabel='Sentiment Polarity',\
		title=company_code)
	figure.savefig(path + '/' + company_code + '.png')
	plt.close(figure)
	return

def plot_all_polarities():
	print "Fetching companies"
	clist = get_companies()	
	companies = zip(*clist)[0]
	for i, company in enumerate(companies):
		path = os.path.join(CURRENT_DIRECTORY, company)
		os.chdir(path)
		print "Getting the 10-K filings for", company
		_10_K_filings = glob.glob('*.txt')
		if not _10_K_filings:
			print "No 10-K filings"
			continue
		print "Cleaning HTML files"
		cleanedhtml = [cleanhtml(_10_K_filing) for _10_K_filing\
		 in _10_K_filings]
		print "Computing polarity scores"
		polarity_score = [polarity(ch) for ch in cleanedhtml]
		print "Fetching dates"
		date = [get_date(_10_K_filing) for _10_K_filing\
		 in _10_K_filings]
		print "Plotting sentiment polarity scores for", company
		plot_line_chart(company, polarity_score, date)