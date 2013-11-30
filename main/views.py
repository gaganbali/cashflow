# Create your views here.
import pandas as pd
import datetime
from django.db.models import Sum
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import View
import main.forms as forms
import main.models as models

class LedgerList(View):
    template_name = 'ledger.html'
    
    def get(self, request, date_string, offset):
        """show ledger starting from given date"""
        begin_date = datetime.datetime.strptime(date_string, '%Y%m%d')
        ledger_items = models.Ledger.objects.filter(date__gte=begin_date,
                            date__lte=begin_date + datetime.timedelta(weeks=4*int(offset)))
        return render(request, self.template_name,
                      {'ledger_date': begin_date, 'ledger_items': ledger_items})

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
        return render(request, self.template_name,
                      {'begin_date': begin_date, 'begin_level': begin_level,
                       'cash_df': cash_df.sort('date')})
