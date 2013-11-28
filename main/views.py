# Create your views here.
import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import View
import main.forms as forms
from main.models import RecurItemRaw

class AddItemView(View):
    form_class = forms.RecurringItemForm
    items_model = RecurItemRaw
    template_name = 'recurring_adj_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'recur_form': self.form_class(),
                       'items': self.items_model.objects.all()})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.save()
        return render(request, self.template_name,
                      {'recur_form': self.form_class(),
                       'items': self.items_model.objects.all()})
        

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