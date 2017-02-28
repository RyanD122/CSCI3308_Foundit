import praw
import os
import sys
from array import array
from praw.models import MoreComments

#only thing I used twice so far
def printTopComments(top):
  clear = lambda: os.system('cls')
  clear()
  print("-Top Comment List-")
  for topCom in top:
    print(str(topCom[0].score) + " : " + topCom[0].body)
    print("Post title: " + topCom[1].title)
    print()

#open instance of reddit with info from reddit foundit page
reddit = praw.Reddit(client_id='8cEoUXP_vP3Gpg',
                     client_secret='IuhFngwlEbGdZtAxm5NdvesMa4U',
                     user_agent='pc:foundit:v1.0 (by r/foundit_bot')
 
#pull command args 
subQ = sys.argv[1]
subLimit = int(sys.argv[2])
commentQ = int(sys.argv[3])
 
#top will contain a tuple of a comment and it's parent submission
top = []  
avgLengthTotal = 0.0

#loop through top subLimit hot submissions of subreddit subQ
for submission in reddit.subreddit(subQ).hot(limit=subLimit):
  print("Searching: " + submission.title)
  for comment in submission.comments:
    #fill list initially
    if(len(top) < commentQ):
      top.append((comment, submission))
    else:
      #sort top list by score to print in order (should probably just be in the print function)
      top.sort(key=lambda x: x[0].score, reverse=True)
      
      index = 0
      for topCom in top:
        try:
          if(topCom[0].score < comment.score):
            top.pop(len(top)-1)
            top.append((comment, submission))
            printTopComments(top)
            break
          
          #this may not be an accurate avg, but adding all char lengths in one variable seems a bit extreme
          avgLengthTotal = (avgLengthTotal + len(comment.body))/2
          index += 1
          
        #reddit shortens most comments (usually 200 or more) of 1 upvote comments into objects called "MoreComments"
        #right now this script ignores them
        except AttributeError:
          pass
          
printTopComments(top)
print("Average comment length: " + str(avgLengthTotal) + " characters")
sum = 0
for topCom in top:
  sum += len(topCom[0].body)
avgLengthTop = sum / len(top)
print("Average top length: " + str(avgLengthTop))
