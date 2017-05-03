from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^loading/$', views.loading, name='loading'),
    url(r'^loading/checkJob', views.checkJob, name='checkJob'),
    url(r'^testResults/$', views.testResults, name='testResults'),
]
