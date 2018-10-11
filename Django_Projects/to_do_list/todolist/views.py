from django.shortcuts import render, redirect
from .models import Todo
from django.core.cache import cache
from django_redis import get_redis_connection


conn = get_redis_connection("default")
lst = Todo.objects.all()
def home(request):

    if request.method == "POST":
        if request.POST['待办事项'] == '':
            content = {'清单': Todo.objects.all(), '警告': '请输入内容！'}
            return render(request, 'todolist/home.html', content)
        else:
            a_row = Todo(thing = request.POST['待办事项'], done = False)
            a_row.save()
            content = { '清单': Todo.objects.all(), '信息': '添加成功'}
            return render(request, 'todolist/home.html', content)

    elif request.method == 'GET':
        content = {'清单': Todo.objects.all()}
        return render(request, "todolist/home.html", content)


def about(request):
    return render(request, 'todolist/about.html')


def edit(request, 每一件事_id):
    if request.method == "POST":
        if request.POST['已修改事项'] == '':
            return render(request, "todolist/edit.html", {'警告': '请输入内容！'})
        else:
            a = Todo.objects.get(id=每一件事_id)
            a.thing = request.POST['已修改事项']
            a.save()
            return redirect("todolist:主页")
    elif request.method == "GET":
        content = { '待修改事项': Todo.objects.get(id=每一件事_id).thing }
    return render(request, 'todolist/edit.html', content)



def delete(request, 每一件事_id):
    a = Todo.objects.get(id=每一件事_id)
    a.delete()
    return redirect("todolist:主页")


def cross(request, 每一件事_id):

    if request.POST['完成状态'] == '已完成':
        a = Todo.objects.get(id=每一件事_id)
        a.done = True
        a.save()
        return redirect("todolist:主页")
    else:
        a = Todo.objects.get(id=每一件事_id)
        a.done = False
        a.save()
        return redirect("todolist:主页")
