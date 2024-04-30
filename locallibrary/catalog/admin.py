from django.contrib import admin
from .models import IncomeSource, Expense, FinancialSummary

admin.site.register(IncomeSource)
admin.site.register(Expense)
admin.site.register(FinancialSummary)
