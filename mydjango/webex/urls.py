from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'webex'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detal, name='detal'),
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('smarp/', views.smarp, name='smarp_page'),


    #path('1/', views.detal, name='detal'),
    #path('2/', views.detal, name='detal'),
    #path('3/', views.detal, name='detal'),
]
