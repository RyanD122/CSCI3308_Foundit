from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^foundit/', include('foundit.urls')),
]
