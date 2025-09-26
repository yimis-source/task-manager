from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import JsonResponse
from .models import Task

def index(request):
    return HttpResponse("Hello, world. index.")

def about(request):
    return HttpResponse("Hello, world. You're at the about index.")
    

def task_list(request,task):
    return HttpResponse("Hello, world. You're at the task %s manager index."% task)
    #return render(request, 'base.html')

def task_detail(request,task):
    task_detail= get_object_or_404(Task, id=task)


    return HttpResponse('task %s' %task_detail.title)
