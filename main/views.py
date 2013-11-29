# Create your views here.
import pandas as pd
import datetime
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import View
import main.forms as forms
import main.models as models

class LedgerList(View):
    template_name = 'ledger.html'
    
    def _prepare_ledger(self):
        """prepare ledger by populating from RecurItem"""
        for recur_item in models.RecurItem.objects.all():
            recur_item.populate_ledger()
    
    def get(self, request, date_string, offset):
        """show ledger starting from given date"""
        begin_date = datetime.datetime.strptime(date_string, '%Y%m%d')
        self._prepare_ledger()
        ledger_items = models.Ledger.objects.filter(date__gte=begin_date,
                            date__lte=begin_date + datetime.timedelta(weeks=4*int(offset)))
        return render(request, self.template_name,
                      {'ledger_date': begin_date, 'ledger_items': ledger_items})