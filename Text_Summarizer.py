# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Importing required libraries
import bs4 as bs
import urllib.request
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import heapq

#Document that needs to be summarized
src=urllib.request.urlopen('https://en.wikipedia.org/wiki/Global_warming').read();

#parsing the document using lxml parser
soup=bs.BeautifulSoup(src,'lxml');

#Extracting contents of the <p> html tag from the page
text=" "
for par in soup.find_all('p'):
    text+= par.text;
    
#Preprocessing data 

text= re.sub(r"\[[0-9]*\]"," ",text)       #removing the no's inside []
text= re.sub(r"\s+"," ",text)              #removing extra spcaes generated

clean_text=text.lower();
clean_text=re.sub(r'\W',' ',clean_text)
clean_text=re.sub(r'\d',' ',clean_text)
clean_text=re.sub(r'\s+',' ',clean_text)

sentences=nltk.sent_tokenize(text)          #tokenizing the article into sentences

stop_words=nltk.corpus.stopwords.words('english')

#Storing the count of words 
word2count={}
for word in nltk.word_tokenize(clean_text):
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word]=1
        else:
            word2count[word]+=1

#Normalising the count           
for key in word2count.keys():
    word2count[key]=word2count[key]/max(word2count.values())
 
#Generating scores of sentences by summing up probabilities of individual words               
score={}
for s in sentences:
   for word in nltk.word_tokenize(s.lower()):
       if word in word2count.keys():
           if len(s.split(' '))<25:         #since we dont wan't very long sentences
               if s not in score.keys():
                   score[s]= word2count[word]
               else:
                   score[s]+=word2count[word]
                   
#Selecting top n=8 sentences                  
output=heapq.nlargest(8,score,key=score.get)               

#Printing the summarized article               
for sentence in output:
    print(sentence)      

