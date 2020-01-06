from django.contrib import admin
import waitlist.models as wm
# Register your models here.


class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'location', )




admin.site.register(wm.WaitList, WaitlistAdmin)

