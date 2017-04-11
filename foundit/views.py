from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template import Context

from .models import Queuery

from . import foundit
from . import graph

def index(request):
  return render(request, 'foundit/index.html')

#def results(request, subreddit):

#def index(request):
 #   latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #  template = loader.get_template('polls/index.html')
   # context = {
    #    'latest_question_list': latest_question_list,
    #}
    #return HttpResponse(template.render(context, request))
#or better return render(request, 'polls/index.html', context)

#try:
# question = Question.objects.get(pk=question_id)
#except Question.DoesNotExist:
# raise Http404("Question does not exist")
#return render(request, 'polls'detail.html', {'question':question})

#shortcut get_object_or_404 exists

###############

#  response = "You're looking at the results of subreddit %s."
#  return HttpResponse(response % subreddit)

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
  

  topWordCounts = []
  topWords = []
  for key, value in topWordList:
    topWordCounts.append(value)
    topWords.append(key)

  dataSet = (topWordCounts, "Top Words", "Occurances", topWords)

  graphString = graph.renderGraph(dataSet)

  t = loader.get_template('foundit/results.html')
  c = Context({ 'subreddit': subreddit, 'topComList' : topComList, 'topWordList' : topWordList, 'Graph' : graphString })
  return HttpResponse(t.render(c))
