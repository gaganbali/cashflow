from django.db import models

FREQ_INTERVAL_CHOICES = [('M', 'Month(s)'), ('W', 'Week(s)'),
                         ('D', 'Day(s)')]

class RecurItemRaw(models.Model):
    """db that collects user entered info on recurring items"""
    name = models.CharField(max_length=30, unique=True)
    exp_inc = models.CharField(max_length=10, choices=(('exp', 'Expense'), ('inc', 'Income')))
    freq_num = models.IntegerField()
    freq_interval = models.CharField(max_length=10, choices=FREQ_INTERVAL_CHOICES)
    begin_date = models.DateField()
    end_date = models.DateField()
    value = models.FloatField()

class CashLevel(models.Model):
    """db that collects actual cash level on given date"""
    cash_level = models.FloatField()
    date = models.DateField()
