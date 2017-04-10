import praw
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize
from datetime import datetime, timedelta
import os

def getSubmissionAge(submission):
  return datetime.utcnow() - datetime.utcfromtimestamp(submission.created_utc)

def search(subreddit, postLimit, topComLimit, topWordLimit, topUserLimit, ohSnapLimit, oldestPostLimit):

  #open reddit instance
  reddit = praw.Reddit(client_id='8cEoUXP_vP3Gpg',
                       client_secret='IuhFngwlEbGdZtAxm5NdvesMa4U',
                       user_agent='pc:foundit:v1.0 (by r/foundit_bot')

  #initialize some variables
  nounDict = {}
  nounIgnoreList = ['http', 'https']
  userDict = {}
  userIgnoreList= ['None']
  topCom = []
  oldestPost = []
  ohSnap = []

  index = 0
  totalLengthAll = 0
  commentsAnalyzed = 0

  #begin analysis
  for submission in reddit.subreddit(subreddit).hot(limit=postLimit):
    
    #adjust oldest post list
    if(len(oldestPost) < oldestPostLimit):
      oldestPost.append((submission, index))
    else:
      for post, ind in oldestPost:
        if(getSubmissionAge(post) < getSubmissionAge(submission)):
          oldestPost.pop(len(oldestPost) - 1)
          oldestPost.append((submission, index))
          oldestPost.sort(key=lambda x: getSubmissionAge(x[0]), reverse=True)
          break
    
    for comment in submission.comments:
      try:
        #find oh snap
        parent = comment.parent()
        if(parent != submission):
          scoreDif = comment.score - parent.score
          if(scoreDif > 0):
            if(len(ohSnap) < ohSnapLimit):
              ohSnap.append((comment, parent, scoreDif))
            else:
              for ohcom, ohparent, ohscoreDif in ohSnap:
                if(ohscoreDif < scoreDif):
                  ohSnap.pop(len(ohSnap) - 1)
                  ohSnap.append((comment, parent, scoreDif))
                  ohSnap.sort(key=lambda x: x[3], reverse=True)
                  break
                      
        #add nouns to dict
        tokens = nltk.word_tokenize(comment.body)
        tagged = nltk.pos_tag(tokens)
        for word, tag in tagged:
          wordLower = word.lower()
          if(tag == 'NNP' or tag == 'NN'):
            if(wordLower in nounDict):
              nounDict[wordLower] += 1
            else:
              nounDict[wordLower] = 1
        
        #add poster to dict
        author = comment.author
        if(author in userDict):
          userDict[author] += 1
        else:
          userDict[author] = 1
        
        #add to average word count
        totalLengthAll += len(tokens)
        commentsAnalyzed += 1
        
        #adjust top comment list
        if(len(topCom) < topComLimit):
          topCom.append((comment, submission))
        else:  
            for com, post in topCom:
              if(com.score < comment.score):
                topCom.pop(len(topCom) - 1)
                topCom.append((comment, submission))
                topCom.sort(key=lambda x: x[0].score, reverse=True)
                break
          
      #ignore "moreComments" types
      except AttributeError:
        pass
    index += 1

  #topComs

  #ohSnap (not working)
    
  #calc top words
  topWords = []
  for key, value in nounDict.items():
    ignoreFlag = False
    for ignore in nounIgnoreList:
      if(key == ignore):
        ignoreFlag = True
    if(not ignoreFlag and len(key) > 1):
      if len(topWords) < topWordLimit:
        topWords.append((key, value))
      else:
        topWords.sort(key=lambda x: x[1], reverse=True)
        for keyTop, valueTop in topWords:
          if valueTop < value:
            topWords.pop(len(topWords)-1)
            topWords.append((key, value))
  #topWords

  #calc top users
  topUsers = []
  for key, value in userDict.items():
    ignoreFlag = False
    for ignore in userIgnoreList:
      if(str(key) == ignore):
        ignoreFlag = True
    if(not ignoreFlag):
      if len(topUsers) < topUserLimit:
        topUsers.append((key, value))
      else:
        topUsers.sort(key=lambda x: x[1], reverse=True)
        for keyTop, valueTop in topUsers:
          if valueTop < value:
            topUsers.pop(len(topUsers)-1)
            topUsers.append((key, value))
  #topUsers

  #totalLengthAll / commentsAnalyzed = averageCommentLengthAll

  #calc and display average top comment length
  if(topComLimit):
    totalLengthTop = 0
    for com, post in topCom:
      tokens = nltk.word_tokenize(com.body)
      totalLengthTop += len(tokens)
    #totalLengthTop / topComLimit = averageTopCommmentLength

  #oldestPosts (use getSubmissionAge(post))
  return (topCom, topWords)

