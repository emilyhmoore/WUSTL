from bs4 import BeautifulSoup
from urllib import urlopen
import re, os, csv, itertools
from nltk import word_tokenize

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



