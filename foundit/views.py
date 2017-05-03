from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template import Context

from .models import Queuery

from rq import Queue
from worker import conn
from . import utils
from django.http import JsonResponse

from . import foundit
from . import graph

from collections import Counter

#subreddit=""
q = Queue(connection=conn)
#workercount=5#totalworkercount =workdercount+1, need one to schedule


def index(request):
	print("@@@@@@@@@@@@@START OF EVERYTHING@@@@@@@@@@@@")
	return render(request, 'foundit/index.html')

def loading(request):
	subreddit = request.GET["subreddit"]
	postLimit = request.GET["postLimit"]
	topComs = request.GET["topComs"]
	topReplies = request.GET["topReplies"]
	topWords = request.GET["topWords"]
	topUsers = request.GET["topUsers"]
	oldestPosts = request.GET["oldestPosts"]
	activePosts = request.GET["activePosts"]
	print("%%%%%%%%%%%STARTING SCHEDULING TEST%%%%%%%%%%%%%%%%")
	print(str(subreddit))
	job = q.enqueue(foundit.schedule,str(subreddit),int(postLimit),int(topComs),int(topReplies),int(topWords),int(topUsers),int(oldestPosts),int(activePosts), timeout=200)
	print("OUT OF SCHEDULER")

	t = loader.get_template('foundit/loading.html')
	c = Context({ 'jobid': job.id })

	return HttpResponse(t.render(c))

def checkJob(request):
	jobid = request.GET['jobid']
	results = q.fetch_job(jobid).result
	if(results):
		return HttpResponse(jobid)
	else:
		return HttpResponse(results)

def testResults(request):
	return HttpResponse("results!")

def results(request):  
	jobid = request.GET['jobid']
	results = q.fetch_job(jobid).result

	topComList = results[0]
	topRepliesList = results[1]
	topWordList = results[2]
	avgLengthTop = results[3]
	avgLengthAll = results[4]
	topUserList = results[5]
	oldestPostList = results[6]
	activePostList = results[7]

	topicWordList = results[8]
	subreddit=results[9]
	#supportWordList = allList[9]

	#compile graph for topWords
	topWordCounts = [x[1] for x in topWordList]
	topWords = [x[0] for x in topWordList]
	topWordsData = (topWordCounts, "Top Words", "Occurances", topWords)
	topWordsGraph = graph.renderGraph(topWordsData)

	#compile graph for topUsers
	topUserCounts = [x[1] for x in topUserList]
	topUsers = [x[0] for x in topUserList]
	topUsersData = (topUserCounts, "Top Users", "Activity", topUsers)
	topUsersGraph = graph.renderGraph(topUsersData)

	#LUKES TEST GRAPHS

	#Topic Words Graph
	topicWordCounts = [x[1] for x in topicWordList]
	topicWords = [x[0] for x in topicWordList]
	topicWordsData = (topicWordCounts, "Topic Words", "Occurances", topicWords)
	topicWordsGraph = graph.renderGraph(topicWordsData)  

	#data=(topicWordList, supportWordList)
	#supportWordsGraph = graph.urenderGraph(data)


	#subreddit = "placeholder, need to make foundit.py return subreddit"

	t = loader.get_template('foundit/results.html')
	c = Context({ 'subreddit': subreddit, 'topComList' : topComList, 'topWordsGraph' : topWordsGraph, 'topUsersGraph' : topUsersGraph, 'topicWordsGraph' : topicWordsGraph,}) #'supportWordsGraph' : supportWordsGraph})
	return HttpResponse(t.render(c))
