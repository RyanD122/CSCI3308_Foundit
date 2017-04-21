from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template import Context

from .models import Queuery

from . import foundit
from . import graph

def index(request):
  return render(request, 'foundit/index.html')

def results(request):
  subreddit = request.GET['subreddit']
  postLimit = request.GET['postLimit']
  topComs = request.GET['topComs']
  topReplies = request.GET['topReplies']
  topWords = request.GET['topWords']
  topUsers = request.GET['topUsers']
  oldestPosts = request.GET['oldestPosts']
  activePosts = request.GET['activePosts']

  allList = foundit.search(str(subreddit), int(postLimit), int(topComs), int(topReplies), int(topWords), int(topUsers), int(oldestPosts), int(activePosts))

  topComList = allList[0]
  topRepliesList = allList[1]
  topWordList = allList[2]
  avgLengthTop = allList[3]
  avgLengthAll = allList[4]
  topUserList = allList[5]
  oldestPostList = allList[6]
  activePostList = allList[7]
  
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

  t = loader.get_template('foundit/results.html')
  c = Context({ 'subreddit': subreddit, 'topComList' : topComList, 'topWordsGraph' : topWordsGraph, 'topUsersGraph' : topUsersGraph})
  return HttpResponse(t.render(c))
