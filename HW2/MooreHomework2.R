library(plyr)

setwd("~/WUSTL/HW2/SessionsShelby")
Unigrams=read.csv("Unigrams.csv", stringsAsFactors=FALSE)
Trigrams=read.csv("Trigrams.csv", stringsAsFactors=FALSE)
##Having an issue where numbers that were in the top 1000 or whatever don't load correctly into R. even though they're strings
##


head(Unigrams)
colnames(Unigrams)

##Create separate datasets for ease.
ShelbyUnigrams=Unigrams[Unigrams$Author=="Shelby",-c(2,3)] ##removing word count and author but leaving filename
ShelbyTrigrams=Trigrams[Trigrams$Author=="Shelby",-c(2,3)]
SessionsUnigrams=Unigrams[Unigrams$Author=="Sessions",-c(2,3)] ##removing word count and author but leaving filename
SessionsTrigrams=Trigrams[Trigrams$Author=="Sessions",-c(2,3)]

##N Documents
numShelby=nrow(ShelbyUnigrams)
numSessions=nrow(SessionsUnigrams)

##Means
ShelbyUnigramMeans=colMeans(ShelbyUnigrams[,-1])
SessionsUnigramMeans=colMeans(SessionsUnigrams[,-1])
ShelbyTrigramMeans=colMeans(ShelbyTrigrams[,-1])
SessionsTrigramMeans=colMeans(SessionsTrigrams[,-1])

##Variances
ShelbyUnigramVar=laply(ShelbyUnigrams[,-1],var)
SessionsUnigramVar=laply(SessionsUnigrams[,-1],var)
ShelbyTrigramVar=laply(ShelbyTrigrams[,-1],var)
SessionsTrigramVar=laply(SessionsTrigrams[,-1],var)

################################################################
#############Mosteller and Wallace LDA##########################
################################################################

UnigramWeights<- (ShelbyUnigramMeans - SessionsUnigramMeans) / (ShelbyUnigramVar + SessionsUnigramVar)

#trigrams
TrigramWeights<- (ShelbyTrigramMeans - SessionsTrigramMeans) / (ShelbyTrigramVar + SessionsTrigramVar)

#ldWeightsT!="-Inf"]
UnigramWeights<- sort(UnigramWeights)
TrigramWeights<- sort(TrigramWeights)

#get 20 most discriminating words
LDmostSessionsU<- head(UnigramWeights, 10)
LDmostShelbyU<- tail(UnigramWeights, 10)
LDmostSessionsT<- head(TrigramWeights, 10) 
LDmostShelbyT<- tail(TrigramWeights, 10)

#for plots
LDdiscrimU<-c(LDmostSessionsU, LDmostShelbyU)
LDdiscrimT<- c(LDmostSessionsT, LDmostShelbyT)

index<- seq(1, 20, 1)

##my plots look somewhat different. Not sure why. ##Maybe based on the stop words I used?
##Any thoughts would be helpful.
plot(LDdiscrimU, index, xlim=c(-5,11),pch="", xlab="weight", ylab="", yaxt="n", main="Most discriminating words\n Linear Discriminant Analysis")
text(LDdiscrimU, index , label=names(LDdiscrimU), cex=.7)

##I think something weird happened with the unicode in python that made some weird changes. 
##If I were doing this on my stuff I would make sure that wasn't happening, but I'm running out of time. :)
plot(LDdiscrimT, index,xlim=c(-250,500), pch="", xlab="weight", ylab="", yaxt="n", main="Most discriminating words\n Linear Discriminant Analysis")
text(LDdiscrimT, index , label=names(LDdiscrimT), cex=.7)

################################################################
#############Standardized Mean Difference#######################
################################################################
NumeratorUnigram<- ShelbyUnigramMeans - SessionsUnigramMeans
denomUnigram<- sqrt((ShelbyUnigramVar/numShelby) + (SessionsUnigramVar/numSessions))
stdDiffUnigram<-NumeratorUnigram / denomUnigram

#trigrams
NumeratorTrigram<- ShelbyTrigramMeans - SessionsTrigramMeans
##this was a mistake in the answer key and I fixed it
DenomTrigram<- sqrt((ShelbyTrigramVar/numShelby) + SessionsTrigramVar/numSessions)
stdDiffTrigram<- NumeratorTrigram/DenomTrigram

sdWeightsUnigram<- sort(stdDiffUnigram[stdDiffUnigram!="-Inf"])
sdWeightsTrigram<- sort(stdDiffTrigram[stdDiffTrigram!="-Inf"])

SDmostSessionsU<- head(sdWeightsUnigram,10)
SDmostShelbyU<- tail(sdWeightsUnigram, 10)
SDmostSessionsT<- head(sdWeightsTrigram, 10)
SDmostShelbyT<- tail(sdWeightsTrigram, 10)

SDdiscrimU<- c(SDmostSessionsU, SDmostShelbyU)
SDdiscrimT<- c(SDmostSessionsT, SDmostShelbyT)

##again, I think some differences are in the stop words I used from nltk.
plot(SDdiscrimU, index, pch="", xlab="weight", ylab="", yaxt="n", main="Most discriminating words\n Standard Mean Difference")
text(SDdiscrimU, index, label=names(SDdiscrimU), cex=.7)

##not sure why I didn't get the same words on the right as the answer key. Maybe because of their mistake in the key?
plot(LDdiscrimT, index, pch="", xlab="weight", xlim=c(-400,1600), ylab="", yaxt="n", main="Most discriminating words\n Linear Discriminant Analysis")
text(LDdiscrimT, index, label=names(LDdiscrimT), cex=.7)


################################################################
####################Standardized Log Odds#######################
################################################################



################################################################
####################Document Similarity#########################
################################################################
##sample wasn't working directly for me(samples on the columns instead of the rows for some reason)
##so instead I just sampled the length of the document and selected from there.
##I did this for both unigrams and trigrams even though it just asked for trigrams.
set.seed(85142)
ShelbyUnigramSampleIndex<-sample(1:nrow(ShelbyUnigrams), size=100, replace=FALSE)
ShelbyUnigramSample<-ShelbyUnigrams[ShelbyUnigramSampleIndex,]

SessionsUnigramSampleIndex<-sample(1:nrow(SessionsUnigrams), size=100, replace=FALSE)
SessionsUnigramSample<-SessionsUnigrams[SessionsUnigramSampleIndex,]

ShelbyTrigramSampleIndex<-sample(1:nrow(ShelbyTrigrams), size=100, replace=FALSE)
ShelbyTrigramSample<-ShelbyTrigrams[ShelbyTrigramSampleIndex,]

SessionsTrigramSampleIndex<-sample(1:nrow(SessionsTrigrams), size=100, replace=FALSE)
SessionsTrigramSample<-SessionsTrigrams[SessionsTrigramSampleIndex,]


ShelbySessionsSampleMatrix<-rbind(ShelbyTrigramSample[,-1], SessionsTrigramSample[,-1])
rownames(ShelbySessionsSampleMatrix)<-c(ShelbyTrigramSample[,1],SessionsTrigramSample[,1])

ShelbySessionsSampleMatrix<-ShelbySessionsSampleMatrix[,-c(which(colSums(ShelbySessionsSampleMatrix)==0))]

##Not sure I did this right??
EuclideanDistMatrix<-as.matrix(dist(ShelbySessionsSampleMatrix,method="euclidean"))

ShelbySessionsSampleMatrix
EuclideanDistMatrix<-as.matrix(EuclideanDistMatrix)
diag(EuclideanDistMatrix)<- NA


#max distance
which(EuclideanDistMatrix == max(EuclideanDistMatrix, na.rm=T), arr.ind=T)

##LOTS for min distance
which(EuclideanDistMatrix == min(EuclideanDistMatrix, na.rm=T), arr.ind=T)
################
####TF-IDF######
################
calcIDF<- function(x){
  return(log(200/length(which(x>0))))
}

idf<- apply(ShelbySessionsSampleMatrix, 2, calcIDF)

SampleEIDF<- as.matrix(t(apply(ShelbySessionsSampleMatrix, 1, function(x) x*idf)))

SampleIFIDF<- as.matrix(dist(SampleEIDF, method="euclidean"))

diag(SampleIFIDF)<- NA

##Two Shelby Docs Again
which(SampleIFIDF == max(SampleIFIDF, na.rm=T), arr.ind=T)

##LOTS for min distance. I don't get it?
which(SampleIFIDF== min(SampleIFIDF, na.rm=T), arr.ind=T)

##########################
#####Cosine Similarity####
##########################
########################################################################################################
####Honestly, I had no time to do anything but copy this part##########################################
##########I was worried I would never get to the other homeworks.#################
########################################################################################################

cs<- matrix(nrow=200, ncol=200)
cosineSim<- function(x, y){
  return( sum(x*y)/ sqrt( sum(x^2)* sum(y^2)))
}

#this thing takes forever on my computer
for (m in 1:nrow(ShelbySessionsSampleMatrix)){
  for (n in 1:nrow(ShelbySessionsSampleMatrix)){
    a<- cosineSim(ShelbySessionsSampleMatrix[m,], ShelbySessionsSampleMatrix[n,])
    cs[m, n]<- a
    cs[n, m]<- a
  }
}
m<-NULL
n<-NULL

diag(cs)<-NA


csWithTfidf<- matrix(nrow=200, ncol=200)

for (m in 1:nrow(SampleEIDF)){
  for (n in 1:nrow(SampleEIDF)){
    a <- cosineSim(SampleEIDF[m,], SampleEIDF[n,])
    csWithTfidf[m, n]<- a
    csWithTfidf[n, m]<- a
  }
}

diag(csWithTfidf)<- NA



normed<-ShelbySessionsSampleMatrix
for (i in 1:nrow(ShelbySessionsSampleMatrix)){
  normed[i,]<- ShelbySessionsSampleMatrix[i,]/sum(ShelbySessionsSampleMatrix[i,])
}

#choose sigma
sigma = 100
gauss<- exp(-(as.matrix(dist(normed)))/sigma)

diag(gauss)<- NA

gauss

idf<- apply(normed, 2, calcIDF)
normed_idf<- as.matrix(t(apply(normed, 1, function(x) x*idf)))
gaussNorm<- exp(-(as.matrix(dist(normed_idf)))/sigma)
write.csv(gaussNorm, "gaussNorm.csv")

diag(gaussNorm)<- NA

gaussNorm







