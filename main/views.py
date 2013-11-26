# Create your views here.
import pandas as pd
from django.shortcuts import render
from django.contrib import messages
import main.forms as forms
from main.models import RecurItemRaw, OverrideItem

def add_recurring(request):
    """adds recurring items and override to appropriate models"""
    if request.POST:
        if "recur" in request.POST:
            recur_form = forms.RecurringItemForm(request.POST)
            if recur_form.is_valid():
                messages.success(request, 'Your recurring item was successfully saved.')
                cleaned = recur_form.cleaned_data
                row = RecurItemRaw(name=cleaned['name'],
                        exp_inc=cleaned['exp_inc'],
                        freq_num=cleaned['freq_num'],
                        freq_interval=cleaned['freq_interval'],
                        begin_date=cleaned['begin_date'],
                        end_date=cleaned['end_date'],
                        value=cleaned['value'])
                row.save()
        elif "override" in request.POST:
            override_form = forms.OverrideItemForm(request.POST)
            if override_form.is_valud():
                messages.success(request, 'Your override item was successfully saved.')
                cleaned = override_form.cleaned_data
                recur_item = RecurItemRaw.objects.filter(name=cleaned['name'])[0]
                row = OverrideItem(recur_item=recur_item,
                                   date=cleaned['date'],
                                   value=cleaned['value'])
                row.save()
    recur_form = forms.RecurringItemForm()
    override_form = forms.OverrideItemForm()
    return render(request, 'recurring_adj_form.html',
                  {'recur_form': recur_form, 
                   'override_form': override_form, 
                   'items': RecurItemRaw.objects.all()})

def view_cash(request):
    """lists predicted cash each day based on current cash input
    and predicted inflows/outflows
    
    """
    cash_table = pd.DataFrame()
    if request.POST:
        if "recur" in request.POST:
            cash_form = forms.CashLevelForm(request.POST)
            if cash_form.is_valid():
                messages.success(request, 'Cash level updated.')
                cleaned = cash_form.cleaned_data
                cash_table = calc_expected_cash(cleaned['date'], cleaned['cash_level'])
    cash_form = forms.CashLevelForm()
    return render(request, 'view_cash.html',
                  {'cash_form': cash_form,
                   'cash_table': cash_table})


def calc_expected_cash(start_date, start_level):
    return pd.DataFrame({'date': [start_date], 'cash_level': [start_level]})