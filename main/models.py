from django.db import models
import pandas as pd

FREQ_INTERVAL_CHOICES = [('M', 'Month(s)'), ('W', 'Week(s)'),
                         ('D', 'Day(s)')]

WEEKDAYS = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI',
            5: 'SAT', 6: 'SUN'}

def _date_range(begin_date, end_date, freq_num, freq_interval):
    """list of dates between begin date and end date at given interval"""
    if freq_interval == 'M':
        day_offset = begin_date.day - 1
        return (pd.date_range(begin_date, end_date, freq = 'MS')
                      .shift(day_offset, freq=pd.datetools.day))
    if freq_interval == 'W':
        freq_interval += '-{}'.format(WEEKDAYS[begin_date.weekday()])
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
            try:
                ledger_item = Ledger.objects.get(name=self.name, date=date)
                if override:
                    ledger_item.recur_item = self
                    ledger_item.exp_inc = self.exp_inc
                    ledger_item.amount = self.amount
                ledger_item.save()
            except Ledger.DoesNotExist:
                Ledger.objects.create(name=self.name, date=date,
                        exp_inc=self.exp_inc, amount=self.amount, recur_item=self)

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
    recur_item = models.ForeignKey(RecurItem, blank=True, null=True)
    
    class Meta:
        ordering = ['date', 'name']
        unique_together = ('name', 'date')
    
    def __str__(self):
        return '%s (%s)' % (self.name, self.date)
    
    @property
    def recurring(self):
        """True if ledger item has a recur item"""
        return (self.recur_item is not None)
    
    @property
    def expense(self):
        """expense amount if type is expense"""
        if self.exp_inc == 'exp':
            return self.amount
    
    @property
    def income(self):
        """income amount if type is income"""
        if self.exp_inc == 'inc':
            return self.amount
    
