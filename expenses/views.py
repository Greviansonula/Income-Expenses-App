from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
          
        search_str = json.loads(request.body).get("searchStr")
        
        body = request.body
    
        # expenses = Expense.objects.filter(
        #     amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
        #     date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
        #     description__icontains=search_str, owner=request.user) | Expense.objects.filter(
        # #     category__icontains=search_str, owner=request.user)
        # data =expenses.values()
        data = [3, 4]
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    
    context = {
        'expenses':expenses,
        'page_obj': page_obj
        }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    
    if request.method == 'GET':
            return render(request, 'expenses/add_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, date=date, amount=amount, description=description, category=category).save()
        
        messages.success(request, "The expense was saved susccessfully")
        return redirect('expenses')
    
    
@login_required(login_url='/authentication/login')    
def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    
    context = {
        'expense' : expense,
        'values': expense,
        'categories': categories
    }
    if request.method ==  'GET':
        return render(request, 'expenses/edit-expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        
        
        messages.success(request, "The expense was updated susccessfully")
        return redirect('expenses')
    
@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect('expenses')