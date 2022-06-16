from django.conf.urls import url
from django.urls import include
from . import views  

urlpatterns = [
    url(r'^$', views.index),
    url(r'signin$', views.signin),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'dashboard$', views.dash),
    url(r'create$', views.create),
    url(r'new/user$', views.new),
    url(r'update$', views.update),
    url(r'update-pw$', views.updatepw),
    url(r'edit/(?P<num>\d+)$', views.edit),
    url(r'show/(?P<num>\d+)$', views.show),
    url(r'destroy/(?P<num>\d+)$', views.destroy),
    url(r'new/message$', views.new_message),
    url(r'new/comment$', views.new_comment),
    url(r'like/message/(?P<num>\d+)$', views.msg_like),
    url(r'like/comment/(?P<num>\d+)$', views.cmnt_like),
    url(r'unlike/message/(?P<num>\d+)$', views.msg_unlike),
    url(r'unlike/comment/(?P<num>\d+)$', views.cmnt_unlike),
    url(r'logout$', views.logout),
]