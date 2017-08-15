from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^(?P<course_no>\d+)/$', views.detail, name='detail'),
        url(r'^topic/$', views.topic, name='topic'),
        url(r'^addtopic/$', views.addtopic, name='addtopic'),
        url(r'^topic/(?P<topic_id>\d+)/$', views.topicdetail, name='topicdetail'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^mycourses/$', views.mycourses, name='mycourses'),
        url(r'^forgotpass/$', views.forgotpass, name='forgotpass'),
        ]
