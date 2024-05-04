from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from .models import IncomeSource, Expense
import json
from django.db import models
from itertools import chain
from django.core.serializers.json import DjangoJSONEncoder




def index(request):
    total_income = IncomeSource.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    profit = total_income - total_expenses
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    incomes = IncomeSource.objects.filter(user=request.user).order_by('date')
    expenses_by_category = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    expenses_data = {expense['category']: float(expense['total']) for expense in expenses_by_category}

    transactions = sorted(
        list(incomes) + list(expenses),
        key=lambda x: x.date
    )

    balance = 0
    balance_changes = []
    balance_dates = []
    balances = []


    # Iterate through each transaction to calculate the balance changes
    for transaction in transactions:
        if isinstance(transaction, IncomeSource):
            balance += transaction.amount
        elif isinstance(transaction, Expense):
            balance -= transaction.amount
        else:
            continue

        balance_changes.append({
            'category': transaction.category,
            'balance': balance,
        })

    # Collect data for the balance over time chart
    for transaction in transactions:
        balance += transaction.amount if isinstance(transaction, IncomeSource) else -transaction.amount
        balance_dates.append(transaction.date.strftime('%Y-%m-%d'))
        balances.append(balance)

    # Preparing data for the balance chart
    balance_chart_data = json.dumps({
        'dates': balance_dates,
        'balances': balances
    }, cls=DjangoJSONEncoder)

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'profit': profit,
        'expenses': expenses,
        'expenses_data': json.dumps(expenses_data, cls=DjangoJSONEncoder),
        'balance_changes': balance_changes,
        'balance_chart_data': balance_chart_data  # Pass this to the template for Chart.js
    }

    return render(request, 'index.html', context)

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
from django.http import HttpResponseRedirect

def income_expense_list(request):
    incomes = IncomeSource.objects.filter(user=request.user).order_by('date')
    expenses = Expense.objects.filter(user=request.user).order_by('date')


    # Initialize forms without POST data initially
    income_add_form = IncomeAddForm()
    expense_add_form = ExpenseAddForm()
    income_edit_form = IncomeEditForm()
    expense_edit_form = ExpenseEditForm()

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
            income_id = request.POST.get('edit_income_id')  # Ensure you're using the correct field to retrieve the ID
            income_instance = get_object_or_404(IncomeSource, id=income_id)
            income_edit_form = IncomeEditForm(request.POST, instance=income_instance)
            if income_edit_form.is_valid():
                income_edit_form.save()
                return redirect('income_expense_list')

        elif 'edit_expense_submit' in request.POST:
            expense_id = request.POST.get('edit_expense_id')  # Ensure you're using the correct field to retrieve the ID
            expense_instance = get_object_or_404(Expense, id=expense_id)
            expense_edit_form = ExpenseEditForm(request.POST, instance=expense_instance)
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

    # If it's a GET request or no form was submitted, render page with all forms
    return render(request, 'income_expense_list.html', {
        'incomes': incomes,
        'expenses': expenses,
        'income_add_form': income_add_form,
        'expense_add_form': expense_add_form,
        'income_edit_form': income_edit_form,
        'expense_edit_form': expense_edit_form,
    })















