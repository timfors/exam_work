from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('recruit/', views.recruit_register),
    path('recruit/test/', views.test_recruit),
    path('sith/', views.sith),
    path('sith/<int:sithid>/', views.all_recruits),
    path('sith/<int:sithid>/<int:recruitid>/', views.recruit_answer),

]