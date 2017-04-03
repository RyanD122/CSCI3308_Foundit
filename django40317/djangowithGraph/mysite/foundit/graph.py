"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import mpld3 as mpld3
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins

def renderGraph(dataSet):

  data = dataSet[0]
  title = dataSet[1]
  ylabel = dataSet[2]
  xlabels = dataSet[3]

  ind = np.arange(len(data))  # the x locations for the groups
  width = 0.35       # the width of the bars

  fig, ax = plt.subplots()
  #print 'Before figure'
  chart = plt.figure()
  #print 'After first figure'

  rects1 = ax.bar(ind, data, width, color='r')

  # add some text for labels, title and axes ticks
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.set_xticks(ind + width / 2)
  ax.set_xticklabels(xlabels)

  def autolabel(rects):
      """
      Attach a text label above each bar displaying its height
      """
      for rect in rects:
          height = rect.get_height()
          ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                  '%d' % int(height),
                  ha='center', va='bottom')

  autolabel(rects1)
  #fig_to_html attempt
  #current error: 'Figure' object has no attribute 'fig_to_html'
  
  #needed to download jinja2 for mpld3 to work
  graphOutput = plt.figure() #initialize variable as current graph to be later passed on to HTML code
  graphHTML = fig_to_html(graphOutput) #convert current graph to HTML code
  #print graphHTML
  #plt.show()
  plt.close(graphOutput) #close the current graph
  mpld3.display(chart)
  return graphHTML


