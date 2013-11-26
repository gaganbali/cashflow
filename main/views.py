# Create your views here.
from django.shortcuts import render
from django.contrib import messages
import main.forms as forms
from main.models import RecurItemRaw, OverrideItem

def add_recurring(request):
    if request.POST:
        if "recur" in request.POST:
            recur_form = forms.RecurringItemForm(request.POST)
            if recur_form.is_valid():
                messages.success(request, 'Your recurring item was successfully saved.')
                cleaned = recur_form.cleaned_data
                row = RecurItemRaw(name=cleaned['name'],
                        exp_inc=cleaned['exp_inc'],
                        freq_num=cleaned['freq_num'],
                        freq_interval=cleaned['freq_interval'],
                        base_date=cleaned['base_date'],
                        value=cleaned['value'])
                row.save()
        elif "override" in request.POST:
            override_form = forms.OverrideItemForm(request.POST)
            if override_form.is_valud():
                messages.success(request, 'Your override item was successfully saved.')
                cleaned = override_form.cleaned_data
                recur_item = RecurItemRaw.objects.filter(name=cleaned['name'])[0]
                row = OverrideItem(recur_item=recur_item,
                                   date=cleaned['date'],
                                   value=cleaned['value'])
                row.save()
    recur_form = forms.RecurringItemForm()
    override_form = forms.OverrideItemForm()
    return render(request, 'recurring_adj_form.html',
                  {'recur_form': recur_form, 
                   'override_form': override_form, 
                   'items': RecurItemRaw.objects.all()})