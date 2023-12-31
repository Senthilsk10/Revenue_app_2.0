from django.contrib import admin

from .models import User

from django.contrib.auth.admin import UserAdmin

fields = list(UserAdmin.fieldsets)
fields[1] = ("personal info",{'fields':("first_name","last_name","email","current_status", "registration_number", "surname", "firstname", "other_name", "gender", "date_of_birth", "current_class", "date_of_admission", "quali", "mobile_number", "parent_mobile_number", "address", "others")})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User,UserAdmin)