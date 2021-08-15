from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item, List

# Create your views here.
def home_page(request):
    
    items = Item.objects.all()

    return render(request, 'home.html')

def view_list(request, list_id):
    my_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=my_list)
    return render(request, 'list.html', {'items': items})

def new_list(request):
    my_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=my_list)
    print("In new list before redirect")
    return redirect(f'/lists/{my_list.id}/')

def add_item(request, list_id):
    my_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=my_list)
    return redirect(f'/lists/{my_list.id}/')