from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from .models import IncomeSource, Expense
import json
from django.db import models
from itertools import chain




def index(request):


    total_income = IncomeSource.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    profit = total_income - total_expenses

    expenses = Expense.objects.filter(user=request.user)
    incomes = IncomeSource.objects.filter(user=request.user)
    expenses_by_category = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    expenses_data = {expense['category']: float(expense['total']) for expense in expenses_by_category}


    transactions = list(chain(incomes, expenses))

    # Sort the transactions based on the date attribute
    transactions = sorted(transactions, key=lambda transaction: transaction.date)

    # Initialize the starting balance
    balance = 0
    
    # Create a list to store the balance and category for each transaction
    balance_changes = []

    # Iterate through each transaction to calculate the balance changes
    for transaction in transactions:
        if isinstance(transaction, IncomeSource):
            balance += transaction.amount
            category = transaction.category  # Accessing category attribute directly
        elif isinstance(transaction, Expense):
            balance -= transaction.amount
            category = transaction.category  # Accessing category attribute directly
        else:
            continue

        balance_changes.append({
            'category': category,  # Using the extracted category
            'balance': balance,
        })

    # Print balance_changes for debugging
        print(balance_changes)

    context = {
         'total_income': total_income,
         'total_expenses': total_expenses,
         'profit': profit,
         'expenses': expenses,
         'expenses_data': json.dumps(expenses_data),
          'balance_changes': balance_changes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import IncomeAddForm, IncomeEditForm, ExpenseAddForm, ExpenseEditForm
from .models import IncomeSource, Expense
from django.db.models import Sum

def income_expense_list(request):
    incomes = IncomeSource.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)


  
    
    income_add_form = IncomeAddForm()
    expense_add_form = ExpenseAddForm()
    income_edit_form = None
    expense_edit_form = None
    
    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_add_form = IncomeAddForm(request.POST)
            if income_add_form.is_valid():
                income = income_add_form.save(commit=False)
                income.user = request.user
                income.save()
                return redirect('income_expense_list')
        elif 'expense_submit' in request.POST:
            expense_add_form = ExpenseAddForm(request.POST)
            if expense_add_form.is_valid():
                expense = expense_add_form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('income_expense_list')
        elif 'edit_income_submit' in request.POST:
            income_id = request.POST.get('edit_income')
            income = get_object_or_404(IncomeSource, id=income_id)
            income_edit_form = IncomeEditForm(request.POST, instance=income)
            if income_edit_form.is_valid():
                income_edit_form.save()
                return redirect('income_expense_list')
        elif 'edit_expense_submit' in request.POST:
            expense_id = request.POST.get('edit_expense')
            expense = get_object_or_404(Expense, id=expense_id)
            expense_edit_form = ExpenseEditForm(request.POST, instance=expense)
            if expense_edit_form.is_valid():
                expense_edit_form.save()
                return redirect('income_expense_list')
        elif 'delete_expense' in request.POST:
            expense_id = request.POST.get('delete_expense')
            expense = get_object_or_404(Expense, id=expense_id)
            expense.delete()
            return redirect('income_expense_list')
        elif 'delete_income' in request.POST:
            income_id = request.POST.get('delete_income')
            income = get_object_or_404(IncomeSource, id=income_id)
            income.delete()
            return redirect('income_expense_list')

    return render(request, 'income_expense_list.html', {
        'incomes': incomes,
        'expenses': expenses,
        'income_add_form': income_add_form,
        'expense_add_form': expense_add_form,
        'income_edit_form': income_edit_form,
        'expense_edit_form': expense_edit_form,
    })














