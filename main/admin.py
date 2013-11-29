from django.contrib import admin
import main.models as models

admin.site.register(models.CashLevel)
admin.site.register(models.RecurItem)
admin.site.register(models.Ledger)