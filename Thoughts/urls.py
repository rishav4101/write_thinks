from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add_thot/', views.add_thot, name="add_thot"),
    path('view_thought/<int:thought_id>/',
         views.view_thought, name='view_thought'),
    path('profile/', views.profile, name="profile"),
    #path('like/<int:thought_id>', views.like, name="like")
]
