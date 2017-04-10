"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""



import numpy as np
import matplotlib.pyplot as plt

def renderGraph(dataSet):

  data = dataSet[0]
  title = dataSet[1]
  ylabel = dataSet[2]
  xlabels = dataSet[3]

  ind = np.arange(len(data))  # the x locations for the groups
  width = 0.35       # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, data, width, color='r')

  #women_means = (25, 32, 34, 20, 25)
  #women_std = (3, 5, 2, 3, 3)
  #rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

  # add some text for labels, title and axes ticks
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.set_xticks(ind + width / 2)
  ax.set_xticklabels(xlabels)

  #ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


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
  #autolabel(rects2)

  plt.show()
