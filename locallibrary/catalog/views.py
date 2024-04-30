from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from .models import IncomeSource, Expense

def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
         'num_visits': num_visits,
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














