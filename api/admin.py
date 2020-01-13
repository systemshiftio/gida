from django.contrib import admin
import api.models as am
# Register your models here.


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'address', 'images', 
                    'ammenities', 'price', 'star_rating', 
                    'number_of_checkins', 'state', 'country', 
                    'location', 'owner', 
                    'verified', 'created', 'frequency', )

class BookedAdmin(admin.ModelAdmin):
    list_display = ('created', 'tenant', 'apartment', 'check_in', 'check_out', )
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'image', 
                    'verified', 'dob', 'phone', 
                    'star_rating', 'created', )



admin.site.register(am.GidaUser, UserAdmin)
admin.site.register(am.Apartment, ApartmentAdmin)
admin.site.register(am.BookedApartment, BookedAdmin)
