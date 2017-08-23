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
##did this so as not to confuse with the function
trigram_count={}
for release in StatementDictionary:
	##work on the basic preprocessing
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
			trigram_count[trigram] += count
		else:
			trigram_count[trigram] = count 

##found this on stack exchange and is also in answer key			
topUnigrams = sorted(unigrams, key=unigrams.get, reverse=True)[:1000]
topTrigrams = sorted(trigram_count, key=trigram_count.get, reverse=True)[:500]

##from the answer key
def BindTuples(tuples):
    return ".".join(tuples)

stringTrigrams = [BindTuples(tup) for tup in topTrigrams]


##I decided to do this differently than what's in the answer key. 
#I like the way it writes and I like including the file name and word
##count in the file.
UnigramDictionary={}
##Write the unigrams to a new dictionary
for release in StatementDictionary:
	UnigramDictionary[release]={'Author':StatementDictionary[release]["StatementAuthor"],'WordCount':StatementDictionary[release]["numUnigrams"]}
	##writes a key for each topUnigram
	for unigram in topUnigrams:
		UnigramDictionary[release][unigram]=0
	##checks to see if each unigram in document is in top and updates if it is.
	for unigram in StatementDictionary[release]["Unigrams"]:
		if unigram in topUnigrams:
			UnigramDictionary[release][unigram]=StatementDictionary[release]["Unigrams"][unigram]

##write the file
fields=["FileName", "Author", "WordCount"]+topUnigrams
with open("Unigrams.csv", "wb") as f:
	w = csv.DictWriter(f, fields)
	w.writeheader()
	for key,val in sorted(UnigramDictionary.items()):
		row = {'FileName': key}
		row.update(val)
		w.writerow(row)
		
##same thing for trigrams
TrigramDictionary={}
##Write the unigrams to a new dictionary
for release in StatementDictionary:
	TrigramDictionary[release]={'Author':StatementDictionary[release]["StatementAuthor"],'WordCount':StatementDictionary[release]["numTrigrams"]}
	for trigram in stringTrigrams:
		TrigramDictionary[release][trigram]=0
	for trigram in StatementDictionary[release]["Trigrams"]:
		if BindTuples(trigram) in stringTrigrams:
			TrigramDictionary[release][BindTuples(trigram)]=StatementDictionary[release]["Trigrams"][trigram]


fields=["FileName", "Author", "WordCount"]+stringTrigrams
with open("Trigrams.csv", "wb") as f:
	w = csv.DictWriter(f, fields)
	w.writeheader()
	for key,val in sorted(TrigramDictionary.items()):
		row = {'FileName': key}
		row.update(val)
		w.writerow(row)


















