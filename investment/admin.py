from django.contrib import admin
import investment.models as im
# Register your models here.


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('roi', 'investment_time', 'description', 'images', 'state', 'location', 'status', 'min_investment', )

class InvestmentAdmin(admin.ModelAdmin):
    list_display =('owner', 'apartment', 'principal', 'current_value', 'maturity_period', 'active', 'created', ) 


admin.site.register(im.PersonalInvestment, InvestmentAdmin)
admin.site.register(im.Apartment, ApartmentAdmin)

