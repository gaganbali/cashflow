# Create your views here.
import pandas as pd
import datetime
from django.db.models import Sum
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import View
from django.views.generic import ListView
import main.forms as forms
import main.models as models

class LedgerList(ListView):
    """view that gives list of ledger items on a given day"""
    model = models.Ledger
    context_object_name = 'ledger_items'
    template_name = 'ledger.html'
    
    def get_queryset(self):
        """return ledger items corresponding to date in url"""
        self.ledger_date = datetime.datetime.strptime(self.kwargs['date_string'], '%Y%m%d')
        end_date = self.ledger_date + datetime.timedelta(weeks = 4 * int(self.kwargs['offset']))
        return self.model.objects.filter(date__gte=self.ledger_date, date__lte=end_date)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ledger_date'] = self.ledger_date
        return context

class CashLevelList(View):
    template_name = 'cash_levels.html'
    
    def get(self, request, date_string, begin_level, offset=2):
        """given cash level on given date, display expected cash level
        over time
        
        """
        begin_date = datetime.datetime.strptime(date_string, '%Y%m%d')
        begin_level = float(begin_level)
        ledger_items = models.Ledger.objects.all()
        dates = pd.date_range(begin_date, periods=30*int(offset))
        min_levels, final_levels = [], []
        min_levels.append(begin_level)
        final_levels.append(begin_level)
        for date in dates[1:]:
            expenses = (ledger_items.filter(date = date,
                                            exp_inc = 'exp').aggregate(Sum('amount')))['amount__sum']
            income = (ledger_items.filter(date = date,
                                            exp_inc = 'inc').aggregate(Sum('amount')))['amount__sum']
            if expenses is None:
                expenses = 0
            if income is None:
                income = 0
            min_levels.append(final_levels[-1] - expenses)
            final_levels.append(final_levels[-1] - expenses + income)       
        cash_df = pd.DataFrame({'min_level': min_levels, 'final_level': final_levels,
                                'date': dates})
        cash_df['date_string'] = cash_df['date'].map(lambda dt: dt.strftime('%Y%m%d'))
        return render(request, self.template_name,
                      {'begin_date': begin_date, 'begin_level': begin_level,
                       'cash_df': cash_df.sort('date')})
