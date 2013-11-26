from django import forms
from django.forms.extras import widgets
import main.models as models

FREQ_INTERVAL_CHOICES = [('M', 'Month(s)'), ('W', 'Week(s)'),
                         ('D', 'Day(s)')]

class RecurringItemForm(forms.Form):
    """for users to enter recurring items
    data get loaded into RecurItemRaw
    
    """
    name = forms.CharField()
    exp_inc = forms.ChoiceField(choices=[('exp', 'Expense'), ('inc', 'Income')],
                                initial='exp')
    freq_num = forms.TypedChoiceField(choices=[(n, n) for n in range(91)],
                                      coerce=int, empty_value=1, initial=1)
    freq_interval = forms.ChoiceField(choices=FREQ_INTERVAL_CHOICES,
                                      initial='M')
    base_date = forms.DateField(widget=widgets.SelectDateWidget)
    value = forms.FloatField(min_value=0, max_value=100000)

class OverrideItemForm(forms.Form):
    """override value of recurring item on specific date"""
    name = forms.ChoiceField(choices=[item.name for item in models.RecurItemRaw.objects.all()])
    date = forms.DateField(widget=widgets.SelectDateWidget)
    value = forms.FloatField(min_value=0, max_value=100000)

f = OverrideItemForm()
print(f)