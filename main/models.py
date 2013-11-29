from django.db import models
import pandas as pd

FREQ_INTERVAL_CHOICES = [('M', 'Month(s)'), ('W', 'Week(s)'),
                         ('D', 'Day(s)')]

def _date_range(begin_date, end_date, freq_num, freq_interval):
    """list of dates between begin date and end date at given interval"""
    if freq_interval == 'M':
        day_offset = begin_date.day - 1
        return (pd.date_range(begin_date, end_date, freq = 'MS')
                      .shift(day_offset, freq=pd.datetools.day))
    return pd.date_range(begin_date, end_date,
                               freq = '{}{}'.format(freq_num, freq_interval))

class RecurItem(models.Model):
    """db that collects user entered info on recurring items"""
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    exp_inc = models.CharField(max_length=10, choices=(('exp', 'Expense'), ('inc', 'Income')))
    freq_num = models.IntegerField()
    freq_interval = models.CharField(max_length=10, choices=FREQ_INTERVAL_CHOICES)
    begin_date = models.DateField()
    end_date = models.DateField()
    amount = models.FloatField()
    
    def __str__(self):
        return self.name
    
    def populate_ledger(self, override=False):
        """populate rows in ledger based on row of recur item
        create or update rows but don't override amount if already there
        
        """
        date_range = _date_range(self.begin_date, self.end_date,
                                 self.freq_num, self.freq_interval)
        for date in date_range:
            ledger_item = Ledger(name=self.name, date=date,
                                 exp_inc=self.exp_inc, recur_item=self)
            if override or ledger_item.amount is None:
                ledger_item.amount = self.amount
            ledger_item.save()

class CashLevel(models.Model):
    """db that collects actual cash level on given date"""
    cash_level = models.FloatField()
    date = models.DateField(unique=True, primary_key=True)
    
    def __str__(self):
        return '%s' % self.date

class Ledger(models.Model):
    """lists income/expense items by date as built from recurring items
    and manually entered items
    
    """
    name = models.CharField(max_length=30)
    date = models.DateField()
    amount = models.FloatField()
    exp_inc = models.CharField(max_length=10, choices=(('exp', 'Expense'), ('inc', 'Income')))
    recur_item = models.ForeignKey(RecurItem, blank=True)
    
    class Meta:
        ordering = ['-date', 'name']
        unique_together = ('name', 'date')
    
