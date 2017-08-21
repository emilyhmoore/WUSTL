from bs4 import BeautifulSoup
from urllib import urlopen
import re, os, csv, itertools
from nltk import word_tokenize
from nltk import word_tokenize
from nltk import bigrams
from nltk import trigrams
from nltk import ngrams

os.chdir("/Users/emilymoore/WUSTL/HW2/SessionsShelby")

SessionsStatement = "/Users/emilymoore/WUSTL/HW2/SessionsShelby/Sessions"
SessionsStatementList = os.listdir(SessionsStatements)
ShelbyStatement = "/Users/emilymoore/WUSTL/HW2/SessionsShelby/Shelby"
ShelbyStatementList = os.listdir(ShelbyStatements)

##Create the Sessions Dictionary with all of the information.
SessionsDictionary={}
for index in range(len(SessionsStatementList)):
	SessionsDictionary[SessionsStatementList[index]]={
	'SessionsStatementMonth':SessionsStatementList[index][2:5], 
	'SessionsStatementDay':SessionsStatementList[index][0:2],
	'SessionsStatementYear':SessionsStatementList[index][5:9],
	'SessionsStatementText':(open("/Users/emilymoore/WUSTL/HW2/SessionsShelby/Sessions/" +SessionsStatementsList[index]).read())
	}

ShelbyDictionary={}
for index in range(len(ShelbyStatementList)):
	ShelbyDictionary[ShelbyStatementList[index]]={
	'ShelbyStatementMonth':ShelbyStatementList[index][2:5], 
	'ShelbyStatementDay':ShelbyStatementList[index][0:2],
	'ShelbyStatementYear':ShelbyStatementList[index][5:9],
	'ShelbyStatementText':(open("/Users/emilymoore/WUSTL/HW2/ShelbyShelby/Shelby/" +ShelbyStatementsList[index]).read())
	}


##writing some text to do on each press report. Will then iterate

##convert to lower case
statement=SessionsStatementList[item]
text1 = statement.lower()
text2=re.sub('\W', ' ', text1)
text3 = word_tokenize(text2)
from nltk.stem import PorterStemmer
pt = PorterStemmer()


from nltk.corpus import stopwords
stop_words=stopwords.words('english')
AdditionalStop=["shelby","sessions","richard","jeff","email","press","room","member","senate"]
stop_words+=AdditionalStop

stop_wordsStem=map(pt.stem, stop_words)

text4=map(pt.stem, text3)

text5 = [x for x in text4 if x not in stop_wordsStem]


text5_tri = trigrams(text5)

##counting unigrams. Need to make it so this will count up across texts?
press = {}
used = []
for word in text5:
	if word in press:
		press[word] += 1
	if word not in press and word not in used:
		press[word] = 1
		used.append(press)

press_count = press.values()
press_keys = press.keys()


















