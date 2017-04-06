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
  topWords = request.GET['topWords']
  topUsers = request.GET['topUsers']
  OhSnap = request.GET['ohSnap']
  OldestPosts = request.GET['oldestPosts']

  allList = foundit.search(str(subreddit), int(postLimit), int(topComs), int(topWords), int(topUsers), int(OhSnap), int(OldestPosts))

  topComList = allList[0]
  topWordList = allList[1]

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
