from django import forms
from django.forms.extras import widgets
import main.models as models

class RecurringItemForm(forms.ModelForm):
    
    class Meta:
        model = models.RecurItemRaw
        fields = ['name', 'exp_inc', 'freq_num', 'freq_interval', 'begin_date',
                  'end_date', 'value']
        widgets = {'begin_date': widgets.SelectDateWidget,
                   'end_date': widgets.SelectDateWidget}

class OverrideItemForm(forms.Form):
    """override value of recurring item on specific date"""
    name = forms.ChoiceField(choices=[(item.name, item.name) for item
                                      in models.RecurItemRaw.objects.all()])
    date = forms.DateField(widget=widgets.SelectDateWidget)
    value = forms.FloatField(min_value=0, max_value=100000)

class CashLevelForm(forms.Form):
    """input actual cash level on given date"""
    cash_level = forms.FloatField(min_value=-500, max_value=100000)
    date = forms.DateField(widget=widgets.SelectDateWidget)
