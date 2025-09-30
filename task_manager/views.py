from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .models import Task


def index(request):
    title = "Task Manager Home"
    return render(request, "index.html", {"title": title})


def task_list(request):
    tasks = Task.objects.all()
    print(tasks)
    return render(request, "task_list.html", {"tasks": tasks})


def task_detail(request, task):
    task_detail = get_object_or_404(Task, id=task)
    return render(request, "task_detail.html", {"task": task_detail})


def about(request):
    return render(request, "about.html")

def create_task(request):
    return render(request, "create_task.html")

