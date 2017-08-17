#WUSTL Text as Data Course Homework

from bs4 import BeautifulSoup
from urllib import urlopen
import re, os, csv, itertools
from nltk import word_tokenize

url  = urlopen('file:///Users/emilymoore/WUSTL/Debate1.html').read()

soup = BeautifulSoup(url, "html.parser")

	##Identify Statements
text=soup.find_all('p')

	#This is the text of the actual debate. #Need to devise a rule here
text2=text[6:476] 

	##There is probably a better/more pythonic way to do this but the goal was to get a list of strings without the tags. 
	#I had tried this without the loop before and it did weird things with the unicode, so I left it for now.
text3=[]
for i in range(len(text2)):
	text3.append(text2[i].contents[0])

text4 = ' '.join(text3) ##joining into one

text5 =  re.split(" (?=[A-Z+]*:)",text4) #splitting based on a regular expression for speaker. 

	##This code finds all of the capital words in parentheses and replaces them with nothing
text6 = [re.sub("\([A-Z+]*\)", '',word) for word in text5]


pos_words = urlopen('http://www.unc.edu/~ncaren/haphazard/positive.txt').read().split('\n')
neg_words = urlopen('http://www.unc.edu/~ncaren/haphazard/negative.txt').read().split('\n')
from nltk.corpus import stopwords
stop_words=stopwords.words('english')

##convert to lower case
text7 = [word.lower() for word in text6]

##remove white space characters
text8 = [re.sub("\W", ' ',word) for word in text7]

text9 = [word_tokenize(string) for string in text8]

#not sure how to fully do this with list comprehension. Example works fine if everything is in one big bubble
#like in example, but not when I'm going over lists of strings
text10=[]
for string in text9:
	text10.append([word for word in string if word not in stop_words])


##this removes the speaker name so it doesn't show up in word counts
text11=[list[1:] for list in text10]


##NOTE: DESPITE THE QUESTION WORDING, I CHOSE TO SEARCH FOR THE WORDS DIRECTLY.
##IN THE NEXT PART, I STEM THE WORDS AND THEN USE THE CORRESPONDING STEMMED DICTIONARY
textPOS=[]
for string in text11:
	textPOS.append([word for word in string if word in pos_words])


textNEG=[]
for string in text11:
	textNEG.append([word for word in string if word in neg_words])


	###################
    #####STEMMERS######
    ###################

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
from nltk.stem import PorterStemmer
pt = PorterStemmer()
from nltk.stem.snowball import EnglishStemmer
sb = EnglishStemmer()

PTStemPOSDict=map(pt.stem, pos_words)

PTStemNegDict=map(pt.stem, neg_words)

STStemPOSDict=map(st.stem, pos_words)

STStemNegDict=map(st.stem, neg_words)

SBStemPOSDict=map(sb.stem, pos_words)

SBStemNegDict=map(sb.stem, neg_words)


##Stem the debate
textPTSTEM=[]
for string in text11:
	textPTSTEM.append(map(pt.stem, string))



textSTSTEM=[]
for string in text11:
	textSTSTEM.append(map(st.stem, string))



textSBSTEM=[]
for string in text11:
	textSBSTEM.append(map(sb.stem, string))



##calculate PT stemmed positive and negative
textPTPOS=[]
for string in textPTSTEM:
	textPTPOS.append([word for word in string if word in PTStemPOSDict])



textPTNEG=[]
for string in textPTSTEM:
	textPTNEG.append([word for word in string if word in PTStemNegDict])
	

	
##calculate ST stemmed positive and negative	
textSTPOS=[]
for string in textSTSTEM:
	textSTPOS.append([word for word in string if word in STStemPOSDict])



textSTNEG=[]
for string in textSTSTEM:
	textSTNEG.append([word for word in string if word in STStemNegDict])



##calculate SB stemmed positive and negative
textSBPOS=[]
for string in textSBSTEM:
	textSBPOS.append([word for word in string if word in SBStemPOSDict])



textSBNEG=[]
for string in textSBSTEM:
	textSBNEG.append([word for word in string if word in SBStemNegDict])
	


##Calculate the data entries
StatementNumber=range(len(text6))
	#Identify the Speakers
Speakers = [re.findall("([A-Z+]*:)",word)[0] for word in text6]

NonStopLength=[len(list) for list in text11]

POSUnStemLength=[len(list) for list in textPOS]

NEGUnStemLength=[len(list) for list in textNEG]

POSPTStem=[len(list) for list in textPTPOS]

NEGPTStem=[len(list) for list in textPTNEG]

POSSTStem=[len(list) for list in textSTPOS]

NEGSTStem=[len(list) for list in textSTNEG]

POSSBStem=[len(list) for list in textSBPOS]

NEGSBStem=[len(list) for list in textSBNEG]

##write data to dictionary
Datadict={}
for i in range(len(text10)):
	Datadict[text6[i]] = {'StatementNumber':StatementNumber[i],'Speaker':Speakers[i], 'NonStopLength': NonStopLength[i], 'POSUnStemLength': POSUnStemLength[i],'NEGUnStemLength':NEGUnStemLength[i],'POSPTStem':POSPTStem[i],'NEGPTStem':NEGPTStem[i],'POSSTStem':POSSTStem[i],'NEGSTStem':NEGSTStem[i],'POSSBStem':POSSBStem[i],'NEGSBStem':NEGSBStem[i]}



fields=['Statement','StatementNumber','Speaker','NonStopLength','POSUnStemLength', 'NEGUnStemLength','POSPTStem','NEGPTStem','POSSTStem','NEGSTStem','POSSBStem','NEGSBStem']

with open("DebateStatementData.csv", "wb") as f:
	w = csv.DictWriter(f, fields)
	w.writeheader()
	for key,val in sorted(Datadict.items()):
		row = {'Statement': key}
		row.update(val)
		w.writerow(row)





