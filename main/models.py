from django.db import models


class RecurringAdjustments(models.Model):
    """db that tracks expected adjustments to cashflow"""
    name = models.CharField(max_length=30)
    base_date = models.DateField()
    date_offset = models.CharField(max_length=20)
    value = models.FloatField()
    exact = models.BooleanField()

class RecurItemRaw(models.Model):
    """db that collects user entered info on recurring items"""
    name = models.CharField(max_length=30)
    exp_inc = models.CharField(max_length=10)
    freq_num = models.IntegerField()
    freq_interval = models.CharField(max_length=10)
    base_date = models.DateField()
    value = models.FloatField()

class OverrideItem(models.Model):
    """db that collects user entered info on recurring item values
    to override
    
    """
    recur_item = models.ForeignKey(RecurItemRaw)
    date = models.DateField()
    value = models.FloatField()
