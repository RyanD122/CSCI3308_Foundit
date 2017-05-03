#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import praw
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from datetime import datetime, timedelta
import time
import os
from collections import Counter

from rq import Queue
from worker import conn
from . import utils
from django.http import JsonResponse

q = Queue(connection=conn)

workercount=5#totalworkercount =workdercount+1, need one to schedule


#def isascii(s):
#	return all(ord(c) < 128 for c in s)

#def sortdata(lists):


def schedule(subreddit, postLimit, topComLimit, topReplyLimit, topWordLimit, topUserLimit, oldestPostLimit, activePostLimit):
	print("$$$$$$$$$$$$$$$$$$IN SCHEDULER$$$$$$$$$$$$$$$$$$$$$$$$$$")
	jobq=[]
	splits=int(postLimit)/workercount
	index=0
	timeinc=5
	totalinc=0
	# print"Partitions= "+(str(splits))
	qindex=0
	while(index<postLimit):
		startpos=int(index)
		endpos=int(index+splits)
		if(qindex==(workercount)):
			startpos=postLimit-diff
			endpos=postLimit
		#print("START: "+str(startpos)+"  END: "+str(endpos))
		print("QINDEX: "+str(qindex))
		jobq.append(q.enqueue(search, str(subreddit),int(postLimit),int(topComLimit)*2,int(topReplyLimit)*2,int(topWordLimit)*2,int(topUserLimit)*2,int(oldestPostLimit)*2,int(activePostLimit)*2,int(startpos),int(endpos),int(qindex)+1,timeout=200))
		time.sleep(6+qindex)
		index=(index+splits)
		print("INDEX: "+str(index))
		qindex+=1
	rcount=0
	
	while(1):
		flag=1
		for job in jobq:	
			if(not job.result):
				flag = 0
		if(flag):
			break
			
			
	return()
	
	for job in jobq:
		if(job.result):
			rcount+=1
			print(str(job.result[9]))
#	check=0
#	qindex=0
#	results=[]
#	tempc=workercount
#	print("---------------LENGTH: "+str(len(q)))
#	while (check!=workercount):
#		while(qindex!=(workercount)):
#			#print("GINDEX: "+str(qindex))
##			temp=q.fetch_job(jobq[qindex]).get_id.result
#			temp=q.fetch_job(jobq[qindex]).id.result
#			if(temp):
#				results.append(temp)
#				q.remove(q.fetch_job(jobq[qindex]).id)
#				check+=1
##				gindex+=1
#				print("WORKER SEARCH #"+str(qindex)+(" DONE!!!")+"vTOTAL COMPLETE: "+str(check))
#				time.sleep(workercount+3)
#			qindex+=1
#		time.sleep(workercount*2)
#		print("WAITING...")
#		if(check!=workercount):
#			qindex=0
      #COMBINE ALL DATA ONCE CHECK PASSES
      #ORDER OF RETURN FOR WORKERS
      #0titleWords, 1nounDict, 2userDict, 3topCom, 4topReply, 5oldestPost, 6activePost, 7postsAnalyzed, 8totalLengthAll, 9commentsAnalyzed)
	print("#########################ALL WORKERS DONE@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	print("OUTPUTTING ANALYZED DATA HERE@@@@@@@@@@@@")
	return(results)

def getSubmissionAge(submission):
	return(datetime.utcnow()-datetime.utcfromtimestamp(submission.created_utc))

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

def search(subreddit, postLimit, topComLimit, topReplyLimit, topWordLimit, topUserLimit, oldestPostLimit, activePostLimit,startpos,endpos,qindex):
	starttime = time.time()
	print("SEARCHING FROM: "+str(startpos)+" - "+str(endpos))

	topicWordLimit = topWordLimit
	#open reddit instance
	reddit = praw.Reddit(client_id='8cEoUXP_vP3Gpg', client_secret='IuhFngwlEbGdZtAxm5NdvesMa4U', user_agent='pc:foundit:v1.0 (by r/foundit_bot')

	#initialize some variables
	nounDict = {}
	titleWords = {}
	userIgnoreList= ['automoderator']
	nounIgnoreList = ['http', 'https','incivility','bot','shill','troll','hate','speech','subreddit','moderators','wiki_please_be_civil','violation','reminder']
	userDict = {}
	topCom = []
	topReply = []
	oldestPost = []
	activePost = []

	postsAnalyzed = 0
	totalLengthAll = 0
	commentsAnalyzed = 0
	diff=endpos-startpos
	#begin analysis
	#loop through submissions
	index=0
	pcounter=0
	for submission in reddit.subreddit(subreddit).hot(limit=endpos):
		if(index>=startpos):
			pcounter=((float(index-startpos)/float(endpos-startpos))*100)
			print("Searching post: " + str(index)+" - "+"WORKER: "+ str(qindex)+" - " + str(pcounter)+" % ")
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
				if(comment.author != 'automoderator'):
					score = comment.score
					topCom = adjust(topCom, topComLimit, 1, (comment.body, score, submission.title))
					#adjust top replies
					parent = comment.parent()
					if(parent != submission):
						scoreDif = comment.score - parent.score
						if(scoreDif > 0):
							topReply = adjust(topReply, topReplyLimit, 2, (comment.body, parent.body, scoreDif, submission.title))

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
						#if(isascii(word)):
						#print("WORKER: "+str(qindex)+"-----"+(word))
						if(tag == 'NNP' or tag == 'NN'):
							if(word in nounDict):
								nounDict[word] += 1
							else:
								nounDict[word] = 1

					#add to total word count
					totalLengthAll += len(tokens)
					commentsAnalyzed += 1


		postsAnalyzed += 1
		index+=1
					#analysis finished
					#LUKES CODE RETURN WORKER DATA HERE@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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

	print("ANALYSIS DONE!!!!!")
	endttime=time.time()
	ttime=endttime-starttime
	print("-----------------------"+"WORKER: "+str(qindex)+" - TIME: "+str(ttime))
	
	return(toptwords, topWords, topUsers, topCom, topReply, oldestPost, activePost, postsAnalyzed, totalLengthAll, commentsAnalyzed)
