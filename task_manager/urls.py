from task_manager import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('about', views.about),  
    path('tasks/<int:task>', views.task_list, ),
    path('detail/<int:task>', views.task_detail, ),

]