from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.registeruser, name='signup'),
    url(r'^logout/$', views.mylogout, name='logout'),
    url(r'^profile/(?P<id>.+)$', views.profile, name='profile'),
    url(r'^details/$', views.details, name='details'),
    url(r'^imgupload/$', views.imgupload, name='imgupload'),
    url(r'^apply/(?P<id>.+)$', views.apply, name='apply')
]