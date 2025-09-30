from task_manager import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('about', views.about),  
    path('tasks/', views.task_list, ),
    path('detail/<int:task>', views.task_detail, ),
    path('create-task/', views.create_task,),

]