from django.contrib import admin
from .models import User, Address, City, Country

admin.site.register(User)
admin.site.register(Address)
admin.site.register(City)
admin.site.register(Country)
