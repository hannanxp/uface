from django.conf.urls import patterns, include, url

urlpatterns = patterns('billboard.views',
    url(r'^$', 'index'),
    url(r'^acceptmsg/$', 'acceptmsg'),
    url(r'^delmsg/$', 'delmsg'),
    url(r'^saveapps/$', 'saveapps'),
)