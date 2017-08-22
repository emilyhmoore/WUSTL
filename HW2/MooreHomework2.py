from bs4 import BeautifulSoup
from urllib import urlopen
import re, os, csv, itertools
from nltk import word_tokenize
from nltk import word_tokenize
from nltk import bigrams
from nltk import trigrams
from nltk import ngrams
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

##loading stemming and stop words
pt = PorterStemmer()
stop_words=stopwords.words('english')
AdditionalStop=["shelby","sessions","richard","jeff","email","press","room","member","senate"]
stop_words+=AdditionalStop
stop_wordsStem=map(pt.stem, stop_words)

##load up the statements
os.chdir("/Users/emilymoore/WUSTL/HW2/SessionsShelby")

SessionsStatement = "/Users/emilymoore/WUSTL/HW2/SessionsShelby/Sessions"
SessionsStatementList = os.listdir(SessionsStatement)
ShelbyStatement = "/Users/emilymoore/WUSTL/HW2/SessionsShelby/Shelby"
ShelbyStatementList = os.listdir(ShelbyStatement)

StatementList=SessionsStatementList+ShelbyStatementList


##Create Dictionary with all of the information.
StatementDictionary={}
for index in range(len(StatementList)):
	Author=re.findall("(?<=[0-9]{4})[A-Za-z]*(?=[0-9])",StatementList[index])[0]
	StatementDictionary[StatementList[index]]={
	'StatementAuthor': Author,
	'StatementMonth':StatementList[index][2:5], 
	'StatementDay':StatementList[index][0:2],
	'StatementYear':StatementList[index][5:9],
	'StatementText':(open("/Users/emilymoore/WUSTL/HW2/SessionsShelby/" +Author+ "/" +StatementList[index]).read())
	}

unigrams={}
trigram_count={}
for release in StatementDictionary:
	statement=StatementDictionary[release]['StatementText']
	text1 = statement.lower()
	text2 = re.sub('\W', ' ', text1)
	text3 = word_tokenize(text2)
	text4 = map(pt.stem, text3)
	text5 = [x for x in text4 if x not in stop_wordsStem]
	StatementDictionary[release]["numUnigrams"] = len(text5)
	StatementDictionary[release]["Unigrams"]={}
	##I realize this is similar to answer key. I didn't really come up with a better way of doing it. 
	##I did come up with some worse ways :)
	for unigram in set(text5):
		count = text5.count(unigram)
		StatementDictionary[release]["Unigrams"][unigram] = count
		if unigram in unigrams:
			unigrams[unigram] += count
		else:
			unigrams[unigram] = count
	text5_tri = list(trigrams(text5))
	StatementDictionary[release]["numTrigrams"] = len(text5_tri)
	StatementDictionary[release]["Trigrams"] = {}
	for trigram in set(text5_tri):
		count = text5_tri.count(trigram)
		StatementDictionary[release]["Trigrams"][trigram] = count
		if trigram in trigram_count:
			trigram_count[release] += count
		else:
			trigram_count[release] = count 



##index will be the document number
##k will be the author
#press = {}
#used = []
#DataDict={}
#for k in range(len(authors)):
	##used later for the counting.
#	for index in range(len(authorlists[k])):
		##load, convert to lower case, stem, remove stopwords, etc.
#		statement=authorlists[k][authors[k]+'StatementText']
		#open("/Users/emilymoore/WUSTL/HW2/SessionsShelby/" + authors[k] + "/" +authorlists[k][index]).read()
#		text1 = statement.lower()
#		text2=re.sub('\W', ' ', text1)
#		text3 = word_tokenize(text2)
#		text4 = map(pt.stem, text3)
#		text5 = [x for x in text4 if x not in stop_wordsStem]
#		text5_tri = trigrams(text5)
		##need to make this work across texts in each senator's corpus.
#		for word in text5:
#			if word in press:
#				press[word] += 1
#			if word not in press and word not in used:
#				press[word] = 1
#				used.append(word)
#		DataUnigram.update({"Author":author[k]},press)
				
		#with open(authors[k]+"Unigrams.csv", "wb") as f:
			#w = csv.DictWriter(f, fields)
			#w.writeheader()
			#for key,val in sorted(press.items()):
				#row = {'Statement': key}
				#row.update(val)
				#w.writerow(row)

		
			
#press_count = press.values()			
#press_keys = press.keys()


















