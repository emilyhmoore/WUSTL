setwd("~/WUSTL")


##LOAD IN DEBATE DATA
DebateStatementData=read.csv("DebateStatementData.csv", stringsAsFactors=FALSE)
DebateStatementData=DebateStatementData[order(DebateStatementData$StatementNumber),]

head(DebateStatementData)

##SIMPLE PLOT OF ALL STEMMERS. SEEM TO BE SIMILAR
plot(x=DebateStatementData$StatementNumber, y=DebateStatementData$POSSTStem, type="line", col="blue")
lines(x=DebateStatementData$StatementNumber, y=DebateStatementData$POSSBStem, col="red")
lines(x=DebateStatementData$StatementNumber, y=DebateStatementData$POSPTStem, col="green")

##proportion of positive words in each statement overall
plot(x=DebateStatementData$StatementNumber, y=DebateStatementData$POSSTStem/DebateStatementData$NonStopLength, type="line", col="blue")

##proportion of negative words in each statement
plot(x=DebateStatementData$StatementNumber, y=DebateStatementData$NEGSTStem/DebateStatementData$NonStopLength, type="line", col="blue")

##Create datasets that are speaker specific
OBAMA=DebateStatementData[DebateStatementData$Speaker=="OBAMA:",2:12]
head(OBAMA)
LEHRER=DebateStatementData[DebateStatementData$Speaker=="LEHRER:",2:12]
ROMNEY=DebateStatementData[DebateStatementData$Speaker=="ROMNEY:",2:12]
head(ROMNEY)

##Plot Romney Over Time
plot(ROMNEY$POSPTStem, type="l")
plot(ROMNEY$NEGPTStem, type="l")
###Romney more negative at the beginning, relatively positive through middle, slight re-spike toward end.
plot(ROMNEY$POSPTStem/ROMNEY$NonStopLength, type="l")
plot(ROMNEY$NEGPTStem/ROMNEY$NonStopLength, type="l")

##Obama proportion varied but appears that he was more positive in the middle
plot(OBAMA$POSPTStem/OBAMA$NonStopLength, type="l")
##As a proportion of his overall words, Obama was not very negative. It may be something about him
##but it could also just be that he is the incumbent and so he is less likely to talk negatively about the
##state of society under his governance.
plot(OBAMA$NEGPTStem/OBAMA$NonStopLength, type="l")

##Total words spoken by each. Lehrer much less unsurprisingly
sum(OBAMA$NonStopLength)
sum(ROMNEY$NonStopLength)
sum(LEHRER$NonStopLength)

##Number of Positive Words per statement over time
plot(OBAMA$POSPTStem, type="l",col="blue")
lines(LEHRER$POSPTStem, type="l",col="green")
lines(ROMNEY$POSPTStem, type="l",col="red")

##Number of negative words per statement over time
plot(ROMNEY$NEGPTStem, type="l",col="red")
lines(LEHRER$NEGPTStem, type="l",col="green")
lines(OBAMA$NEGPTStem, type="l",col="blue")

##Proportion of Positive Words per statement over time
plot(OBAMA$POSPTStem/OBAMA$NonStopLength, type="l",col="blue")
lines(LEHRER$POSPTStem/LEHRER$NonStopLength, type="l",col="green")
lines(ROMNEY$POSPTStem/ROMNEY$NonStopLength, type="l",col="red")

##Proportion of negative words per statement over time
plot(OBAMA$NEGPTStem/OBAMA$NonStopLength, type="l",col="blue")
lines(LEHRER$NEGPTStem/LEHRER$NonStopLength, type="l",col="green")
lines(ROMNEY$NEGPTStem/ROMNEY$NonStopLength, type="l",col="red")

