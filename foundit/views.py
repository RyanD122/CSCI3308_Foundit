from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template import Context

from .models import Queuery

from rq import Queue
from worker import conn
from . import utils

from . import foundit
from . import graph

q = Queue(connection=conn)

def index(request):
  return render(request, 'foundit/index.html')

def loading(request):
  job = q.enqueue(utils.printHello, 'http://heroku.com') #not sure what the heroku.com does
  t = loader.get_template('foundit/loading.html')
  c = Context({ 'jobid': job.id })
  while(1):
    print(job.result)

  return HttpResponse(t.render(c))

def checkJob(request):
  job = q.fetch_job(request.GET['jobid'])
  return HttpResponse(job.result)

def testResults(request):
  return HttpResponse("results!")

def results(request):
  subreddit = request.GET['subreddit']
  postLimit = request.GET['postLimit']
  topComs = request.GET['topComs']
  topReplies = request.GET['topReplies']
  topWords = request.GET['topWords']
  topUsers = request.GET['topUsers']
  oldestPosts = request.GET['oldestPosts']
  activePosts = request.GET['activePosts']
  if(int(postLimit)<10):
    postLimit=10
  if(int(topComs)>15):
    topComs=15
  if(int(topWords)>15):
    topWords=15
  if(int(topUsers)>15):
    topUsers=15
  allList = foundit.search(str(subreddit), int(postLimit), int(topComs), int(topReplies), int(topWords), int(topUsers), int(oldestPosts), int(activePosts))

  topComList = allList[0]
  topRepliesList = allList[1]
  topWordList = allList[2]
  avgLengthTop = allList[3]
  avgLengthAll = allList[4]
  topUserList = allList[5]
  oldestPostList = allList[6]
  activePostList = allList[7]
  
  topicWordList = allList[8]
  supportWordList = allList[9]
  
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
  
  data=(topicWordList, supportWordList)
  supportWordsGraph = graph.urenderGraph(data)
  

  t = loader.get_template('foundit/results.html')
  c = Context({ 'subreddit': subreddit, 'topComList' : topComList, 'topWordsGraph' : topWordsGraph, 'topUsersGraph' : topUsersGraph, 'topicWordsGraph' : topicWordsGraph, 'supportWordsGraph' : supportWordsGraph})
  return HttpResponse(t.render(c))
