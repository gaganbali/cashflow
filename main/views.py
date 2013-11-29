# Create your views here.
import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import View
import main.forms as forms
import main.models as models

class AddDisplayItemView(View):
    form_class = None
    form_name = None
    model = None
    template_name = None

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {self.form_name: self.form_class(),
                       'items': self.model.objects.all()})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.save()
        return render(request, self.template_name,
                      {self.form_name: self.form_class(),
                       'items': self.model.objects.all()})
        
class RecurItemView(AddDisplayItemView):
    form_class = forms.RecurringItemForm
    form_name = 'recur_form'
    model = models.RecurItem
    template_name = 'recurring_adj_form.html'

class CashView(AddDisplayItemView):
    form_class = forms.CashLevelForm
    form_name = 'cash_form'
    model = models.CashLevel
    template_name = 'view_cash.html'
    
