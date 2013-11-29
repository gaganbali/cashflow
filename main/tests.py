"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import main.models as models
import datetime


class TestRecurItem(TestCase):
    
    def test__date_range(self):
        begin_date = datetime.date(2013, 11, 15)
        end_date = datetime.date(2014, 2, 15)
        freq_num = 2
        freq_interval = 'W'
        date_range = models._date_range(begin_date, end_date, freq_num,
                                        freq_interval)
        self.assertEqual(len(date_range), 7)
        self.assertEqual(date_range[0].date(), begin_date)
        self.assertEqual(date_range[-1].date(), datetime.date(2014, 2, 7))
    
    def test_populate_ledger__new_item(self):
        name = 'test'
        exp_inc = 'inc'
        begin_date = datetime.date(2013, 11, 15)
        end_date = datetime.date(2014, 2, 15)
        amount = 1000
        freq_num = 2
        freq_interval = 'W'
        recur_item = models.RecurItem(name=name, exp_inc=exp_inc,
                                      begin_date=begin_date, end_date=end_date,
                                      amount=amount, freq_num=freq_num,
                                      freq_interval=freq_interval)
        recur_item.save()
        recur_item.populate_ledger()
        ledger_items = models.Ledger.objects.filter(recur_item=recur_item)
        self.assertEqual(len(ledger_items), 7)
        self.assertEqual(ledger_items[0].name, name)
        self.assertEqual(ledger_items[0].date, begin_date)
        self.assertEqual(ledger_items[0].recur_item, recur_item)
    
    def test_populate_ledger__existing_item(self):
        name = 'test'
        exp_inc = 'inc'
        begin_date = datetime.date(2013, 11, 15)
        end_date = datetime.date(2014, 2, 15)
        amount = 1000
        freq_num = 2
        freq_interval = 'W'
        recur_item = models.RecurItem(name=name, exp_inc=exp_inc,
                                      begin_date=begin_date, end_date=end_date,
                                      amount=amount, freq_num=freq_num,
                                      freq_interval=freq_interval)
        recur_item.save()
        ledger1 = models.Ledger(name=name, date=datetime.date(2013, 11, 29),
                                amount=600, recur_item=recur_item)
        ledger1.save()
        recur_item.populate_ledger()
        ledger_item = (models.Ledger.objects.filter(recur_item=recur_item)
                       .get(date=datetime.date(2013, 11, 29)))
        self.assertEqual(ledger_item.amount, 600)