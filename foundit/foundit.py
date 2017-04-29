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

def search(subreddit, postLimit, topComLimit, topReplyLimit, topWordLimit, topUserLimit, oldestPostLimit, activePostLimit):

  print("SEARCH CALLED")

  topicWordLimit = topWordLimit
  #open reddit instance
  reddit = praw.Reddit(client_id='8cEoUXP_vP3Gpg',
                       client_secret='IuhFngwlEbGdZtAxm5NdvesMa4U',
                       user_agent='pc:foundit:v1.0 (by r/foundit_bot')

  #initialize some variables
  nounDict = {}
  titleWords = {}
  userIgnoreList= ['automoderator']
  nounIgnoreList = ['http', 'https','incivility','bot','shill','troll','hate','speech','subreddit','moderators','wiki_please_be_civil','violation','reminder']
  userDict = {}
  userIgnoreList= ['automoderator']
  userDict = {}
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
    
    print("searching post: " + str(postsAnalyzed))

    #add nouns to dictionary
    tokens = nltk.word_tokenize(submission.title)
    tagged = nltk.pos_tag(tokens)
    for word, tag in tagged:
      tword = word.lower()
      if(tag == 'NNP' or tag == 'NN'):
        if tword in titleWords:
          titleWords[tword] += 1
        else:
          titleWords[tword] = 1
     
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
      if (comment.author != 'automoderator'):
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


    postsAnalyzed += 1

  #analysis finished

  print("analysis done")

  #build top title words
  toptwords = []
  for word, freq in titleWords.items():
    if not word in nounIgnoreList and len(word) > 1:
      toptwords = adjust(toptwords, topWordLimit, 1, (word, freq))    

  print("top title words done")

  #build top words
  topWords = []
  for word, freq in nounDict.items():
    if not word in nounIgnoreList and len(word) > 1:
        topWords = adjust(topWords, topWordLimit, 1, (word, freq))

  print("topwords done")

  #build top users
  topUsers = []
  for user, freq in userDict.items():
    userStr = str(user)
    if userStr != "None":
      topUsers = adjust(topUsers, topUserLimit, 1, (userStr, freq))

  print("top users done")

  #calc top comment length
  averageLengthTop = 0
  if(topComLimit):
    totalLengthTop = 0
    for com, sc, sub in topCom:
      tokens = nltk.word_tokenize(com.body)
      totalLengthTop += len(tokens)
    averageLengthTop = totalLengthTop / topComLimit

  print("top comment done")

  #calc all comment length
  averageLengthAll = 0
  if(postLimit):
    averageLengthAll = totalLengthAll / commentsAnalyzed

  print("all comment done") 

  #refine lists
  refTopCom = []
  for comment, score, submission in topCom:
    refTopCom.append((comment.body, score, submission.title))

  refTopReply = []
  for comment, parent, scoreDif, submission in topReply:
    refTopReply.append((comment.body, parent.body, scoreDif, submission.title))

  refOldestPost = []
  for submission, postsAnalyzed, age, comCount in oldestPost:
    refOldestPost.append((submission.title, postsAnalyzed, age, comCount))

  refActivePost = []
  for submission, postsAnalyzed, comCount in activePost:
    refActivePost.append((submission.title, postsAnalyzed, comCount))

  return (refTopCom, refTopReply, topWords, averageLengthTop, averageLengthAll, topUsers, refOldestPost, refActivePost,toptwords)

