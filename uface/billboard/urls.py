from django.conf.urls import patterns, include, url

urlpatterns = patterns('billboard.views',
    url(r'^$', 'index'),
    url(r'^test/$', 'test'),
    url(r'^init/$', 'init'),
    #url(r'^(?P<poll_id>\d+)/$', 'detail'),
    #url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)