# pylint: disable=F0401
from django.shortcuts import redirect, render
from lists.models import Item, TodoList


def home_page(request):
    return render(request, 'home.html')


def view_list(request, todo_list_id):
    list_ = TodoList.objects.get(id=todo_list_id)
    return render(request, 'list.html', {'todo_list': list_})


def new_list(request):
    list_ = TodoList.objects.create()
    Item.objects.create(text=request.POST['item_text'], todo_list=list_)
    return redirect('/lists/{}/'.format(list_.id))


def add_item(request, todo_list_id):
    list_ = TodoList.objects.get(id=todo_list_id)
    Item.objects.create(text=request.POST['item_text'], todo_list=list_)
    return redirect('/lists/{}/'.format(list_.id))
