import praw
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from nltk import word_tokenize
import os

def printTopComments(list):
  print(chr(27) + "[2J")
  print("-Top Comments-")
  for element in list:
    print("-" + str(element[0].score) + " : " + element[0].body)
    print("Post title: " + element[1].title)
  print()

#open reddit instance
reddit = praw.Reddit(client_id='8cEoUXP_vP3Gpg',
                     client_secret='IuhFngwlEbGdZtAxm5NdvesMa4U',
                     user_agent='pc:foundit:v1.0 (by r/foundit_bot')

#gather queue info
subreddit = input('Subreddit: ')
postLimit = int(input('Post Limit: '))
topComLimit = int(input('# top comments to show: '))
topWordLimit = int(input('# top words to show: '))

#initialize some variables
nounsDict = {}
topCom = []
totalLengthAll = 0
commentsAnalyzed = 0

#begin analysis
print(chr(27) + "[2J")
for submission in reddit.subreddit(subreddit).hot(limit=postLimit):
  print("Searching: " + submission.title)
  for comment in submission.comments:
    try:
      #add nouns to dict
      tokens = nltk.word_tokenize(comment.body)
      tagged = nltk.pos_tag(tokens)
      for word, tag in tagged:
        wordLower = word.lower()
        if(tag == 'NNP' or tag == 'NN'):
          if(wordLower in nounsDict):
            nounsDict[wordLower] += 1
          else:
            nounsDict[wordLower] = 1
      
      #add to average word count
      totalLengthAll += len(tokens)
      commentsAnalyzed += 1
      
      #adjust top comment list
      if(len(topCom) < topComLimit):
        topCom.append((comment, submission))
      else:  
          for com, post in topCom:
            if(com.score < comment.score):
              print("added to list")
              topCom.pop(len(topCom) - 1)
              topCom.append((comment, submission))
              topCom.sort(key=lambda x: x[0].score, reverse=True)
              printTopComments(topCom)
              break
        
    #ignore "moreComments" types
    except AttributeError:
      pass

#display top comms        
printTopComments(topCom)

#calc and display top words
topWords = []
for key, value in nounsDict.items():
  if len(topWords) < topWordLimit:
    topWords.append((key, value))
  else:
    topWords.sort(key=lambda x: x[1], reverse=True)
    for keyTop, valueTop in topWords:
      if valueTop < value:
        topWords.pop(len(topWords)-1)
        topWords.append((key, value))
print("-Top Words-")
for key, value in topWords:
  print(str(value) + ": " + key)
print()
import plotly.plotly as py
import plotly.graph_objs as go
import plotly 
plotly.tools.set_credentials_file(username='kefo7771', api_key='Iq4jzTXCXsmRm7sEA0sc')
data = [go.Bar(
            x=[topWords[0][0],topWords[1][0],topWords[2][0]],
            y=[topWords[0][1],topWords[1][1],topWords[2][1]]
    )]

py.iplot(data, filename='Top Words')


#display average comment length
print("Average comment length: " + str(totalLengthAll / commentsAnalyzed) + " words")

#calc and display average top comment length
totalLengthTop = 0
for com, post in topCom:
  tokens = nltk.word_tokenize(com.body)
  totalLengthTop += len(tokens)
print("Average Top comment length: " + str(totalLengthTop / topComLimit) + " words")
