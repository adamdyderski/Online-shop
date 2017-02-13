from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import * 

class MyUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
            ('Dane adresowe:', {'fields': ('street', 'postcode', 'city')}),
            ('Dane kontaktowe:', {'fields': ('phone',)}),
    )


admin.site.register(User, MyUserAdmin)