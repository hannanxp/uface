from django.conf.urls import patterns, include, url

urlpatterns = patterns('billboard.views',
    url(r'^$', 'index'),
    url(r'^test/$', 'test'),
    url(r'^load/$', 'load'),
    url(r'^chpos/$', 'chpos'),
    url(r'^acceptmsg/$', 'acceptmsg'),
)