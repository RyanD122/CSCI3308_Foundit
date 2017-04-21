import praw
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from datetime import datetime, timedelta
import os

def getSubmissionAge(submission):
  return datetime.utcnow() - datetime.utcfromtimestamp(submission.created_utc)

def adjust(l, limit, indexToCompare, thingToAdd):
    #fill list to limit
    if(len(l) < limit):
      l.append(thingToAdd)
      l.sort(key=lambda x: x[indexToCompare], reverse=True)
    #replace lowest value of indexToCompare with thingToAdd
    else:
      for item in l:
        if(thingToAdd[indexToCompare] > item[indexToCompare]):
          l.pop(len(l) - 1)
          l.append(thingToAdd)
          l.sort(key=lambda x: x[indexToCompare], reverse=True)
          break
    return l

def search(subreddit="all", postLimit=0, topComLimit=0, topReplyLimit=0, topWordLimit=0, topUserLimit=0, oldestPostLimit=0, activePostLimit=0):

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
  topReply = []
  oldestPost = []
  activePost = []

  postsAnalyzed = 0
  totalLengthAll = 0
  commentsAnalyzed = 0

  #begin analysis

  #loop through submissions
  for submission in reddit.subreddit(subreddit).hot(limit=postLimit):

    #get all comments including replies
    submission.comments.replace_more(limit=0)
    all_comments = submission.comments.list()
    comCount = len(all_comments)

    #adjust active post list
    activePost = adjust(activePost, activePostLimit, 2, (submission, postsAnalyzed, comCount))

    #adjust oldest post list
    age = getSubmissionAge(submission)
    oldestPost = adjust(oldestPost, oldestPostLimit, 2, (submission, postsAnalyzed, age, comCount))

    #loop through all comments
    for comment in all_comments:
      try:

        #adjust top comments
        score = comment.score
        topCom = adjust(topCom, topComLimit, 1, (comment, score, submission))
        
        #adjust top replies
        parent = comment.parent()
        if(parent != submission):
          scoreDif = comment.score - parent.score
          if(scoreDif > 0):
            topReply = adjust(topReply, topReplyLimit, 2, (comment, parent, scoreDif, submission))

        #add poster to dict
        author = comment.author
        if(author in userDict):
          userDict[author] += 1
        else:
          userDict[author] = 1

        #add nouns to dict
        tokens = nltk.word_tokenize(comment.body)
        tagged = nltk.pos_tag(tokens)
        for word, tag in tagged:
          word = word.lower()
          if(tag == 'NNP' or tag == 'NN'):
            if(word in nounDict):
              nounDict[word] += 1
            else:
              nounDict[word] = 1

        #add to total word count
        totalLengthAll += len(tokens)
        commentsAnalyzed += 1

        #ignore "moreComments" type
      except AttributeError:
        pass

    postsAnalyzed += 1

  #analysis finished

  print("analysis finished")

  #build top words
  topWords = []
  for word, freq in nounDict.items():
    if not word in nounIgnoreList and len(word) > 1:
        topWords = adjust(topWords, topWordLimit, 1, (word, freq))

  print("topword build finished")

  #build top users
  topUsers = []
  for user, freq in userDict.items():
    print(user.fullname)
    if not user in userIgnoreList:
      topUsers = adjust(topUsers, topUserLimit, 1, (user.fullname, freq))

  print("topusers build finished")

  #calc top comment length
  averageLengthTop = 0
  if(topComLimit):
    totalLengthTop = 0
    for com, sc, sub in topCom:
      tokens = nltk.word_tokenize(com.body)
      totalLengthTop += len(tokens)
    averageLengthTop = totalLengthTop / topComLimit

  #calc all comment length
  averageLengthAll = 0
  if(postLimit):
    averageLengthAll = totalLengthAll / commentsAnalyzed

  return (topCom, topReply, topWords, averageLengthTop, averageLengthAll, topUsers, oldestPost, activePost)

