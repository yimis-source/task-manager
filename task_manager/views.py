from datetime import date
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task
from .forms import crete_new_taskForm


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
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        year = int(request.POST["due_date_year"])
        month = int(request.POST["due_date_month"])
        day = int(request.POST["due_date_day"])
        due_date = date(year, month, day)

        Task.objects.create(title=title, description=description, due_date=due_date)

        return redirect("/tasks/")
    elif request.method == "GET":
        return render(request, "create_task.html", {"form": crete_new_taskForm()})
